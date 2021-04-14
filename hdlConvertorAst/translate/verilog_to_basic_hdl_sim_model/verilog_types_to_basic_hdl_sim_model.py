
from hdlConvertorAst.hdlAst import HdlTypeBitsDef, HdlOpType, HdlOp, HdlValueId,\
    HdlTypeAuto, HdlValueInt
from hdlConvertorAst.to.basic_hdl_sim_model.utils import BitsT,\
    _verilog_slice_to_width
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_index
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.verilog_resolve_types import VerilogResolveTypes
from hdlConvertorAst.py_ver_compatibility import is_str


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
            width = _verilog_slice_to_width(t.msb, t.lsb)
            return BitsT(width, bool(t.signed))
        elif isinstance(t, HdlValueId):
            if t == HdlValueId("integer"):
                return HdlValueId("INT")
        raise NotImplementedError(t)

    def visit_HdlIdDef(self, o):
        """
        :type o: HdlIdDef
        """
        if o.type is HdlTypeAuto:
            if is_str(o.value):
                o.type = HdlValueId("STR")
                return o
            elif isinstance(o.value, HdlValueInt):
                v = o.value.val
                if isinstance(v, int) and (v <= 1 and v >= 0):
                    o.type =  HdlValueId("BIT")
                else:
                    o.type =  HdlValueId("INT")
                return o

        return VerilogResolveTypes.visit_HdlIdDef(self, o)

    def visit_type(self, t):
        """
        :type t: iHdlExpr
        """
        t = VerilogResolveTypes.visit_type(self, t)
        return self._visit_type(t)