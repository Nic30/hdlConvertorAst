from hdlConvertorAst.hdlAst import HdlDirection, HdlOpType,\
    HdlOp, HdlCompInst, HdlIdDef, iHdlStatement,\
    HdlTypeAuto, HdlFunctionDef
from hdlConvertorAst.to.hdlUtils import Indent, iter_with_last
from hdlConvertorAst.to.verilog.stm import ToVerilog2005Stm


class ToVerilog2005(ToVerilog2005Stm):
    """
    Convert HdlConverotr hdlObject AST back to Verilog 2002
    """
    DIR2V = {
        HdlDirection.IN: "input",
        HdlDirection.OUT: "output",
        HdlDirection.INOUT: "inout",
    }
    def __init__(self, out_stream):
        ToVerilog2005Stm.__init__(self, out_stream)
        self._type_requires_nettype = True

    def visit_doc(self, obj):
        return super(ToVerilog2005, self).visit_doc(obj, "//")

    def visit_direction(self, d):
        """
        :type d: HdlDirection
        """
        vd = self.DIR2V[d]
        self.out.write(vd)

    def visit_generic_declr(self, g):
        """
        :type g: HdlIdDef
        """
        self.visit_doc(g)
        w = self.out.write
        w("parameter ")
        if g.type is HdlTypeAuto:
            is_array = False
        else:
            is_array = self.visit_type_first_part(g.type)
            w(" ")
        w(g.name)
        if is_array:
            self.visit_type_array_part(g.type)
        v = g.value
        if v is not None:
            w(" = ")
            self.visit_iHdlExpr(v)

    def visit_port_declr(self, p):
        """
        :type p: HdlIdDef
        """
        w = self.out.write
        self.visit_doc(p)
        self.visit_direction(p.direction)
        w(" ")

        t = p.type
        if t is HdlTypeAuto:
            w("wire ")
            is_array = False
        else:
            is_array = self.visit_type_first_part(t)
            w(" ")

        w(p.name)
        if is_array:
            self.visit_type_array_part(t)

    def visit_HdlIdDef(self, var):
        """
        :type var: HdlIdDef
        """
        self.visit_doc(var)
        name = var.name
        t = var.type
        w = self.out.write

        if var.is_const:
            w("localparam ")
            assert var.value is not None, var.name

        if t is HdlTypeAuto:
            if self._type_requires_nettype and not var.is_const:
                w("wire ")
            is_array = False
        else:
            is_array = self.visit_type_first_part(t)
            w(" ")
        w(name)
        if is_array:
            self.visit_type_array_part(t)

        if var.value is not None:
            w(" = ")
            self.visit_iHdlExpr(var.value)

        return True

    def visit_map_item(self, item):
        if isinstance(item, HdlOp)\
                and item.fn == HdlOpType.MAP_ASSOCIATION:
            w = self.out.write
            # k, v pair
            k, v = item.ops
            w(".")
            self.visit_iHdlExpr(k)
            w("(")
            self.visit_iHdlExpr(v)
            w(")")
        else:
            self.visit_iHdlExpr(item)

    def visit_map(self, map_):
        w = self.out.write
        with Indent(self.out):
            for last, m in iter_with_last(map_):
                self.visit_map_item(m)
                if last:
                    w("\n")
                else:
                    w(",\n")

    def visit_HdlCompInst(self, c):
        """
        :type c: HdlCompInst
        """
        self.visit_doc(c)
        w = self.out.write
        assert c.module_name
        self.visit_iHdlExpr(c.module_name)
        gms = c.param_map
        if gms:
            w(" #(\n")
            self.visit_map(gms)
            w(")")
        w(" ")
        w(c.name.val)
        pms = c.port_map
        if pms:
            w(" (\n")
            self.visit_map(pms)
            w(")")
        return True

    def visit_HdlFunctionDef(self, o):
        """
        :type o: HdlFunctionDef
        """
        self.visit_doc(o)
        w = self.out.write
        if o.is_task:
            w("task ")
        else:
            w("function ")
        if not o.is_static:
            w("automatic ")

        if not o.is_task:
            trnt = self._type_requires_nettype
            try:
                self._type_requires_nettype = False
                self.visit_type_first_part(o.return_t)
                self.visit_type_array_part(o.return_t)
            finally:
                self._type_requires_nettype = trnt
        if o.is_virtual or o.is_operator:
            raise NotImplementedError(o)
        if not o.is_task and o.return_t is not HdlTypeAuto:
            # because " " is already written by previous string
            w(" ")
        w(o.name)
        ps = o.params
        if ps:
            w(" (\n")
            with Indent(self.out):
                for last, p in iter_with_last(ps):
                    self.visit_port_declr(p)
                    if last:
                        w("\n")
                    else:
                        w(",\n")
            w(")")
        w(";\n")
        with Indent(self.out):
            for s in o.body:
                if isinstance(s, HdlIdDef):
                    self.visit_HdlIdDef(s)
                    w(";\n")
                elif isinstance(s, iHdlStatement):
                    need_semi = self.visit_iHdlStatement(s)
                    if need_semi:
                        w(";\n")
                    else:
                        w("\n")
                else:
                    self.visit_iHdlExpr(s)
                    w(";\n")

        if o.is_task:
            w("endtask")
        else:
            w("endfunction")

    def visit_HdlClassDef(self, o):
        raise NotImplementedError()

    def visit_HdlPhysicalDef(self, o):
        raise NotImplementedError()

    def visit_HdlEnumDef(self, o):
        raise NotImplementedError()

    def visit_HdlModuleDec(self, e):
        raise ValueError(self, "does not support a module headers without body")

    def visit_HdlModuleDef(self, a):
        """
        :type a: HdlModuleDef
        """
        mod_dec = a.dec
        assert mod_dec is not None, a
        assert not mod_dec.objs, mod_dec
        self.visit_doc(mod_dec)
        w = self.out.write
        w("module ")
        w(mod_dec.name)
        gs = mod_dec.params
        if gs:
            w(" #(\n")
            with Indent(self.out):
                for last, g in iter_with_last(gs):
                    self.visit_generic_declr(g)
                    if last:
                        w("\n")
                    else:
                        w(",\n")

            w(")")
        ps = mod_dec.ports
        if ps:
            w(" (\n")
            with Indent(self.out):
                for last, p in iter_with_last(ps):
                    self.visit_port_declr(p)
                    if last:
                        w("\n")
                    else:
                        w(",\n")
            w(")")
        w(";\n")

        w = self.out.write
        with Indent(self.out):
            for o in a.objs:
                if isinstance(o, HdlIdDef):
                    self.visit_HdlIdDef(o)
                    w(";\n")
                elif isinstance(o, HdlCompInst):
                    self.visit_HdlCompInst(o)
                    w(";\n\n")
                elif isinstance(o, iHdlStatement):
                    need_semi = self.visit_iHdlStatement(o)
                    if need_semi:
                        w(";\n")
                    else:
                        w("\n\n")
                elif isinstance(o, HdlFunctionDef):
                    self.visit_HdlFunctionDef(o)
                    w("\n\n")
                elif o is None:
                    w(";\n")
                else:
                    raise NotImplementedError(o)

        self.out.write("endmodule\n")

