
from hdlConvertorAst.hdlAst import HdlTypeBitsDef, HdlOpType, HdlOp
from hdlConvertorAst.to.basic_hdl_sim_model.utils import BitsT
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_index
from hdlConvertorAst.translate.verilog_resolve_types import VerilogResolveTypes


class VerilogTypesToBasicHdlSimModel(VerilogResolveTypes):
    """
    Translate Verilog HDL types to BasicHdlSimModel HDL types
    """
    def _visit_type(self, t):
        """
        :type t: Union[iHdlExpr, iHdlTypeDef]
        """
        if isinstance(t, HdlOp) and t.fn == HdlOpType.INDEX:
            o0, o1 = t.ops
            return hdl_index(self._visit_type(o0), o1)
        elif isinstance(t, HdlTypeBitsDef):
            return BitsT(t.msb, t.signed)
        else:
            raise NotImplementedError()

    def visit_type(self, t):
        """
        :type t: iHdlExpr
            def visit_type(self, t):
        """
        t = VerilogResolveTypes.visit_type(self, t)
        return self._visit_type(t)
