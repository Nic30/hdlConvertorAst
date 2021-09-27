from hdlConvertorAst.hdlAst import HdlIdDef, iHdlExpr, HdlOp, HdlOpType, \
    HdlDirection, HdlValueId, HdlStmProcess, HdlCompInst, HdlModuleDec, \
    HdlPhysicalDef, HdlEnumDef, HdlClassDef, HdlFunctionDef, iHdlTypeDef
from hdlConvertorAst.hdlAst._statements import ALL_STATEMENT_CLASSES
from hdlConvertorAst.py_ver_compatibility import method_as_function
from hdlConvertorAst.to.basic_hdl_sim_model._main import ToBasicHdlSimModel
from hdlConvertorAst.to.common import ToHdlCommon
from hdlConvertorAst.to.hdlUtils import Indent, iter_with_last
from hdlConvertorAst.to.hwt.stm import ToHwtStm

DEFAULT_IMPORTS = """\
from hwt.code import If, Switch, Concat
from hwt.code_utils import rename_signal
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import INT, SLICE, STR, BIT, FLOAT64
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


def is_not_const(e, names_of_constants):
    """
    :param e: expression to check
    """
    if e is None:
        return False
    elif isinstance(e, HdlOp):
        for o in e.ops:
            if is_not_const(o, names_of_constants):
                return True
        return False
    elif isinstance(e, HdlValueId):
        return e.val not in names_of_constants
    return False


class ToHwt(ToHwtStm):
    """
    Convert hdlObject AST to BasicHdlSimModel
    (Python simulation model used by hwtSimApi simulator)

    :ivar _is_param: flag which specifies if the current HdlIdDef is a param/generic
    :ivar _is_port: flag which specifies if the current HdlIdDef is a port
    """
    ALL_STATEMENT_CLASSES = ALL_STATEMENT_CLASSES
    VAR_PER_LINE_LIMIT = 10
    TYPES_WHICH_CAN_BE_OMMITED = (HdlValueId("INT"), HdlValueId("STR"), HdlValueId("BOOL"), HdlValueId("FLOAT"))

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

    def ivars_to_local_vars(self, var_names):
        if var_names:
            w = self.out.write
            VAR_PER_LINE_LIMIT = self.VAR_PER_LINE_LIMIT
            # ports and params to locals
            for i, (last, name) in enumerate(iter_with_last(var_names)):
                w(name)
                if not last:
                    w(", ")
                if i % VAR_PER_LINE_LIMIT == 0 and i > 0:
                    # jump to new line to have reasonably long variable list
                    w("\\\n")
            w(" = \\\n")
            for i, (last, name) in enumerate(iter_with_last(var_names)):
                w("self.")
                w(name)
                if not last:
                    w(", ")
                if i % VAR_PER_LINE_LIMIT == 0 and i > 0:
                        # jump to new line to have reasonably long variable list
                        w("\\\n")
            w("\n")

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
        otherDefs, variables, processes, components, others = \
            split_HdlModuleDefObjs(self, mod_def.objs)

        method_as_function(ToBasicHdlSimModel.visit_component_imports)(self, components)

        w("class ")
        w(mod_dec.name)
        w("(Unit):\n")
        with Indent(self.out):
            self.visit_doc(mod_dec, doc_string=True)

            params_names = []
            if mod_dec.params:
                w('def _config(self):\n')
                with Indent(self.out):
                    try:
                        self._is_param = True
                        for p in mod_dec.params:
                            self.visit_HdlIdDef(p, None)
                            params_names.append(p.name)
                    finally:
                        self._is_param = False
                w("\n")

            types = []
            for d in otherDefs:
                if isinstance(d, HdlFunctionDef):
                    self.visit_HdlFunctionDef(d)
                elif isinstance(d, iHdlTypeDef):
                    types.append(d)
                else:
                    raise NotImplementedError(d)

            names_of_constants = set(params_names)
            port_params_comp_names = [*params_names]
            w('def _declr(self):\n')
            with Indent(self.out):
                self.ivars_to_local_vars(port_params_comp_names)
                for t in types:
                    self.visit_type_declr(t)

                w('# ports\n')
                try:
                    self._is_port = True
                    for p in mod_dec.ports:
                        self.visit_HdlIdDef(p, names_of_constants)
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
                self.ivars_to_local_vars(port_params_comp_names)
                w("# internal signals\n")
                for v in variables:
                    self.visit_HdlIdDef(v, names_of_constants)

                if others:
                    w("# others")
                    for o in others:
                        self.visit_iHdlObj(o)

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

    def visit_HdlFunctionDef(self, o):
        """
        :type o: HdlFunctionDef
        """
        w = self.out.write
        w("def ")
        w(o.name)
        w("(self")
        for p in o.params:
            w(", ")
            w(p.name)
        w("):\n")
        with Indent(self.out):
            self.visit_doc(o, doc_string=True)
            for stm in o.body:
                self.visit_iHdlStatement(stm)
                w("\n")
        w("\n")

    def visit_HdlIdDef(self, var, names_of_constants):
        """
        :type var: HdlIdDef
        """
        self.visit_doc(var)
        w = self.out.write
        if self._is_port or self._is_param:
            w("self.")
        w(var.name)
        if self._is_port:
            w(" = Signal(")
            if var.type != HdlValueId("BIT"):
                self.visit_type(var.type)
            w(")")
            if var.direction == HdlDirection.OUT:
                w("._m()\n")
            else:
                w("\n")
                assert var.direction == HdlDirection.IN, var.direction
        elif self._is_param:
            w(" = Param(")
            if var.type in self.TYPES_WHICH_CAN_BE_OMMITED:
                # ommit the type specification in the case where the type can be resolved from value type
                self.visit_iHdlExpr(var.value)
                w(")\n")
            else:
                self.visit_type(var.type)
                w(".from_py(")
                self.visit_iHdlExpr(var.value)
                w("))\n")
        elif var.is_const:
            names_of_constants.add(var.name)
            w(" = ")
            if var.type in self.TYPES_WHICH_CAN_BE_OMMITED:
                self.visit_iHdlExpr(var.value)
                w("\n")
            else:
                self.visit_type(var.type)
                w(".from_py(")
                self.visit_iHdlExpr(var.value)
                w(")\n")
        else:
            # body signal
            if var.value is not None and var.value != HdlValueId("None") and is_not_const(var.value, names_of_constants):
                w(' = rename_signal(self, ')
                self.visit_iHdlExpr(var.value)
                w(', "')
                w(var.name)
                w('")\n')
            else:
                w(' = self._sig(')
                with Indent(self.out):
                    w('"')
                    w(var.name)
                    if var.type == HdlValueId("BIT"):
                        w('"')
                    else:
                        w('", ')
                        self.visit_type(var.type)
                if var.value is None:
                    w(")\n")
                else:
                    w(", def_val=")
                    self.visit_iHdlExpr(var.value)
                    w(")\n")
