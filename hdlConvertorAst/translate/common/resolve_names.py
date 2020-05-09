"""
Use declarations collected from resolve_names
and use them to associate HdlValueIds to a HdlObjects.
"""
from itertools import chain

from hdlConvertorAst.hdlAst import HdlOp, HdlOpType, HdlValueId, HdlAll,\
    HdlValueInt, HdlIdDef, HdlStmAssign, HdlModuleDec, HdlModuleDef,\
    HdlCompInst, iHdlStatement
from hdlConvertorAst.to.hdl_ast_visitor import HdlAstVisitor
from hdlConvertorAst.translate.common.discover_declarations import WithNameScope


class ResolveNames(HdlAstVisitor):

    def __init__(self, name_scope):
        """
        :type name_scope: NameScope
        """
        super(ResolveNames, self).__init__()
        self.name_scope = name_scope
        self.in_args = False

    def visit_HdlIdDef(self, o):
        """
        :type o: HdlIdDef
        """
        self.name_scope.register_name(o.name, o)

    def visit_HdlModuleDec(self, o):
        """
        :type o: HdlModuleDec
        """
        with WithNameScope(self, self.name_scope.level_push(o.name)):
            for p in chain(o.params, o.ports):
                self.visit_HdlIdDef(p)

            for o2 in o.objs:
                raise NotImplementedError(o2)

    def visit_HdlModuleDef(self, o):
        """
        :type o: HdlModuleDef
        """
        if o.dec is not None:
            self.visit_HdlModuleDec(o.dec)

        with WithNameScope(self, self.name_scope.get_child(o.module_name.val)):
            for o2 in o.objs:
                self.visit_iHdlObj(o2)

    def visit_port_param_map(self, mod_name_scope, pmap):
        """
        :type pmap: List[HdlOp]
        """
        for pm in pmap:
            assert isinstance(pm, HdlOp) and\
                pm.fn == HdlOpType.MAP_ASSOCIATION, pm
            mod_port, connected_sig = pm.ops
            assert isinstance(mod_port, HdlValueId), mod_port
            orig_name_scope = self.name_scope
            try:
                self.name_scope = mod_name_scope
                self.visit_iHdlExpr(mod_port)
            finally:
                self.name_scope = orig_name_scope

            self.visit_iHdlExpr(connected_sig)

    def visit_HdlCompInst(self, o):
        """
        :type o: HdlCompInst
        """
        if o.name is not None:
            o.name.obj = o
        ns = self.name_scope
        mod_name_scope, mod_def = ns.get_object_and_scope_by_name(
            o.module_name.val)
        mod_name_scope = mod_name_scope.get_child(o.module_name.val)
        o.module_name.obj = mod_def
        self.visit_port_param_map(mod_name_scope, o.param_map)
        self.visit_port_param_map(mod_name_scope, o.port_map)

    def visit_iHdlExpr(self, o):
        """
        :type o: iHdlExpr
        """
        if isinstance(o, HdlOp):
            if o.fn is HdlOpType.DOT:
                # resolve only top id in id.id.id....
                self.visit_iHdlExpr(o.ops[0])
                assert isinstance(o.ops[1], HdlValueId), o.ops[1]

            elif o.fn in (HdlOpType.CALL, HdlOpType.PARAMETRIZATION):
                # mark argument list so we know that we should not search for
                # keyword ids
                orig_in_args = self.in_args
                try:
                    self.visit_iHdlExpr(o.ops[0])
                    self.in_args = True
                    for o2 in o.ops[1:]:
                        self.visit_iHdlExpr(o2)
                finally:
                    self.in_args = orig_in_args

            elif self.in_args and o.fn == HdlOpType.MAP_ASSOCIATION:
                # function keyword args, do not search for argument object
                assert isinstance(o.ops[0], HdlValueId), o.ops[0]
                for o2 in o.ops[1:]:
                    self.visit_iHdlExpr(o2)

            else:
                for o2 in o.ops:
                    self.visit_iHdlExpr(o2)

        elif isinstance(o, HdlValueId):
            _, o.obj = self.name_scope.get_object_and_scope_by_name(o.val)

        elif o is None or o is HdlAll or isinstance(
                o,  (HdlValueInt, float, str)):
            pass

        elif isinstance(o, (list, tuple)):
            for o2 in o:
                self.visit_iHdlExpr(o2)

        else:
            raise NotImplementedError(o)
