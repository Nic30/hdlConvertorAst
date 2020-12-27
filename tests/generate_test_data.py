#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
:attention: this script is used to re-generate files for tests,
    it is mostly the documentation of origin of files
    and it is not part of the tests
    and it requires a libraries which are not installed by default
'''
import json
import os

from hdlConvertorAst.hdlAst._structural import HdlContext
from hdlConvertorAst.to.json import ToJson
from hwt.serializer.hwt import HwtSerializer
from hwt.serializer.simModel import SimModelSerializer
from hwt.serializer.store_manager import StoreManager, SaveToStream
from hwt.serializer.systemC import SystemCSerializer
from hwt.serializer.verilog import VerilogSerializer
from hwt.serializer.vhdl import Vhdl2008Serializer
from hwt.synthesizer.unit import Unit, HdlConstraintList
from hwt.synthesizer.utils import to_rtl
from hwtLib.examples.hierarchy.groupOfBlockrams import GroupOfBlockrams
from hwtLib.examples.showcase0 import Showcase0
from tests.fromJsonToHdl_test import FromJsonToHdlTC


class SaveHwtToJson(StoreManager):
    """
    Store all produced code to a json
    """

    def __init__(self,
                 to_hdl_ast,
                 _filter=None,
                 name_scope=None):

        class HwtJsonSerializerConfig():
            fileExtension = None
            TO_HDL_AST = to_hdl_ast
            TO_HDL = ToJson
            TO_CONSTRAINTS = None

        super(SaveHwtToJson, self).__init__(
            HwtJsonSerializerConfig, _filter=_filter, name_scope=name_scope)
        self.ctx = []

    def write(self, obj):
        self.as_hdl_ast.name_scope = self.name_scope
        if not isinstance(obj, HdlConstraintList):
            hdl = self.as_hdl_ast.as_hdl(obj)
            ser = self.serializer_cls.TO_HDL()
            j = ser.visit_main_obj(hdl)
            if isinstance(hdl, HdlContext):
                self.ctx.extend(j)
            else:
                self.ctx.append(j)


def hwt_to_json(u: Unit, to_hdl_ast):
    store_manager = SaveHwtToJson(to_hdl_ast)
    to_rtl(u, store_manager)
    return store_manager.ctx


HDLCONVERTOAST_TO_HWT = {
    ser.TO_HDL: ser for ser in [
        VerilogSerializer,
        Vhdl2008Serializer,
        HwtSerializer,
        SimModelSerializer,
        SystemCSerializer,
    ]
}


def generate_hwt_examples(u_cls, data_root):
    for _ser, (json_suffix, ref_file_suffix) in FromJsonToHdlTC.FILE_SUFFIX.items():
        u = u_cls()

        ser = HDLCONVERTOAST_TO_HWT[_ser]
        j = hwt_to_json(u, ser.TO_HDL_AST)
        u_name = u._name
        with open(os.path.join(data_root, f"{u_name}{json_suffix}"), "w") as f:
            json.dump(j, f, sort_keys=True, indent=1)

        u = u_cls()
        with open(os.path.join(data_root, "ref", f"{u_name}{ref_file_suffix}"), "w") as f:
            store_man = SaveToStream(ser, f)
            to_rtl(u, store_man)


if __name__ == '__main__':
    test_data_root = os.path.join(os.path.dirname(__file__), "data")
    generate_hwt_examples(Showcase0, test_data_root)
    generate_hwt_examples(GroupOfBlockrams, test_data_root)
    print("done")
