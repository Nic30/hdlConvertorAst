from hdlConvertorAst.hdlAst import HdlImport, HdlStmProcess, HdlStmIf,\
    HdlStmAssign, HdlStmCase, HdlStmWait, HdlStmReturn, HdlStmFor, HdlStmForIn,\
    HdlStmWhile, HdlStmBlock, iHdlStatement, HdlModuleDec, HdlModuleDef,\
    HdlValueIdspace, HdlIdDef, HdlFunctionDef, HdlOp, HdlCompInst, \
    HdlValueInt, HdlStmBreak, HdlStmContinue, HdlStmRepeat, HdlLibrary, HdlContext,\
    HdlClassDef, HdlPhysicalDef, HdlEnumDef
from hdlConvertorAst.to.hdl_ast_visitor import HdlAstVisitor


class HdlAstModifier(HdlAstVisitor):
    """
    A visitor which can be used to traverse and modyfy AST (Abstract Syntax Tree) made of objects
    from `hdlConvertorAst.hdlAst` module.
    Each visit function has to return the object which replaces current object
    It should return the same object if no change is required.
    """

    def visit_iHdlObj_list(self, obj_list, visit_fn):
        """
        :ivar obj_list: list of HDL objects
        :ivar visit_fn: function to modidify the object
        """
        for i, o in enumerate(obj_list):
            obj_list[i] = visit_fn(o)
        return obj_list

    def visit_HdlContext(self, context):
        """
        :type context: HdlContext
        """
        self.visit_iHdlObj_list(context.objs, self.visit_main_obj)
        return context

    def visit_HdlValueIdspace(self, o):
        """
        :type o: HdlValueIdspace
        """
        self.visit_doc(o)
        self.visit_iHdlObj_list(o.objs, self.visit_iHdlObj)
        return o

    def visit_HdlModuleDec(self, o):
        """
        :type o: HdlModuleDec
        """
        self.visit_doc(o)
        self.visit_iHdlObj_list(o.params, self.visit_param)
        self.visit_iHdlObj_list(o.ports, self.visit_port)
        self.visit_iHdlObj_list(o.objs, self.visit_main_obj)
        return o

    def visit_HdlIdDef(self, o):
        """
        :type o: HdlIdDef
        """
        self.visit_doc(o)
        o.type = self.visit_type(o.type)
        if o.value is not None:
            o.value = self.visit_iHdlExpr(o.value)
        
        return o

    def visit_iHdlExpr(self, o):
        """
        :type o: iHdlExpr
        :return: iHdlExpr
        """
        if isinstance(o, HdlOp):
            return self.visit_HdlOp(o)
        else:
            return o

    def visit_HdlOp(self, o):
        """
        :type o: HdlOp
        :return: iHdlExpr
        """
        self.visit_iHdlObj_list(o.ops, self.visit_iHdlExpr)
        return o

    def visit_HdlValueInt(self, o):
        """
        :type o: HdlValueInt
        """
        return o

    def visit_port(self, o):
        return self.visit_HdlIdDef(o)

    def visit_param(self, o):
        return self.visit_HdlIdDef(o)

    def visit_HdlModuleDef(self, o):
        """
        :type o: HdlModuleDef
        """
        if o.dec is not None:
            o.dec = self.visit_HdlModuleDec(o.dec)

        self.visit_doc(o)
        objs = o.objs
        for i, _o in enumerate(objs):
            if isinstance(_o, iHdlStatement):
                _o = self.visit_iHdlStatement(_o)
            elif isinstance(_o, HdlIdDef):
                _o = self.visit_HdlIdDef(_o)
            elif isinstance(_o, HdlCompInst):
                _o = self.visit_HdlCompInst(_o)
            elif isinstance(_o, HdlFunctionDef):
                _o = self.visit_HdlFunctionDef(_o)
            else:
                raise NotImplementedError(_o)
            objs[i] = _o
        return o

    def visit_HdlCompInst(self, o):
        """
        :type o: HdlCompInst
        """
        self.visit_doc(o)
        self.visit_iHdlObj_list(o.param_map, self.visit_iHdlExpr)
        self.visit_iHdlObj_list(o.port_map, self.visit_iHdlExpr)
        return o

    def visit_HdlClassDef(self, o):
        """
        :type o: HdlClassDef
        """
        self.visit_doc(o)
        
        self.visit_iHdlObj_list(o.base_types, self.visit_iHdlExpr)
        self.visit_iHdlObj_list(o.members, self.visit_iHdlObj)

        return o

    def visit_HdlPhysicalDef(self, o):
        """
        :type o: HdlPhysicalDef
        """
        return o
    
    def visit_HdlEnumDef(self, o):
        """
        :type o: HdlEnumDef
        """
        return o

    def visit_HdlFunctionDef(self, o):
        """
        :type o: HdlFunctionDef
        """
        self.visit_doc(o)
        self.visit_iHdlObj_list(o.params, self.visit_HdlIdDef)
        if o.return_t is not None:
            o.return_t = self.visit_iHdlExpr(o.return_t)

        self.visit_iHdlObj_list(o.body, self.visit_main_obj)
        return o

    def visit_HdlStmProcess(self, o):
        """
        :type o: HdlStmProcess
        """
        self.visit_doc(o)
        o.body = self.visit_iHdlStatement(o.body)
        return o

    def visit_HdlStmBlock(self, o):
        """
        :type o: HdlStmBlock
        """
        self.visit_doc(o)
        self.visit_iHdlObj_list(o.body, self.visit_iHdlStatement)
        return o

    def visit_HdlStmCase(self, o):
        """
        :type o: HdlStmCase
        """
        self.visit_doc(o)
        o.switch_on = self.visit_iHdlExpr(o.switch_on)
        cases = o.cases
        for i, (c, stm) in enumerate(cases):
            new_c = self.visit_iHdlExpr(c)
            new_stm = self.visit_iHdlStatement(stm)
            cases[i] = (new_c, new_stm)

        if o.default is not None:
            o.default = self.visit_iHdlStatement(o.default)
        return o

    def visit_HdlStmWait(self, o):
        """
        :type o: HdlStmWait
        """
        self.visit_doc(o)
        o.val = self.visit_iHdlExpr(o.val)
        return o

    def visit_HdlStmIf(self, o):
        """
        :type o: HdlStmIf
        """
        self.visit_doc(o)
        o.cond = self.visit_iHdlExpr(o.cond)
        if o.if_true is not None:
            o.if_true = self.visit_iHdlStatement(o.if_true)

        for i, (c, stm) in enumerate(o.elifs):
            new_c = self.visit_iHdlExpr(c)
            new_stm = self.visit_iHdlStatement(stm)
            o.elifs[i] = (new_c, new_stm)

        if o.if_false is not None:
            o.if_false = self.visit_iHdlStatement(o.if_false)
        return o

    def visit_HdlStmFor(self, o):
        """
        :type o: HdlStmFor
        """
        self.visit_doc(o)
        o.init = self.visit_iHdlStatement(o.init)
        o.cond = self.visit_iHdlExpr(o.cond)
        o.step = self.visit_iHdlStatement(o.step)
        o.body = self.visit_iHdlStatement(o.body)
        return o

    def visit_HdlStmForIn(self, o):
        """
        :type o: HdlStmForIn
        """
        self.visit_doc(o)
        self.visit_iHdlObj_list(o.var_defs, self.visit_main_obj)
        o.collection = self.visit_iHdlExpr(o.collection)
        o.body = self.visit_iHdlStatement(o.body)
        return o

    def visit_HdlStmWhile(self, o):
        """
        :type o: HdlStmWhile
        """
        self.visit_doc(o)
        o.cond = self.visit_iHdlExpr(o.cond)
        o.body = self.visit_iHdlStatement(o.body)
        return o

    def visit_HdlStmRepeat(self, o):
        """
        :type o: HdlStmRepeat
        """
        self.visit_doc(o)
        o.n = self.visit_iHdlExpr(o.n)
        o.body = self.visit_iHdlStatement(o.body)
        return o

    def visit_HdlStmReturn(self, o):
        """
        :type o: HdlStmReturn
        """
        self.visit_doc(o)
        if o.val is not None:
            o.val = self.visit_iHdlExpr(o.val)
        return o

    def visit_HdlStmAssign(self, o):
        """
        :type o: HdlStmAssign
        """
        self.visit_doc(o)
        o.src = self.visit_iHdlExpr(o.src)
        o.dst = self.visit_iHdlExpr(o.dst)
        if o.event_delay is not None:
            o.event_delay = self.visit_iHdlExpr(o.event_delay)
        if o.time_delay is not None:
            o.time_delay = self.visit_iHdlExpr(o.time_delay)
        return o
