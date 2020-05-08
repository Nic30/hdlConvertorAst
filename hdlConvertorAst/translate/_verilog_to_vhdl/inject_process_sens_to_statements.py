"""
.. code-block:: verilog

    // sync reset
    always @(posedge clk) begin
       if(reset)
          reg <= 0;
       else
          reg <= reg_next;
    end
    //-->
    if(clk.rising_edge())
       if(reset)
          reg <= 0;
       else
          reg <= reg_next;
    // async reset
    always @(posedge clk, posedge reset) begin
        if(reset == 1'b1)
           reg <= 0;
        else
           reg <= reg_next;
    end
    -->
    if(reset == 1'b1)
       reg <= 0;
    else if(clk.rising_endge())
       reg <= reg_next;
    // latch
    always @(enable, clk) begin
        if(!clk)
           en_out = enable
    end
    -->
    if(!clk)
       en_out = enable
    // comb. logic
    always @(sel, a, b)
      begin
        f = b;
        if (sel == 1)
          f = a;
      end
    -->
    begin
      f = b;
      if (sel == 1)
        f = a;
    end
    // same with always_*
    always_ff @(negedge clk)
        latch_update_en <= next_latch_update_en;
    always_comb
        gated_clk = clk & latch_update_en;
    always_latch
        if(gated_clk)
             latch_data <= new_data;
"""
from hdlConvertorAst.to.hdl_ast_visitor import HdlAstVisitor
from hdlConvertorAst.hdlAst._expr import HdlOp, HdlOpType
from hdlConvertorAst.hdlAst._statements import HdlStmIf

class InjectProcessSensToStatements(HdlAstVisitor):

    def visit_HdlStmProcess(self, o):
        """
        :type o: HdlStmProcess
        """
        sens = o.sensitivity
        if sens:
            if len(sens) == 1:
                s = sens[0]
                if isinstance(s, HdlOp):
                    assert s.fn in [HdlOpType.RISING, HdlOpType.FALLING], s
                    i = HdlStmIf()
                    i.cond = s
                    i.if_true = o.body
                    o.body = i
                else:
                    raise NotImplementedError()
            else:
                raise NotImplementedError()
