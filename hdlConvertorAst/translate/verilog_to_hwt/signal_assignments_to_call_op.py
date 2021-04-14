from hdlConvertorAst.hdlAst import HdlOpType
from hdlConvertorAst.to.hdl_ast_modifier import HdlAstModifier
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_call
from hdlConvertorAst.to.verilog.expr import ASSIGN_OPERATORS


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
        elif o.fn in ASSIGN_OPERATORS:
            raise NotImplementedError(o)

        return o
