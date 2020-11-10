
from hdlConvertorAst.hdlAst import HdlTypeBitsDef
from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlTypeAuto
from hdlConvertorAst.to.hdl_ast_visitor import HdlAstVisitor
from hdlConvertorAst.to.verilog.utils import collect_array_dims, get_wire_t_params
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_index


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
            self.visit_iHdlExr(o.value)

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
            base_t, width, is_signed, _ = wire_params
            if width is None:
                width = 1
            t = HdlTypeBitsDef(width, is_signed)

        for i in array_dims:
            t = hdl_index(t, i)

        return t
