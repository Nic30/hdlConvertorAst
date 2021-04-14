
from hdlConvertorAst.hdlAst import HdlTypeBitsDef, HdlOp, HdlOpType, HdlValueId
from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlTypeAuto
from hdlConvertorAst.to.hdl_ast_visitor import HdlAstVisitor
from hdlConvertorAst.to.verilog.utils import collect_array_dims, get_wire_t_params
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_index, \
    hdl_sub_int


class VerilogResolveTypes(HdlAstVisitor):
    """
    Translate Verilog HDL types to BasicHdlSimModel HDL types
    """
    def visit_HdlIdDef(self, o):
        """
        :type o: HdlIdDef
        """
        o.type = self.visit_type(o.type)
        if o.value is not None:
            self.visit_iHdlExpr(o.value)

    def visit_type(self, t):
        """
        :type t: iHdlExpr
        """
        t, array_dims = collect_array_dims(t)
        wire_params = get_wire_t_params(t)
        if wire_params is None:
            if t == HdlTypeAuto:
                t = HdlTypeBitsDef(1)
        else:
            base_t, msb, is_signed, _ = wire_params
            lsb = 0
            if msb is None:
                msb = 0
            elif isinstance(msb, HdlOp):
                if msb.fn == HdlOpType.DOWNTO:
                    msb, lsb = msb.ops
                elif msb.fn == HdlOpType.TO:
                    lsb, msb = msb.ops
                elif msb.fn == HdlOpType.CALL and msb.ops[0] == HdlValueId("slice"):
                    lsb = msb.ops[2]
                    msb = hdl_sub_int(msb.ops[1], 1)

            t = HdlTypeBitsDef(msb, lsb=lsb, signed=is_signed)

        for i in array_dims:
            t = hdl_index(t, i)

        return t
