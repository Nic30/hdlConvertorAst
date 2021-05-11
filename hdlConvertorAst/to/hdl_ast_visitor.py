from itertools import chain

from hdlConvertorAst.hdlAst import HdlImport, HdlStmProcess, HdlStmIf, \
    HdlStmAssign, HdlStmCase, HdlStmWait, HdlStmReturn, HdlStmFor, HdlStmForIn, \
    HdlStmWhile, HdlStmBlock, iHdlStatement, HdlModuleDec, HdlModuleDef, \
    HdlValueIdspace, HdlIdDef, HdlFunctionDef, HdlOp, HdlCompInst, \
    HdlValueInt, HdlStmBreak, HdlStmContinue, HdlStmRepeat, HdlLibrary, HdlContext, \
    HdlClassDef, HdlPhysicalDef, HdlEnumDef, ALL_STATEMENT_CLASSES, HdlStmNop,\
    HdlValueId


class HdlAstVisitor(object):
    """
    A visitor which can be used to traverse AST (Abstract Syntax Tree) made of objects from `hdlConvertorAst.hdlAst` module.

    """

    def __init__(self):
        self._visit_call_dispatch_dict = {
            cls: getattr(self, "visit_" + cls.__name__)
            for cls in [
                HdlContext, HdlImport, HdlLibrary, HdlModuleDec, HdlModuleDef,
                HdlValueIdspace, HdlIdDef, HdlFunctionDef,
                HdlClassDef, HdlPhysicalDef, HdlEnumDef,
                HdlCompInst, HdlOp, HdlValueInt] + list(ALL_STATEMENT_CLASSES)
        }

    def visit_iHdlObj(self, o):
        visit_fn = self._visit_call_dispatch_dict.get(o.__class__, None)
        if visit_fn is not None:
            return visit_fn(o)
        else:
            return self.visit_iHdlExpr(o)

    def visit_doc(self, o):
        pass

    def visit_HdlContext(self, context):
        """
        :type context: HdlContext
        """
        for o in context.objs:
            self.visit_main_obj(o)

        return context

    def visit_HdlImport(self, o):
        """
        :type o: HdlImport
        """
        return o

    def visit_HdlLibrary(self, o):
        """
        :type o: HdlLibrary
        """
        return o

    def visit_HdlValueIdspace(self, o):
        """
        :type o: HdlValueIdspace
        """
        self.visit_doc(o)
        for o2 in o.objs:
            self.visit_iHdlObj(o2)
        return o

    def visit_main_obj(self, o):
        visit_fn = self._visit_call_dispatch_dict.get(o.__class__, None)
        if visit_fn is not None:
            return visit_fn(o)
        else:
            return self.visit_iHdlExpr(o)

    def visit_iHdlStatement(self, o):
        """
        :type o: iHdlStatement
        """
        # statement can be also expressin
        visit_fn = self._visit_call_dispatch_dict.get(o.__class__, None)
        if visit_fn is not None:
            return visit_fn(o)
        elif o is None:
            return self.visit_HdlStmNop(HdlStmNop())
        else:
            return self.visit_iHdlExpr(o)

    def visit_HdlModuleDec(self, o):
        """
        :type o: HdlModuleDec
        """
        self.visit_doc(o)
        for p in o.params:
            self.visit_param(p)
        for p in o.ports:
            self.visit_port(p)
        for o2 in o.objs:
            self.visit_main_obj(o2)
        return o

    def visit_HdlIdDef(self, o):
        """
        :type o: HdlIdDef
        """
        self.visit_doc(o)
        self.visit_type(o.type)
        if o.value is not None:
            self.visit_iHdlExpr(o.value)
        return o

    def visit_iHdlExpr(self, o):
        """
        :type o: iHdlExpr
        :return: iHdlExpr
        """
        if isinstance(o, HdlOp):
            return self.visit_HdlOp(o)
        return o

    def visit_HdlOp(self, o):
        """
        :type o: HdlOp
        :return: iHdlExpr
        """
        for op in o.ops:
            self.visit_iHdlExpr(op)
        return o

    def visit_HdlValueInt(self, o):
        """
        :type o: HdlValueInt
        """
        return o

    def visit_port(self, o):
        """
        :type o: HdlIdDef
        """
        return self.visit_HdlIdDef(o)

    def visit_param(self, o):
        """
        :type o: HdlIdDef
        """
        return self.visit_HdlIdDef(o)

    def visit_HdlModuleDef(self, o):
        """
        :type o: HdlModuleDef
        """
        if o.dec is not None:
            self.visit_HdlModuleDec(o.dec)

        self.visit_doc(o)
        for _o in o.objs:
            if isinstance(_o, iHdlStatement):
                self.visit_iHdlStatement(_o)
            elif isinstance(_o, HdlIdDef):
                self.visit_HdlIdDef(_o)
            elif isinstance(_o, HdlCompInst):
                self.visit_HdlCompInst(_o)
            elif isinstance(_o, HdlFunctionDef):
                self.visit_HdlFunctionDef(_o)
            elif isinstance(_o, HdlModuleDec):
                # vhdl components
                self.visit_HdlModuleDec(_o)
            elif isinstance(_o, HdlOp):
                assert _o.ops[0] == HdlValueId("assert"), _o
                self.visit_HdlOp(_o)
            else:
                raise NotImplementedError(_o)
        return o

    def visit_HdlCompInst(self, o):
        """
        :type o: HdlCompInst
        """
        self.visit_doc(o)
        for pm in chain(o.param_map, o.port_map):
            self.visit_iHdlExpr(pm)
        return o

    def visit_HdlClassDef(self, o):
        """
        :type o: HdlClassDef
        """
        self.visit_doc(o)
        for t in o.base_types:
            self.visit_iHdlExpr(t)

        for m in o.members:
            self.visit_iHdlObj(m)

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
        for p in o.params:
            self.visit_HdlIdDef(p)
        if o.return_t is not None:
            self.visit_iHdlExpr(o.return_t)
        for o2 in o.body:
            self.visit_main_obj(o2)
        return o

    def visit_HdlStmProcess(self, o):
        """
        :type o: HdlStmProcess
        """
        self.visit_doc(o)
        self.visit_iHdlStatement(o.body)
        return o

    def visit_HdlStmBlock(self, o):
        """
        :type o: HdlStmBlock
        """
        self.visit_doc(o)
        for o2 in o.body:
            self.visit_iHdlStatement(o2)
        return o

    def visit_HdlStmCase(self, o):
        """
        :type o: HdlStmCase
        """
        self.visit_doc(o)
        self.visit_iHdlExpr(o.switch_on)
        for c, stm in o.cases:
            self.visit_iHdlExpr(c)
            self.visit_iHdlStatement(stm)
        if o.default is not None:
            self.visit_iHdlStatement(o.default)
        return o

    def visit_HdlStmWait(self, o):
        """
        :type o: HdlStmWait
        """
        self.visit_doc(o)
        self.visit_iHdlExpr(o.val)
        return o

    def visit_HdlStmIf(self, o):
        """
        :type o: HdlStmIf
        """
        self.visit_doc(o)
        self.visit_iHdlExpr(o.cond)
        if o.if_true is not None:
            self.visit_iHdlStatement(o.if_true)
        for c, stm in o.elifs:
            self.visit_iHdlExpr(c)
            self.visit_iHdlStatement(stm)
        if o.if_false is not None:
            self.visit_iHdlStatement(o.if_false)
        return o

    def visit_HdlStmFor(self, o):
        """
        :type o: HdlStmFor
        """
        self.visit_doc(o)
        self.visit_iHdlStatement(o.init)
        self.visit_iHdlExpr(o.cond)
        self.visit_iHdlStatement(o.step)
        self.visit_iHdlStatement(o.body)
        return o

    def visit_HdlStmForIn(self, o):
        """
        :type o: HdlStmForIn
        """
        self.visit_doc(o)
        for v in o.var_defs:
            self.visit_main_obj(v)
        self.visit_iHdlExpr(o.collection)
        self.visit_iHdlStatement(o.body)
        return o

    def visit_HdlStmWhile(self, o):
        """
        :type o: HdlStmWhile
        """
        self.visit_doc(o)
        self.visit_iHdlExpr(o.cond)
        self.visit_iHdlStatement(o.body)
        return o

    def visit_HdlStmRepeat(self, o):
        """
        :type o: HdlStmRepeat
        """
        self.visit_doc(o)
        self.visit_iHdlExpr(o.n)
        self.visit_iHdlStatement(o.body)
        return o

    def visit_HdlStmReturn(self, o):
        """
        :type o: HdlStmReturn
        """
        self.visit_doc(o)
        if o.val is not None:
            self.visit_iHdlExpr(o.val)
        return o

    def visit_HdlStmBreak(self, o):
        """
        :type o: HdlStmBreak
        """
        self.visit_doc(o)
        return o

    def visit_HdlStmNop(self, o):
        """
        :type o: HdlStmNop
        """
        self.visit_doc(o)
        return o

    def visit_HdlStmContinue(self, o):
        """
        :type o: HdlStmContinue
        """
        self.visit_doc(o)
        return o

    def visit_HdlStmThrow(self, o):
        """
        :type o: HdlStmThrow
        """
        self.visit_doc(o)
        self.visit_iHdlExpr(o.val)
        return o

    def visit_HdlStmAssign(self, o):
        """
        :type o: HdlStmAssign
        """
        self.visit_doc(o)
        self.visit_iHdlExpr(o.src)
        self.visit_iHdlExpr(o.dst)
        if o.event_delay is not None:
            self.visit_iHdlExpr(o.event_delay)
        if o.time_delay is not None:
            self.visit_iHdlExpr(o.time_delay)
        return o

    def visit_type(self, t):
        """
        :type t: iHdlExpr
        """
        return self.visit_iHdlExpr(t)
