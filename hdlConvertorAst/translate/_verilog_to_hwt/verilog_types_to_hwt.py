from typing import Union

from hdlConvertorAst.hdlAst import HdlOp, HdlOpType, iHdlTypeDef, iHdlExpr, \
    HdlTypeBitsDef, HdlValueId
from hdlConvertorAst.to.hwt.utils import BitsT
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_index
from hdlConvertorAst.translate.verilog_resolve_types import VerilogResolveTypes


class VerilogTypesToHwt(VerilogResolveTypes):

    def _visit_type(self, t):
        """
        :type t: Union[iHdlExpr, iHdlTypeDef]
        """
        if isinstance(t, HdlOp) and t.fn == HdlOpType.INDEX:
            o0, o1 = t.ops
            return hdl_index(self._visit_type(o0), o1)
        elif isinstance(t, HdlTypeBitsDef):
            return BitsT(t.msb, t.signed)
        elif isinstance(t, HdlValueId):
            if t == HdlValueId("integer"):
                return HdlValueId("INT")
        raise NotImplementedError(t)

    def visit_type(self, t):
        """
        :type t: iHdlExpr
        """
        t = VerilogResolveTypes.visit_type(self, t)
        return self._visit_type(t)
