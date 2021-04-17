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
from hdlConvertorAst.hdlAst._statements import HdlStmIf
from hdlConvertorAst.to.hdl_ast_visitor import HdlAstVisitor
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_or
from hdlConvertorAst.hdlAst import HdlAll


class InjectProcessSensToStatements(HdlAstVisitor):
    def visit_iHdlExpr(self, o):
        pass

    def visit_HdlStmProcess(self, o):
        """
        :type o: HdlStmProcess
        """
        sens = o.sensitivity
        if o.trigger_constrain is not None:
            raise NotImplementedError()
        if not sens or sens == [HdlAll, ]:
            return

        s = hdl_or(*sens)
        i = HdlStmIf()
        i.cond = s
        i.if_true = o.body
        o.body = i
