#from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model\
#    .wrap_module_statements_to_processes import wrap_module_statements_to_processes
from hdlConvertorAst.translate.common.discover_declarations import DiscoverDeclarations
from hdlConvertorAst.translate.vhdl_to_verilog import link_module_dec_def
from hdlConvertorAst.translate.common.name_scope import NameScope
from hdlConvertorAst.translate.common.resolve_names import ResolveNames
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model\
    .verilog_operands_to_basic_hdl_sim_model import BasicHdlSimModelTranslateVerilogOperands
from hdlConvertorAst.translate._verilog_to_vhdl.inject_process_sens_to_statements import InjectProcessSensToStatements
from hdlConvertorAst.translate._verilog_to_hwt.verilog_types_to_hwt import VerilogTypesToHwt


def verilog_to_hwt(context):
    """
    :type context: HdlContext
    """
    link_module_dec_def(context)
    name_scope = NameScope.make_top(False)

    DiscoverDeclarations(name_scope).visit_HdlContext(context)
    ResolveNames(name_scope).visit_HdlContext(context)
    #wrap_module_statements_to_processes(context)
    InjectProcessSensToStatements().visit_HdlContext(context)
    BasicHdlSimModelTranslateVerilogOperands().visit_HdlContext(context)
    VerilogTypesToHwt().visit_HdlContext(context)

    return context, name_scope
