from hdlConvertorAst.hdlAst import HdlOpType, HdlOp, HdlValueId, HdlStmThrow
from hdlConvertorAst.to.hdl_ast_modifier import HdlAstModifier
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import \
    to_property_call, hdl_call, hdl_getattr, hdl_add_int


class BasicHdlSimModelTranslateVerilogOperands(HdlAstModifier):

    def visit_HdlOp(self, o):
        """
        :type o: HdlOp
        """
        o = HdlAstModifier.visit_HdlOp(self, o)
        op = o.fn
        if op == HdlOpType.EQ or op == HdlOpType.XNOR:
            # HdlOpType.EQ: '%s._eq(%s)',
            to_property_call(o, "_eq")
        elif op == HdlOpType.CONCAT:
            to_property_call(o, "_concat")
        elif op == HdlOpType.TERNARY:
            to_property_call(o, "_ternary__val")
        elif op == HdlOpType.DOWNTO:
            o.fn = HdlOpType.CALL
            o.ops = [HdlValueId("slice"), hdl_add_int(o.ops[0], 1), o.ops[1]] 
        elif op == HdlOpType.TO:
            raise NotImplementedError(o)
        elif op == HdlOpType.CALL:
            fn = o.ops[0]
            if fn == HdlValueId("$display"):
                o.ops = [HdlValueId("print"), ] + o.ops[1:]
            elif fn == HdlValueId("$finish"):
                t = HdlStmThrow()
                t.val = hdl_call(HdlValueId("Exception"), [])
                return t
            elif fn == HdlValueId("$time"):
                return hdl_getattr(HdlValueId("sim"), "now")
            else:
                raise NotImplementedError("need to inline function", o)
        elif op == HdlOpType.REPL_CONCAT:
            n, v = o.ops
            return hdl_call(HdlValueId("replicate"), [n, v])
        elif op in (HdlOpType.AND_LOG, HdlOpType.OR_LOG, HdlOpType.NEG_LOG):
            ops = [hdl_call(hdl_getattr(_o, "_isOn"), []) for _o in o.ops]
            if op == HdlOpType.AND_LOG:
                new_o_fn = HdlOpType.AND
            elif op == HdlOpType.OR_LOG:
                new_o_fn = HdlOpType.OR
            else:
                assert op == HdlOpType.NEG_LOG
                new_o_fn = HdlOpType.NEG
            return HdlOp(new_o_fn, ops)
            
        return o
