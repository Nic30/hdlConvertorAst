from hdlConvertorAst.hdlAst import HdlOp, HdlStmIf, HdlStmWhile, HdlStmBlock, HdlStmAssign, HdlStmCaseType
from hdlConvertorAst.to.hdlUtils import Indent, iter_with_last
from hdlConvertorAst.to.hwt.expr import ToHwtExpr
from hdlConvertorAst.to.basic_hdl_sim_model import ToBasicHdlSimModel


class ToHwtStm(ToHwtExpr):

    def visit_HdlStmProcess(self, o):
        """
        :type o: HdlStmProcess
        """
        w = self.out.write
        if o.labels:
            w("# ")
            if o.labels:
                w(o.labels[0])
                # w(", ")
        # w("sens: ")
        # if o.sensitivity:
        #    for last, s in iter_with_last(o.sensitivity):
        #        if isinstance(s, HdlOp):
        #            w(str(s.fn))
        #            w(" ")
        #            self.visit_iHdlExpr(s.ops[0])
        #        else:
        #            self.visit_iHdlExpr(s)
        #        if not last:
        #            w(", ")
        w("\n")
        self.visit_doc(o)
        if o.trigger_constrain is not None:
            raise NotImplementedError()
        self.visit_iHdlStatement(o.body)
        # w("\n")

    def visit_HdlStmBlock(self, o):
        """
        :type o: HdlStmBlock
        """
        self.visit_doc(o)
        w = self.out.write
        for is_last, i in iter_with_last(o.body):
            self.visit_iHdlStatement(i)
            if not is_last:
                if o.in_preproc:
                    w("\n")
                else:
                    w(",\n")

    def visit_HdlStmIf(self, o):
        """
        :type stm: HdlStmIf
        """
        self.visit_doc(o)
        w = self.out.write

        in_preproc = o.in_preproc
        if in_preproc:
            w("if ")
        else:
            w("If(")
        self.visit_iHdlExpr(o.cond)
        if in_preproc:
            w(":\n")
        else:
            w(",\n")
        with Indent(self.out):
            self.visit_iHdlStatement(o.if_true)
            w("\n")
        if not in_preproc:
            w(")")
        for (c, _stm) in o.elifs:
            if in_preproc:
                w("elif ")
            else:
                w(".Elif(")
            self.visit_iHdlExpr(c)
            if in_preproc:
                w(":\n")
            else:
                w(",\n")
            with Indent(self.out):
                self.visit_iHdlStatement(_stm)
            w("\n")
            if not in_preproc:
                w(")")

        ifFalse = o.if_false
        if ifFalse is not None:
            if in_preproc:
                w("else:\n")
            else:
                w(".Else(\n")
            with Indent(self.out):
                self.visit_iHdlStatement(ifFalse)
                w("\n")
            if not in_preproc:
                w(")")

    def visit_HdlStmAssign(self, o):
        """
        :type o: HdlStmAssign
        """
        self.visit_doc(o)
        w = self.out.write
        self.visit_iHdlExpr(o.dst)
        if o.is_blocking:
            raise NotImplementedError(o)
        if o.time_delay is not None:
            raise NotImplementedError()
        if o.event_delay is not None:
            raise NotImplementedError()
        if o.in_preproc:
            w(" = ")
            self.visit_iHdlExpr(o.src)
        else:
            w("(")
            self.visit_iHdlExpr(o.src)
            w(")")

    def visit_HdlStmCase(self, o):
        """
        :type o: HdlStmCase
        """
        self.visit_doc(o)
        if o.uniq_constrain is not None:
            raise NotImplementedError()
        w = self.out.write
        if o.in_preproc:
            assert o.cases
            first = True
            for c, stm in o.cases:
                if first:
                    w("if ")
                    first = False
                else:
                    w("elif ")
                self.visit_iHdlExpr(o.switch_on)
                w(" == ")
                self.visit_iHdlExpr(c)
                w(":\n")
                with Indent(self.out):
                    self.visit_iHdlStatement(stm)
                w("\n")

            if o.default is not None:
                w("else:\n")
                with Indent(self.out):
                    self.visit_iHdlStatement(o.default)

        else:
            # if o.type != HdlStmCaseType.CASE:
            #    raise NotImplementedError(o.type)
            w("Switch(")
            self.visit_iHdlExpr(o.switch_on)
            w(")")
            with Indent(self.out):
                for c, stm in o.cases:
                    w("\\\n")
                    w(".Case(")
                    self.visit_iHdlExpr(c)
                    w(",\n")
                    with Indent(self.out):
                        self.visit_iHdlStatement(stm)
                    w(")")
                if o.default is not None:
                    w("\\\n")
                    w(".Default(\n")
                    with Indent(self.out):
                        self.visit_iHdlStatement(o.default)
                        w(")")

    def visit_HdlStmFor(self, o):
        """
        :type o: HdlStmFor
        """
        if not o.in_preproc:
            raise TypeError("does not support HdlStmFor", self, o)
        self.visit_doc(o)
        w = self.out.write
        # [todo] if is a simple for in range()

        self.visit_iHdlObj(o.init)
        w("\n")
        w("while ")
        self.visit_iHdlExpr(o.cond)
        w(":\n")
        with Indent(self.out):
            self.visit_iHdlObj(o.body)

    def visit_HdlStmWhile(self, o):
        """
        :type o: HdlStmWhile
        """
        self.visit_doc(o)
        assert o.in_preproc
        w = self.out.write
        w("while ")
        self.visit_iHdlExpr(o.cond)
        w(":\n")
        with Indent(self.out):
            self.visit_iHdlObj(o.body)

    def visit_HdlStmBreak(self, o):
        """
        :type o: HdlStmBreak
        """
        assert o.in_preproc, o
        self.out.write("break")
    
    def visit_HdlStmContinue(self, o):
        """
        :type o: HdlStmContinue
        """
        assert o.in_preproc, o
        self.out.write("continue")
    
    def visit_HdlStmThrow(self, o):
        ToBasicHdlSimModel.visit_HdlStmThrow(self, o)

    def visit_HdlStmWait(self, o):
        ToBasicHdlSimModel.visit_HdlStmWait(self, o)

    def visit_HdlStmNop(self, o):
        ToBasicHdlSimModel.visit_HdlStmNop(self, o)
