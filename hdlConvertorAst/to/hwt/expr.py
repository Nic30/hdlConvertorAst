from copy import copy

from hdlConvertorAst.hdlAst import HdlOpType
from hdlConvertorAst.to.basic_hdl_sim_model.expr import ToBasicHdlSimModelExpr


class ToHwtExpr(ToBasicHdlSimModelExpr):
    GENERIC_BIN_OPS = copy(ToBasicHdlSimModelExpr.GENERIC_BIN_OPS)
    GENERIC_BIN_OPS.update({
        HdlOpType.DOWNTO: ":",
    })
