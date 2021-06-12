#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest

from hdlConvertorAst.hdlAst._expr import HdlValueId
from hdlConvertorAst.parse_hdlConvertor_json import parse_hdlConvertor_json_file
from hdlConvertorAst.to.basic_hdl_sim_model._main import ToBasicHdlSimModel
from hdlConvertorAst.to.hwt._main import ToHwt
from hdlConvertorAst.to.hwt.keywords import HWT_KEYWORDS
from hdlConvertorAst.to.systemc._main import ToSystemc
from hdlConvertorAst.to.verilog.verilog2005 import ToVerilog2005
from hdlConvertorAst.to.vhdl.vhdl2008 import ToVhdl2008
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.discover_stm_outputs\
    import discover_stm_outputs_context
from hdlConvertorAst.translate.common.discover_declarations import DiscoverDeclarations
from hdlConvertorAst.translate.common.name_scope import NameScope,\
    LanguageKeyword
from hdlConvertorAst.translate.common.resolve_names import ResolveNames
from hdlConvertorAst.translate.vhdl_to_verilog import link_module_dec_def


ROOT = os.path.join(os.path.dirname(__file__), "data")

try:
    # python2
    from StringIO import StringIO
    from io import open
except ImportError:
    # python3
    from io import StringIO


def rm_ToBasicHdlSimModel_io_prefix_and_tmp_vars_from_outputs(stm_outputs):
    C = HdlValueId("c")
    CVLD = HdlValueId("cVld")
    SELF = HdlValueId("self")
    IO = HdlValueId("io")
    VAL_NEXT = HdlValueId("val_next")
    res = {}
    for stm, outputs in stm_outputs.items():
        new_outputs = []
        for o in outputs:
            if o in (C, CVLD):
                continue
            assert o[0] == SELF, o
            assert o[1] == IO, o
            assert o[-1] == VAL_NEXT
            new_o = o[2:-1]
            if len(new_o) == 1:
                new_o = new_o[0]
            new_outputs.append(new_o)
        res[stm] = new_outputs
    return res


class FromJsonToHdlTC(unittest.TestCase):
    FILE_SUFFIX = {
        ToVerilog2005: (".Verilog.json", ".v"),
        ToVhdl2008: (".Vhdl2008.json", ".vhd"),
        ToHwt: (".hwt.json", ".hwt.py"),
        ToBasicHdlSimModel: (".sim_model.json", ".sim_model.py"),
        ToSystemc: (".systemc.json", ".cpp"),
    }

    def check_file(self, name, to_hdl_cls):
        """
        Load AST from json and convert it to target language
        and compare it with reference file
        """
        json_suffix, ref_file_suffix = self.FILE_SUFFIX[to_hdl_cls]
        d = parse_hdlConvertor_json_file(
            os.path.join(ROOT, name + json_suffix))

        buff = StringIO()
        ser = to_hdl_cls(buff)
        if to_hdl_cls is ToBasicHdlSimModel:
            # it is required to know outputs of each process
            stm_outputs = discover_stm_outputs_context(d)
            stm_outputs = rm_ToBasicHdlSimModel_io_prefix_and_tmp_vars_from_outputs(
                stm_outputs)
            ser.visit_HdlContext(d, stm_outputs)
        else:
            if to_hdl_cls is ToHwt:
                # it is required to know the direction of port connections
                link_module_dec_def(d)
                name_scope = NameScope.make_top(False)
                for kw in HWT_KEYWORDS:
                    name_scope.register_name(kw, LanguageKeyword())
                DiscoverDeclarations(name_scope).visit_HdlContext(d)
                ResolveNames(name_scope).visit_HdlContext(d)

            ser.visit_HdlContext(d)

        res_str = buff.getvalue()

        ref_file = os.path.join(ROOT, "ref", name + ref_file_suffix)
        # with open(ref_file, "w", encoding="utf-8") as f:
        #     f.write(res_str)

        with open(ref_file, encoding="utf-8") as f:
            ref = f.read()

        self.assertEqual(ref, res_str)

    def test_Showcase0_verilog(self):
        self.check_file("Showcase0", ToVerilog2005)

    def test_Showcase0_vhdl(self):
        self.check_file("Showcase0", ToVhdl2008)

    def test_Showcase0_hwt(self):
        self.check_file("Showcase0", ToHwt)

    def test_Showcase0_sim_model(self):
        self.check_file("Showcase0", ToBasicHdlSimModel)

    def test_Showcase0_systemc(self):
        self.check_file("Showcase0", ToSystemc)

    def test_GroupOfBlockrams_verilog(self):
        self.check_file("GroupOfBlockrams", ToVerilog2005)

    def test_GroupOfBlockrams_vhdl(self):
        self.check_file("GroupOfBlockrams", ToVhdl2008)

    def test_GroupOfBlockrams_hwt(self):
        self.check_file("GroupOfBlockrams", ToHwt)

    def test_GroupOfBlockrams_sim_model(self):
        self.check_file("GroupOfBlockrams", ToBasicHdlSimModel)

    def test_GroupOfBlockrams_systemc(self):
        self.check_file("GroupOfBlockrams", ToSystemc)


if __name__ == '__main__':
    unittest.main()
