from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.\
    add_unique_labels_to_all_processes import AddUniqueLabelsToAllProcesses
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model\
    .verilog_types_to_basic_hdl_sim_model import VerilogTypesToBasicHdlSimModel
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model\
    .wrap_module_statements_to_processes import wrap_module_statements_to_processes
from hdlConvertorAst.translate.common.discover_declarations import DiscoverDeclarations
from hdlConvertorAst.translate.vhdl_to_verilog import link_module_dec_def
from hdlConvertorAst.translate.common.name_scope import NameScope
from hdlConvertorAst.translate.common.resolve_names import ResolveNames
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model\
    .discover_stm_outputs import discover_stm_outputs_context
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model\
    .verilog_operands_to_basic_hdl_sim_model import BasicHdlSimModelTranslateVerilogOperands
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model\
    .assignment_to_update_assignment import AssignmentToUpdateAssignment
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.apply_io_scope_to_signal_names import ApplyIoScopeToSignalNames


def verilog_to_basic_hdl_sim_model(context):
    """
    :type context: HdlContext
    """
    link_module_dec_def(context)
    name_scope = NameScope.make_top(False)

    DiscoverDeclarations(name_scope).visit_HdlContext(context)
    ResolveNames(name_scope).visit_HdlContext(context)
    wrap_module_statements_to_processes(context)
    BasicHdlSimModelTranslateVerilogOperands().visit_HdlContext(context)
    VerilogTypesToBasicHdlSimModel().visit_HdlContext(context)
    stm_outputs = discover_stm_outputs_context(context)

    AddUniqueLabelsToAllProcesses(name_scope, stm_outputs).context(context)
    AssignmentToUpdateAssignment().visit_HdlContext(context)
    ApplyIoScopeToSignalNames().visit_HdlContext(context)

    return context, stm_outputs, name_scope
