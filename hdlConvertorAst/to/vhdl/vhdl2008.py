from hdlConvertorAst.hdlAst import HdlDirection, iHdlStatement, \
    HdlIdDef, HdlModuleDec, HdlFunctionDef, HdlCompInst, \
    HdlTypeType, HdlOp, HdlOpType, HdlValueIdspace, HdlPhysicalDef, \
    HdlEnumDef, HdlTypeSubtype, HdlValueInt, HdlClassDef, HdlClassType
from hdlConvertorAst.to.hdlUtils import Indent, iter_with_last, UnIndent
from hdlConvertorAst.to.vhdl.stm import ToVhdl2008Stm


class ToVhdl2008(ToVhdl2008Stm):
    """
    Convert hdlObject AST back to VHDL
    """
    DIR2V = {
        HdlDirection.IN: "IN",
        HdlDirection.OUT: "OUT",
        HdlDirection.INOUT: "INOUT",
    }

    def __init__(self, out_stream):
        ToVhdl2008Stm.__init__(self, out_stream)
        self.in_typedef = False

    def visit_doc(self, obj):
        return super(ToVhdl2008, self).visit_doc(obj, "--")

    def visit_direction(self, d):
        vd = self.DIR2V[d]
        self.out.write(vd)

    def visit_main_obj(self, o):
        ToVhdl2008Stm.visit_main_obj(self, o)
        add_nl = isinstance(o, (HdlModuleDec, HdlModuleDec, HdlValueIdspace))
        if add_nl:
            self.out.write("\n")

    def visit_param_or_port_declr(self, o, is_param):
        """
        :type p: HdlIdDef
        """
        self.visit_doc(o)
        w = self.out.write
        w(o.name)
        w(" : ")
        if not is_param:
            d = o.direction
            if d != HdlDirection.INTERNAL:
                self.visit_direction(d)
                w(" ")
        self.visit_type(o.type)
        v = o.value
        if v is not None:
            w(" := ")
            self.visit_iHdlExpr(v)

    def visit_HdlModuleDec(self, e, vhdl_obj_name="ENTITY"):
        """
        :param e: Entity
        :type e: HdlModuleDec
        """
        self.visit_doc(e)
        w = self.out.write
        w(vhdl_obj_name)
        w(" ")
        w(e.name)
        w(" IS\n")
        gs = e.params
        if gs:
            with Indent(self.out):
                w("GENERIC(\n")
                with Indent(self.out):
                    for last, g in iter_with_last(gs):
                        self.visit_param_or_port_declr(g, True)
                        if last:
                            w("\n")
                        else:
                            w(";\n")

                w(");\n")
        ps = e.ports
        if ps:
            with Indent(self.out):
                w("PORT(\n")
                with Indent(self.out):
                    for last, p in iter_with_last(ps):
                        self.visit_param_or_port_declr(p, False)
                        if last:
                            w("\n")
                        else:
                            w(";\n")
                w(");\n")
        di = e.objs
        if di:
            with Indent(self.out):
                for o in di:
                    self.visit_iHdlObj(o)
        w("END ")
        w(vhdl_obj_name)
        w(";\n")

    def visit_component(self, o):
        """
        :type o: HdlModuleDec
        """
        self.visit_HdlModuleDec(o, vhdl_obj_name="COMPONENT")

    def visit_type(self, t):
        """
        :type t: iHdlExpr
        """
        self.visit_iHdlExpr(t)

    def visit_map_item(self, item):
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
        w(c.name.val)
        w(": ")
        self.visit_iHdlExpr(c.module_name)
        gms = c.param_map
        if gms:
            w(" GENERIC MAP(\n")
            self.visit_map(gms)
            w(")")

        pms = c.port_map
        if pms:
            w(" PORT MAP(\n")
            self.visit_map(pms)
            w(")")
        w(";")

    def visit_body_items(self, objs):
        w = self.out.write
        in_def_section = True
        with Indent(self.out):
            for o in objs:
                if isinstance(o, HdlIdDef):
                    assert in_def_section, o
                    self.visit_HdlIdDef(o)
                    continue
                elif isinstance(o, HdlModuleDec):
                    assert in_def_section, o
                    self.visit_component(o)
                    continue
                elif isinstance(o, HdlFunctionDef):
                    assert in_def_section, o
                    self.visit_HdlFunctionDef(o)
                    continue

                if in_def_section:
                    with UnIndent(self.out):
                        w("BEGIN\n")
                    in_def_section = False

                if isinstance(o, HdlCompInst):
                    self.visit_HdlCompInst(o)
                    w("\n")
                elif isinstance(o, iHdlStatement):
                    self.visit_iHdlStatement(o)
                elif isinstance(o, HdlOp) and o.fn == HdlOpType.CALL:
                    self.visit_HdlOp(o)
                    w(";\n")
                else:
                    raise NotImplementedError(o)
        if in_def_section:
            w("BEGIN\n")

    def visit_HdlModuleDef(self, o):
        """
        :type o: HdlModuleDef
        """
        w = self.out.write
        if o.dec is not None:
            self.visit_HdlModuleDec(o.dec)
            w("\n")
        self.visit_doc(o)
        w("ARCHITECTURE ")
        w(o.name)
        w(" OF ")
        w(o.module_name.val)
        w(" IS\n")
        self.visit_body_items(o.objs)
        self.out.write("END ARCHITECTURE;\n")

    def visit_HdlIdDef(self, var, end=";\n"):
        """
        :type var: HdlIdDef
        """
        self.visit_doc(var)
        w = self.out.write
        name = var.name
        t = var.type
        if t == HdlTypeType:
            orig_in_typedef = self.in_typedef
            try:
                self.in_typedef = True
                # typedef
                w("TYPE ")
                w(name)
                w(" IS ")
                _t = var.value
                if isinstance(_t, HdlEnumDef):
                    self.visit_HdlEnumDef(_t)
                elif isinstance(_t, HdlOp):
                    if _t.fn == HdlOpType.INDEX:
                        w("ARRAY (")
                        for last, i in iter_with_last(_t.ops[1:]):
                            self.visit_iHdlExpr(i)
                            if not last:
                                w(", ")
                        w(") OF ")
                        self.visit_iHdlExpr(_t.ops[0])
                    elif _t.fn == HdlOpType.RANGE:
                        w("RANGE ")
                        assert len(_t.ops) == 1, _t.ops
                        self.visit_iHdlExpr(_t.ops[0])
                    else:
                        raise NotImplementedError(_t.fn)

                elif isinstance(_t, HdlClassDef):
                    self.visit_HdlClassDef(_t)
                elif isinstance(_t, HdlPhysicalDef):
                    self.visit_HdlPhysicalDef(_t)
                else:
                    raise NotImplementedError(type(_t))
            finally:
                self.in_typedef = orig_in_typedef
        elif t == HdlTypeSubtype:
            orig_in_typedef = self.in_typedef
            try:
                self.in_typedef = True
                w("SUBTYPE ")
                w(name)
                w(" IS ")
                self.visit_iHdlExpr(var.value)
            finally:
                self.in_typedef = orig_in_typedef
        else:
            # signal/variable/port/generic
            if not self.in_typedef:
                latch = var.is_latched
                c = var.is_const
                if c:
                    w("CONSTANT ")
                elif latch:
                    w("VARIABLE ")
                else:
                    w("SIGNAL ")
            w(name)
            w(" : ")
            self.visit_type(t)
            v = var.value
            if v is not None:
                w(" := ")
                self.visit_iHdlExpr(v)
        w(end)

    def visit_HdlClassDef(self, o):
        """
        :type o: HdlClassDef
        """
        w = self.out.write
        assert o.type == HdlClassType.STRUCT, o.type
        w("RECORD\n")
        with Indent(self.out):
            for m in o.members:
                self.visit_HdlIdDef(m)
        w("END RECORD")

    def visit_HdlPhysicalDef(self, o):
        """
        :type o: HdlPhysicalDef
        """
        w = self.out.write
        self.visit_HdlOp(o.range)
        w("\n")
        with Indent(self.out):
            w("UNITS\n")
            with Indent(self.out):
                for k, v in o.members:
                    w(k)
                    if v is not None:
                        w(" = ")
                        self.visit_HdlOp(v)
                    w(";\n")
            w("END UNITS")

    def visit_HdlEnumDef(self, o):
        """
        :type o: HdlEnumDef
        """
        w = self.out.write
        w('(')
        for last, ev in iter_with_last(o.values):
            k, v = ev
            if k is not None:
                w(k)
            else:
                assert isinstance(v, HdlValueInt) and v.base == 256, v
                self.visit_HdlValueInt(v)

            if not last:
                w(", ")
        w(")")
        
    def visit_HdlFunctionDef(self, o):
        """
        :type o: HdlFunctionDef
        """
        self.visit_doc(o)
        w = self.out.write
        is_procedure = o.return_t is None
        if is_procedure:
            w("PROCEDURE ")
        else:
            w("FUNCTION ")

        w(o.name)

        w(" (")
        with Indent(self.out):
            for is_last, par in iter_with_last(o.params):
                self.visit_HdlIdDef(par, end="")
                if not is_last:
                    w(";\n")
        w(")")
        if not is_procedure:
            w(" RETURN ")
            self.visit_type(o.return_t)
        if o.is_declaration_only:
            w(";\n")
        else:
            w("\n")
            w("IS\n")
            self.visit_body_items(o.body)
            if is_procedure:
                w("END PROCEDURE;\n")
            else:
                w("END FUNCTION;\n")

    def visit_HdlLibrary(self, o):
        """
        :type o: HdlLibrary
        """
        self.visit_doc(o)
        w = self.out.write
        w("LIBRARY ")
        w(o.name)
        w(";\n")

    def visit_HdlImport(self, o):
        """
        :type o: HdlImport
        """
        self.visit_doc(o)
        w = self.out.write
        w("USE ")
        for last, p in iter_with_last(o.path):
            self.visit_iHdlExpr(p)
            if not last:
                w(".")
        w(";\n")

    def visit_HdlValueIdspace(self, o):
        """
        :type o: HdlValueIdspace
        """
        self.visit_doc(o)
        w = self.out.write
        # TODO:: if o.declaration_only:
        w("PACKAGE ")
        w(o.name)
        w(" IS\n")
        with Indent(self.out):
            for _o in o.objs:
                self.visit_main_obj(_o)

        w("END PACKAGE;\n")

