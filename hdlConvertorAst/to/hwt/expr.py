from copy import copy

from hdlConvertorAst.hdlAst import HdlOpType
from hdlConvertorAst.to.basic_hdl_sim_model.expr import ToBasicHdlSimModelExpr
from hdlConvertorAst.to.common import ASSOCIATIVITY


class ToHwtExpr(ToBasicHdlSimModelExpr):
    OP_PRECEDENCE = copy(ToBasicHdlSimModelExpr.OP_PRECEDENCE)
    OP_PRECEDENCE.update({
        HdlOpType.DOWNTO: (1, ASSOCIATIVITY.L_TO_R),
    })
    GENERIC_BIN_OPS = copy(ToBasicHdlSimModelExpr.GENERIC_BIN_OPS)
    GENERIC_BIN_OPS.update({
        HdlOpType.DOWNTO: ":",
    })

    def visit_HdlOp(self, o):
        """
        :type op: HdlOp
        """
        op = o.fn
        if op in (HdlOpType.AND_UNARY, HdlOpType.OR_UNARY, HdlOpType.XOR_UNARY):
            ops = o.ops
            assert len(ops) == 1, ops
            w = self.out.write
            if HdlOpType.AND_UNARY:
                w("And(*")
            elif op is HdlOpType.OR_UNARY:
                w("Or(*")
            elif op is HdlOpType.XOR_UNARY:
                w("Xor(*(")
            else:
                raise NotImplementedError()
            self.visit_iHdlExpr(ops[0])
            w("))")
            return

        return ToBasicHdlSimModelExpr.visit_HdlOp(self, o)
