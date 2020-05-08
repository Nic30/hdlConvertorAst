from hdlConvertorAst.hdlAst._expr import HdlOpType, HdlOp, HdlValueId
from hdlConvertorAst.to.hdl_ast_visitor import HdlAstVisitor
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import \
    to_property_call


class BasicHdlSimModelTranslateVerilogOperands(HdlAstVisitor):
    def visit_iHdlExpr(self, o):
        """
        :type o: iHdlExpr
        """
        if isinstance(o, HdlOp):
            return self.visit_HdlOp(o)

    def visit_HdlOp(self, o):
        """
        :type o: HdlOp
        """
        op = o.fn
        if op == HdlOpType.EQ:
            # HdlOpType.EQ: '%s._eq(%s)',
            to_property_call(o, "_eq")
        elif op == HdlOpType.CONCAT:
            to_property_call(o, "_concat")
        elif op == HdlOpType.TERNARY:
            to_property_call(o, "_ternary__val")
        elif op == HdlOpType.DOWNTO:
            # HdlOpType.DOWNTO: "slice(%s, %s)",
            o.fn = HdlOpType.CALL
            o.ops = [HdlValueId("slice"), ] + o.ops
        elif op == HdlOpType.TO:
            raise NotImplementedError(o)
        elif op == HdlOpType.CALL:
            raise NotImplementedError("inline", o)
