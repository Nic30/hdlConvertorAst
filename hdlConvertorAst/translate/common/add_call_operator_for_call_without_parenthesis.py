from hdlConvertorAst.hdlAst import HdlOp, HdlValueId, HdlFunctionDef, HdlOpType
from hdlConvertorAst.to.hdl_ast_modifier import HdlAstModifier
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_call


class AddCallOperatorForCallWithoutParenthesis(HdlAstModifier):
    """
    Verilog function call does not need to have () and it can be called just by its id.
    To simplify handling we decorete each such a call with a call operator in this transformation.
    """

    def __init__(self):
        HdlAstModifier.__init__(self)
        self._parentExpr = None

    def visit_iHdlExpr(self, o):
        """
        :type o: iHdlExpr
        :return: iHdlExpr
        """
        if isinstance(o, HdlOp):
            prev_par_expr = self._parentExpr
            self._parentExpr = o
            try:
                self.visit_HdlOp(o)
            finally:
                self._parentExpr = prev_par_expr
        else:
            if isinstance(o, HdlValueId) and\
                    isinstance(o.obj, HdlFunctionDef) and \
                    ( not isinstance(self._parentExpr, HdlOp) or \
                      self._parentExpr.fn != HdlOpType.CALL or \
                      self._parentExpr.ops[0] is not o
                      ):
                # wrap function id in a call operator if parent is not a call operator
                return hdl_call(o, [])
        return o
