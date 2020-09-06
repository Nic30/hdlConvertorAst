from hdlConvertorAst.hdlAst import HdlIdDef, iHdlExpr, HdlOp, HdlOpType,\
    HdlDirection, HdlValueId, HdlStmProcess, HdlCompInst, HdlModuleDec,\
    HdlPhysicalDef, HdlEnumDef, HdlClassDef
from hdlConvertorAst.hdlAst._statements import ALL_STATEMENT_CLASSES
from hdlConvertorAst.py_ver_compatibility import method_as_function
from hdlConvertorAst.to.basic_hdl_sim_model._main import ToBasicHdlSimModel
from hdlConvertorAst.to.common import ToHdlCommon
from hdlConvertorAst.to.hdlUtils import Indent, iter_with_last
from hdlConvertorAst.to.hwt.stm import ToHwtStm


DEFAULT_IMPORTS = """\
from hwt.code import power, If, Switch, Concat
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import INT, SLICE
from hwt.hdl.types.enum import HEnum
from hwt.interfaces.std import Signal
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
"""


def pop_port_or_param_map(o):
    assert isinstance(o, HdlOp) and\
        o.fn == HdlOpType.MAP_ASSOCIATION, o
    mod_p, connected_p = o.ops
    assert isinstance(mod_p, HdlValueId), mod_p
    return mod_p, connected_p


class ToHwt(ToHwtStm):
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
        self._is_port = False
        self._is_param = False

    def visit_doc(self, obj, doc_string=False):
        if doc_string:
            doc = obj.doc
            if doc is not None:
                doc = doc.split("\n")
                w = self.out.write
                if len(doc) > 1:
                    w('"""')
                    for d in doc:
                        w(d.replace('\r', ''))
                        w("\n")
                    w('"""\n')
                else:
                    w('"')
                    if doc:
                        w(doc[0].replace('\r', ''))
                    w('"\n')
        else:
            return super(ToHwt, self).visit_doc(obj, "#")

    def add_module_exampe_serialization(self, module_name):
        w = self.out.write
        w('if __name__ == "__main__":\n')
        with Indent(self.out):
            w("from hwt.synthesizer.utils import to_rtl_str\n")
            w("u = ")
            w(module_name)
            w("()\n")
            w("print(to_rtl_str(u))\n")

    def visit_HdlModuleDef(self, mod_def):
        """
        :type mod_def: HdlModuleDef
        """
        mod_dec = mod_def.dec
        assert mod_dec is not None, mod_def
        assert not mod_dec.objs, mod_dec
        w = self.out.write
        if self.add_imports:
            w(DEFAULT_IMPORTS)
            w("\n")
            if self.module_path_prefix is None:
                self.add_imports = False

        split_HdlModuleDefObjs = method_as_function(ToBasicHdlSimModel.split_HdlModuleDefObjs)
        types, variables, processes, components = \
            split_HdlModuleDefObjs(self, mod_def.objs)

        method_as_function(ToBasicHdlSimModel.visit_component_imports)(self, components)

        w("class ")
        w(mod_dec.name)
        w("(Unit):\n")
        port_params_comp_names = []
        with Indent(self.out):
            self.visit_doc(mod_dec, doc_string=True)

            if mod_dec.params:
                w('def _config(self):\n')
                with Indent(self.out):
                    try:
                        self._is_param = True
                        for p in mod_dec.params:
                            self.visit_HdlIdDef(p)
                            port_params_comp_names.append(p.name)
                    finally:
                        self._is_param = False
                w("\n")

            w('def _declr(self):\n')
            with Indent(self.out):
                for t in types:
                    self.visit_type_declr(t)

                w('# ports\n')
                try:
                    self._is_port = True
                    for p in mod_dec.ports:
                        self.visit_HdlIdDef(p)
                        port_params_comp_names.append(p.name)
                finally:
                    self._is_port = False

                w("# component instances\n")
                for c in components:
                    if c.param_map:
                        w(c.name.val)
                        w(" = ")
                    w("self.")
                    w(c.name.val)
                    w(" = ")
                    w(c.module_name.val)
                    w('()\n')
                    port_params_comp_names.append(c.name.val)
                    for cp in c.param_map:
                        mod_p, val = pop_port_or_param_map(cp)
                        w(c.name.val)
                        w(".")
                        w(mod_p.val)
                        w(" = ")
                        self.visit_iHdlExpr(val)
                        w("\n")

                w("\n")

            w("def _impl(self):\n")
            with Indent(self.out):
                w("# internal signals\n")
                if port_params_comp_names:
                    # ports and params to locals
                    for last, name in iter_with_last(port_params_comp_names):
                        w(name)
                        if not last:
                            w(", ")
                    w(" = \\\n")
                    for last, name in iter_with_last(port_params_comp_names):
                        w("self.")
                        w(name)
                        if not last:
                            w(", ")
                    w("\n")
                for v in variables:
                    self.visit_HdlIdDef(v)

                for c in components:
                    for pm in c.port_map:
                        mod_port, connected_sig = pop_port_or_param_map(pm)
                        assert isinstance(
                            connected_sig, HdlValueId), connected_sig
                        p = mod_port.obj
                        assert p is not None, (
                            "HdlValueId to module ports "
                            "shoudl have been discovered before")
                        d = p.direction
                        assert d.name in (HdlDirection.IN.name,
                                          HdlDirection.OUT.name), d
                        is_input = d.name == HdlDirection.IN.name
                        if is_input:
                            w(c.name.val)
                            w(".")
                            self.visit_iHdlExpr(mod_port)
                            w("(")
                            self.visit_iHdlExpr(connected_sig)
                            w(")\n")
                        else:
                            self.visit_iHdlExpr(connected_sig)
                            w("(")
                            w(c.name.val)
                            w(".")
                            self.visit_iHdlExpr(mod_port)
                            w(")\n")

                for p in processes:
                    self.visit_iHdlStatement(p)
                    # extra line to separate a process functions
                    w("\n")
        # w("\n")
        # w("\n")
        # self.add_module_exampe_serialization(mod_dec.name)

    def visit_HdlIdDef(self, var):
        """
        :type var: HdlIdDef
        """
        self.visit_doc(var)
        w = self.out.write
        if self._is_port or self._is_param:
            w("self.")
        w(var.name)
        if self._is_port:
            w(" = Signal(dtype=")
            self.visit_type(var.type)
            w(")")
            if var.direction == HdlDirection.OUT:
                w("._m()\n")
            else:
                w("\n")
                assert var.direction == HdlDirection.IN, var.direction
        elif self._is_param:
            w(" = Param(")
            self.visit_iHdlExpr(var.value)
            w(")\n")
        else:
            # body signal
            w(' = self._sig(')
            with Indent(self.out):
                w('"')
                w(var.name)
                w('", ')
                self.visit_type(var.type)
            if var.value is None:
                w(")\n")
            else:
                w(", def_val=")
                self.visit_iHdlExpr(var.value)
                w(")\n")
