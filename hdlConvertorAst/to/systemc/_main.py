from hdlConvertorAst.hdlAst import HdlIdDef, iHdlExpr, HdlOp, HdlOpType,\
    HdlDirection, HdlValueId, HdlStmProcess, HdlCompInst, HdlModuleDec,\
    HdlPhysicalDef, HdlEnumDef, HdlClassDef
from hdlConvertorAst.hdlAst._statements import ALL_STATEMENT_CLASSES
from hdlConvertorAst.to.basic_hdl_sim_model._main import ToBasicHdlSimModel
from hdlConvertorAst.to.common import ToHdlCommon
from hdlConvertorAst.to.hdlUtils import Indent, iter_with_last
from hdlConvertorAst.to.systemc.stm import ToSystemcStm
from hdlConvertorAst.hdlAst._expr import HdlTypeType
from hdlConvertorAst.to.verilog.utils import collect_array_dims
from hdlConvertorAst.py_ver_compatibility import method_as_function


DEFAULT_IMPORTS = """\
#include <systemc.h>
"""


class ToSystemc(ToSystemcStm):
    """
    Convert hdlObject AST to BasicHdlSimModel
    (Python simulation model used by pycocotb simulator)

    :ivar _is_param: flag which specifies if the current HdlIdDef is a param/generic
    :ivar _is_port: flag which specifies if the current HdlIdDef is a port
    """
    ALL_STATEMENT_CLASSES = ALL_STATEMENT_CLASSES

    def __init__(self, out_stream):
        ToHdlCommon.__init__(self, out_stream)
        self.module_path_prefix = None
        self.add_imports = True

    def visit_doc(self, obj):
        return super(ToSystemc, self).visit_doc(obj, "//")

    def visit_HdlModuleDef(self, mod_def):
        """
        :type mod_def: HdlModuleDef
        """
        mod_dec = mod_def.dec
        assert mod_dec is not None, mod_def
        assert not mod_dec.objs, mod_dec
        w = self.out.write
        w(DEFAULT_IMPORTS)
        w("\n")

        split_HdlModuleDefObjs = method_as_function(ToBasicHdlSimModel.split_HdlModuleDefObjs)
        types, variables, processes, components = \
            split_HdlModuleDefObjs(self, mod_def.objs)

        self.visit_doc(mod_dec)
        method_as_function(ToBasicHdlSimModel.visit_component_imports)(self, components)

        w("SC_MODULE(")
        w(mod_dec.name)
        w(") {\n")
        with Indent(self.out):
            if mod_dec.params:
                raise NotImplementedError()

            for t in types:
                self.visit_type_declr(t)
                w(";\n")

            w('// ports\n')
            try:
                self._is_port = True
                for p in mod_dec.ports:
                    self.visit_HdlIdDef(p)
                    w(";\n")
            finally:
                self._is_port = False

            w("// component instances\n")
            for c in components:
                w(c.module_name.val)
                w(" ")
                w(c.name.val)
                w('();\n')
            w("// internal signals\n")
            for v in variables:
                self.visit_HdlIdDef(v)
                w(";\n")

            for p in processes:
                self.visit_iHdlStatement(p)
                # extra line to separate a process functions
                w("\n")

            w("SC_CTOR(")
            w(mod_dec.name)
            w(")")
            if components:
                w(": ")
            for last, c in iter_with_last(components):
                w(c.name.val)
                w('("')
                w(c.name.val)
                if last:
                    w('")')
                else:
                    w('"), ')
            w(" {\n")
            with Indent(self.out):
                for p in processes:
                    if p.sensitivity:
                        w("SC_METHOD(")
                        w(p.labels[0])
                        w(");\n")
                        w("sensitive")
                        for s in p.sensitivity:
                            w(" << ")
                            self.visit_iHdlExpr(s)
                        w(";\n")
                    else:
                        w(p.labels[0])
                        w("();\n")
                w("// connect ports\n")
                for c in components:
                    for pm in c.port_map:
                        w(c.name.val)
                        w('.')
                        assert isinstance(pm, HdlOp) and\
                            pm.fn == HdlOpType.MAP_ASSOCIATION, pm
                        mod_port, connected_sig = pm.ops
                        assert isinstance(mod_port, HdlValueId), mod_port
                        self.visit_iHdlExpr(mod_port)
                        assert isinstance(
                            connected_sig, HdlValueId), connected_sig
                        w("(")
                        self.visit_iHdlExpr(connected_sig)
                        w(");\n")

            w("}\n")
        w("};\n")

    def visit_type_declr(self, var):
        """
        :type var: HdlIdDef
        """
        assert var.type == HdlTypeType
        self.visit_doc(var)
        w = self.out.write
        w("typedef ")
        t, arr_dims = collect_array_dims(var.value)
        with Indent(self.out):
            self.visit_iHdlExpr(t)
        w(" ")
        w(var.name)
        for d in arr_dims:
            w("[")
            self.visit_iHdlExpr(d)
            w("]")

        return True

    def visit_HdlIdDef(self, var):
        """
        :type var: HdlIdDef
        """
        self.visit_doc(var)
        w = self.out.write
        t, arr_dims = collect_array_dims(var.type)
        self.visit_type(t)
        w(" ")
        w(var.name)
        for d in arr_dims:
            w("[")
            self.visit_iHdlExpr(d)
            w("]")
        if var.value is not None:
            w(" = ")
            with Indent(self.out):
                self.visit_iHdlExpr(var.value)
        return True

    def visit_HdlClassDef(self, o):
        raise NotImplementedError()

    def visit_HdlEnumDef(self, o):
        raise NotImplementedError()

    def visit_HdlPhysicalDef(self, o):
        raise NotImplementedError()
