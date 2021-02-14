from itertools import chain

from hdlConvertorAst.hdlAst import iHdlStatement, HdlIdDef, \
    HdlModuleDec, HdlModuleDef, HdlCompInst, HdlFunctionDef
from hdlConvertorAst.to.hdl_ast_visitor import HdlAstVisitor
from hdlConvertorAst.translate.common.name_scope import WithNameScope


class BuiltIn(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.name)


class DiscoverDeclarations(HdlAstVisitor):

    def __init__(self, name_scope):
        """
        :type name_scope: NameScope
        """
        super(DiscoverDeclarations, self).__init__()
        self.name_scope = name_scope

    def visit_HdlIdDef(self, o):
        """
        :type name_scope: NameScope
        :type o: HdlIdDef
        """
        self.name_scope.register_name(o.name, o)

    def visit_HdlModuleDec(self, o):
        """
        :type name_scope: NameScope
        :type o: HdlModuleDec
        """
        ns = self.name_scope
        ns.register_name(o.name, o)
        with WithNameScope(self, ns.level_push(o.name)):
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
            self.discover_declarations(o.objs)

    def visit_HdlCompInst(self, o):
        """
        :type o: HdlCompInst
        """
        if o.name is not None:
            self.name_scope.register_name(o.name, o)
        # name_scope = name_scope.get_object_by_name(o.module_name)

    def visit_HdlFunctionDef(self, o):
        """
        :type o: HdlFunctionDef
        """
        ns = self.name_scope
        ns.register_name(o.name, o)
        with WithNameScope(self, ns.level_push(o.name)):
            self.discover_declarations(o.params)
            self.discover_declarations(o.body)
        return o

    def _discover_declarations(self, o):
        if isinstance(o, HdlIdDef):
            self.visit_HdlIdDef(o)
        elif isinstance(o, HdlModuleDec):
            self.visit_HdlModuleDec(o)
        elif isinstance(o, HdlModuleDef):
            self.visit_HdlModuleDef(o)
        elif isinstance(o, iHdlStatement):
            pass
        elif isinstance(o, HdlCompInst):
            self.visit_HdlCompInst(o)
        elif isinstance(o, HdlFunctionDef):
            self.visit_HdlFunctionDef(o)
        else:
            raise NotImplementedError(o)

    def discover_declarations(self, objs):
        for o in objs:
            self._discover_declarations(o)
