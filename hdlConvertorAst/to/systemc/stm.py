from hdlConvertorAst.hdlAst._bases import iHdlStatement
from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._statements import HdlStmBlock, HdlStmCaseType
from hdlConvertorAst.py_ver_compatibility import method_as_function
from hdlConvertorAst.to.hdlUtils import Indent
from hdlConvertorAst.to.systemc.expr import ToSystemcExpr
from hdlConvertorAst.to.verilog.stm import ToVerilog2005Stm


class ToSystemcStm(ToSystemcExpr):

    def visit_iHdlStatement_in_statement(self, stm):
        return method_as_function(ToVerilog2005Stm.visit_iHdlStatement_in_statement)(self, stm)

    def visit_iHdlStatement(self, o):
        """
        :type o: iHdlStatement
        """
        if isinstance(o, HdlIdDef):
            return self.visit_HdlIdDef(o)
        else:
            return super(ToSystemcStm, self).visit_iHdlStatement(o)

    def visit_HdlStmBlock(self, o):
        """
        :type o: HdlStmBlock
        """
        self.visit_doc(o)
        w = self.out.write
        w("{")
        w("\n")
        with Indent(self.out):
            for s in o.body:
                need_semi = self.visit_iHdlStatement(s)
                if need_semi:
                    w(";\n")
                else:
                    w("\n")
        w("}")
        return False

    def visit_HdlStmIf(self, o):
        return method_as_function(ToVerilog2005Stm.visit_HdlStmIf)(self, o)

    def visit_HdlStmProcess(self, o):
        """
        :type o: HdlStmProcess
        """
        w = self.out.write
        self.visit_doc(o)
        w("void ")
        w(o.labels[0])
        if isinstance(o.body, HdlStmBlock):
            w("() ")
            self.visit_HdlStmBlock(o.body)
            w("\n")
        else:
            w("() {\n")
            with Indent(self.out):
                req_semi = self.visit_iHdlStatement(o.body)
                if req_semi:
                    w(";\n")
                else:
                    w("\n")
            w("}\n")

    def visit_HdlStmAssign(self, o):
        """
        :type o: HdlStmAssign
        :return: True if requires ;\n after end
        """
        self.visit_doc(o)
        w = self.out.write
        self.visit_iHdlExpr(o.dst)
        w(" = ")
        self.visit_iHdlExpr(o.src)
        return True

    def visit_HdlStmCase(self, o):
        """
        :type o: HdlStmCase

        :return: True if requires ;\n after end
        """
        self.visit_doc(o)
        w = self.out.write
        if o.type != HdlStmCaseType.CASE:
            raise NotImplementedError()
        w("switch(")
        self.visit_iHdlExpr(o.switch_on)
        w(") {\n")
        cases = o.cases
        for k, stms in cases:
            w("case ")
            self.visit_iHdlExpr(k)
            w(":")
            with Indent(self.out):
                need_semi = self.visit_iHdlStatement_in_statement(stms)
                if need_semi:
                    w(";\n")
                else:
                    w("\n")
        defal = o.default
        if defal is not None:
            w("default:")
            with Indent(self.out):
                need_semi = self.visit_iHdlStatement_in_statement(defal)
                if need_semi:
                    w(";\n")
                else:
                    w("\n")
        w("}")
        return False

    def visit_HdlStmReturn(self, o):
        return method_as_function(ToVerilog2005Stm.visit_HdlStmReturn)(self, o)

    def visit_HdlStmContinue(self, o):
        return method_as_function(ToVerilog2005Stm.visit_HdlStmContinue)(self, o)

    def visit_HdlStmBreak(self, o):
        return method_as_function(ToVerilog2005Stm.visit_HdlStmBreak)(self, o)

