from hdlConvertorAst.hdlAst import HdlOp, HdlOpType
from hdlConvertorAst.to.hdl_ast_modifier import HdlAstModifier
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_call


class SignalAssignmentsToCallOp(HdlAstModifier):
    """
    Convert an assignment to an call operator.
    """

    def visit_HdlStmAssign(self, o):
        """
        :type o: HdlStmAssign
        """
        assert o.event_delay is None, o
        assert o.time_delay is None, o
        return hdl_call(o.dst, [o.src, ])

    def visit_HdlOp(self, o):
        """
        :type o: HdlOp
        :return: HdlOp
        """
        if o.fn == HdlOpType.ASSIGN:
            dst, src = o.ops
            return hdl_call(dst, [src, ])
        elif o.fn in [
            HdlOpType.PLUS_ASSIGN,  # +=
            HdlOpType.MINUS_ASSIGN,  # -=
            HdlOpType.MUL_ASSIGN,  # *=
            HdlOpType.DIV_ASSIGN,  # /=
            HdlOpType.MOD_ASSIGN,  # %=
            HdlOpType.AND_ASSIGN,  # &=
            HdlOpType.OR_ASSIGN,  # |=
            HdlOpType.XOR_ASSIGN,  # ^=
            HdlOpType.SHIFT_LEFT_ASSIGN,  # <<=
            HdlOpType.SHIFT_RIGHT_ASSIGN,  # >>=
            HdlOpType.ARITH_SHIFT_LEFT_ASSIGN,  # <<<=
            HdlOpType.ARITH_SHIFT_RIGHT_ASSIGN,  # >>>=
           ]:
            raise NotImplementedError() 
            
        return o
