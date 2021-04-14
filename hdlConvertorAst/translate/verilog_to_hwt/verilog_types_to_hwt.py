from typing import Union

from hdlConvertorAst.hdlAst import HdlOp, HdlOpType, iHdlTypeDef, iHdlExpr, \
    HdlTypeBitsDef, HdlValueId, HdlIdDef
from hdlConvertorAst.to.basic_hdl_sim_model.utils import _verilog_slice_to_width
from hdlConvertorAst.to.hwt.utils import BitsT
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_index
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.verilog_types_to_basic_hdl_sim_model import VerilogTypesToBasicHdlSimModel


class VerilogTypesToHwt(VerilogTypesToBasicHdlSimModel):

    def visit_HdlModuleDef(self, o):
        """
        Remove genvar instances as they do not need forward declarations

        :type o: HdlModuleDef
        """
        genvar = HdlValueId("genvar")
        o.objs = [_o for _o in o.objs if not isinstance(_o, HdlIdDef) or _o.type != genvar ]
        super(VerilogTypesToHwt, self).visit_HdlModuleDef(o)
        return o

    def _visit_type(self, t):
        """
        :type t: Union[iHdlExpr, iHdlTypeDef]
        """
        if isinstance(t, HdlOp) and t.fn == HdlOpType.INDEX:
            o0, o1 = t.ops
            return hdl_index(self._visit_type(o0), o1)
        elif isinstance(t, HdlTypeBitsDef):
            width = _verilog_slice_to_width(t.msb, t.lsb)
            if width == 1:
                return HdlValueId("BIT")
            return BitsT(width, t.signed)
        elif isinstance(t, HdlValueId):
            if t == HdlValueId("integer"):
                return HdlValueId("INT")
            elif t == HdlValueId("real"):
                return HdlValueId("FLOAT64")
            elif t == HdlValueId("time"):
                return HdlValueId("int")
        raise NotImplementedError(t)
