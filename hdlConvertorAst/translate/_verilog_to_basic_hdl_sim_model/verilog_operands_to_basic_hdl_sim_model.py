from hdlConvertorAst.hdlAst import HdlOpType, HdlOp, HdlValueId, HdlStmThrow
from hdlConvertorAst.to.hdl_ast_modifier import HdlAstModifier
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import \
    to_property_call, hdl_call


class BasicHdlSimModelTranslateVerilogOperands(HdlAstModifier):

    def visit_HdlOp(self, o):
        """
        :type o: HdlOp
        """
        o = HdlAstModifier.visit_HdlOp(self, o)
        op = o.fn
        if op == HdlOpType.EQ:
            # HdlOpType.EQ: '%s._eq(%s)',
            to_property_call(o, "_eq")
        elif op == HdlOpType.CONCAT:
            to_property_call(o, "_concat")
        elif op == HdlOpType.TERNARY:
            to_property_call(o, "_ternary__val")
        elif op == HdlOpType.DOWNTO:
            # HdlOpType.DOWNTO: "slice(%s, %s)",
            o.fn = HdlOpType.CALL
            o.ops = [HdlValueId("slice"), ] + o.ops
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
            else:
                raise NotImplementedError("need to inline function", o)

        return o
