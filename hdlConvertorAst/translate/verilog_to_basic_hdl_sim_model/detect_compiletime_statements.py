from hdlConvertorAst.to.hdl_ast_visitor import HdlAstVisitor
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.wrap_module_statements_to_processes import collect_hdl_ids
from hdlConvertorAst.hdlAst import HdlIdDef

def all_ids_constant(expr):
    all_ids = set()
    collect_hdl_ids(expr, all_ids)
    for hid in all_ids:
        if isinstance(hid.obj, HdlIdDef) and not hid.obj.is_const:
            return False
    return True

class DetectCompileTimeStatements(HdlAstVisitor):
    """
    Mark all statements which can be resolved compiletime with a in_preproc flag

    :attentions: requires all symbols to be resolved
    """
    def visit_param(self, o):
        """
        :type o: HdlIdDef
        """
        o.is_const = True
        return o

    def visit_HdlStmCase(self, o):
        """
        :type o: HdlStmCase
        """
        if not o.in_preproc:
            o.in_preproc = all_ids_constant(o.switch_on)

        return HdlAstVisitor.visit_HdlStmCase(self, o)

    def visit_iHdlExpr(self, o):
        """
        :note: do not descend in to expressions because we do not need it
        """
        return o

    def visit_HdlStmIf(self, o):
        """
        :type o: HdlStmIf
        """
        if not o.in_preproc:
            in_preproc = True
            in_preproc &= all_ids_constant(o.cond)
            if in_preproc:
                for c, _ in o.elifs:
                    in_preproc &= all_ids_constant(c)
                    if not in_preproc:
                        break
            o.in_preproc = in_preproc

        return HdlAstVisitor.visit_HdlStmIf(self, o)