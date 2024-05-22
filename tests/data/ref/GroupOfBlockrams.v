//
//    RAM where each port has an independet clock.
//    It can be configured to true dual port RAM etc.
//    It can also be configured to have write mask or to be composed from multiple smaller memories.
//
//    :note: write-first variant
//
//    .. hwt-autodoc::
//    
module RamMultiClock #(
    parameter ADDR_WIDTH = 8,
    parameter DATA_WIDTH = 64,
    parameter HAS_BE = 0,
    parameter INIT_DATA = "None",
    parameter MAX_BLOCK_DATA_WIDTH = "None",
    parameter PORT_CNT = 2
) (
    input wire[7:0] port_0_addr,
    input wire port_0_clk,
    input wire[63:0] port_0_din,
    output reg[63:0] port_0_dout,
    input wire port_0_en,
    input wire port_0_we,
    input wire[7:0] port_1_addr,
    input wire port_1_clk,
    input wire[63:0] port_1_din,
    output reg[63:0] port_1_dout,
    input wire port_1_en,
    input wire port_1_we
);
    reg[63:0] ram_memory[0:255];
    always @(posedge port_0_clk) begin: assig_process_port_0_dout
        if (port_0_en) begin
            if (port_0_we)
                ram_memory[port_0_addr] <= port_0_din;
            port_0_dout <= ram_memory[port_0_addr];
        end else
            port_0_dout <= 64'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
    end

    always @(posedge port_1_clk) begin: assig_process_port_1_dout
        if (port_1_en) begin
            if (port_1_we)
                ram_memory[port_1_addr] <= port_1_din;
            port_1_dout <= ram_memory[port_1_addr];
        end else
            port_1_dout <= 64'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
    end

    generate if (ADDR_WIDTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DATA_WIDTH != 64)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (HAS_BE != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (INIT_DATA != "None")
        $error("%m Generated only for this param value");
    endgenerate

    generate if (MAX_BLOCK_DATA_WIDTH != "None")
        $error("%m Generated only for this param value");
    endgenerate

    generate if (PORT_CNT != 2)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
//
//    .. hwt-autodoc::
//    
module GroupOfBlockrams #(
    parameter ADDR_WIDTH = 8,
    parameter DATA_WIDTH = 64
) (
    input wire[7:0] addr,
    input wire clk,
    input wire en,
    input wire[63:0] in_r_a,
    input wire[63:0] in_r_b,
    input wire[63:0] in_w_a,
    input wire[63:0] in_w_b,
    output wire[63:0] out_r_a,
    output wire[63:0] out_r_b,
    output wire[63:0] out_w_a,
    output wire[63:0] out_w_b,
    input wire we
);
    wire[7:0] sig_bramR_port_0_addr;
    wire sig_bramR_port_0_clk;
    wire[63:0] sig_bramR_port_0_din;
    wire[63:0] sig_bramR_port_0_dout;
    wire sig_bramR_port_0_en;
    wire sig_bramR_port_0_we;
    wire[7:0] sig_bramR_port_1_addr;
    wire sig_bramR_port_1_clk;
    wire[63:0] sig_bramR_port_1_din;
    wire[63:0] sig_bramR_port_1_dout;
    wire sig_bramR_port_1_en;
    wire sig_bramR_port_1_we;
    wire[7:0] sig_bramW_port_0_addr;
    wire sig_bramW_port_0_clk;
    wire[63:0] sig_bramW_port_0_din;
    wire[63:0] sig_bramW_port_0_dout;
    wire sig_bramW_port_0_en;
    wire sig_bramW_port_0_we;
    wire[7:0] sig_bramW_port_1_addr;
    wire sig_bramW_port_1_clk;
    wire[63:0] sig_bramW_port_1_din;
    wire[63:0] sig_bramW_port_1_dout;
    wire sig_bramW_port_1_en;
    wire sig_bramW_port_1_we;
    RamMultiClock #(
        .ADDR_WIDTH(8),
        .DATA_WIDTH(64),
        .HAS_BE(0),
        .INIT_DATA("None"),
        .MAX_BLOCK_DATA_WIDTH("None"),
        .PORT_CNT(2)
    ) bramR_inst (
        .port_0_addr(sig_bramR_port_0_addr),
        .port_0_clk(sig_bramR_port_0_clk),
        .port_0_din(sig_bramR_port_0_din),
        .port_0_dout(sig_bramR_port_0_dout),
        .port_0_en(sig_bramR_port_0_en),
        .port_0_we(sig_bramR_port_0_we),
        .port_1_addr(sig_bramR_port_1_addr),
        .port_1_clk(sig_bramR_port_1_clk),
        .port_1_din(sig_bramR_port_1_din),
        .port_1_dout(sig_bramR_port_1_dout),
        .port_1_en(sig_bramR_port_1_en),
        .port_1_we(sig_bramR_port_1_we)
    );

    RamMultiClock #(
        .ADDR_WIDTH(8),
        .DATA_WIDTH(64),
        .HAS_BE(0),
        .INIT_DATA("None"),
        .MAX_BLOCK_DATA_WIDTH("None"),
        .PORT_CNT(2)
    ) bramW_inst (
        .port_0_addr(sig_bramW_port_0_addr),
        .port_0_clk(sig_bramW_port_0_clk),
        .port_0_din(sig_bramW_port_0_din),
        .port_0_dout(sig_bramW_port_0_dout),
        .port_0_en(sig_bramW_port_0_en),
        .port_0_we(sig_bramW_port_0_we),
        .port_1_addr(sig_bramW_port_1_addr),
        .port_1_clk(sig_bramW_port_1_clk),
        .port_1_din(sig_bramW_port_1_din),
        .port_1_dout(sig_bramW_port_1_dout),
        .port_1_en(sig_bramW_port_1_en),
        .port_1_we(sig_bramW_port_1_we)
    );

    assign out_r_a = sig_bramR_port_0_dout;
    assign out_r_b = sig_bramR_port_1_dout;
    assign out_w_a = sig_bramW_port_0_dout;
    assign out_w_b = sig_bramW_port_1_dout;
    assign sig_bramR_port_0_addr = addr;
    assign sig_bramR_port_0_clk = clk;
    assign sig_bramR_port_0_din = in_r_a;
    assign sig_bramR_port_0_en = en;
    assign sig_bramR_port_0_we = we;
    assign sig_bramR_port_1_addr = addr;
    assign sig_bramR_port_1_clk = clk;
    assign sig_bramR_port_1_din = in_r_b;
    assign sig_bramR_port_1_en = en;
    assign sig_bramR_port_1_we = we;
    assign sig_bramW_port_0_addr = addr;
    assign sig_bramW_port_0_clk = clk;
    assign sig_bramW_port_0_din = in_w_a;
    assign sig_bramW_port_0_en = en;
    assign sig_bramW_port_0_we = we;
    assign sig_bramW_port_1_addr = addr;
    assign sig_bramW_port_1_clk = clk;
    assign sig_bramW_port_1_din = in_w_b;
    assign sig_bramW_port_1_en = en;
    assign sig_bramW_port_1_we = we;
    generate if (ADDR_WIDTH != 8)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (DATA_WIDTH != 64)
        $error("%m Generated only for this param value");
    endgenerate

endmodule
