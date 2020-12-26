//
//    True dual port RAM.
//    :note: write-first variant 
//
//    .. hwt-autodoc::
//    
module Ram_dp #(
    parameter ADDR_WIDTH = 8,
    parameter DATA_WIDTH = 64
) (
    input wire[7:0] a_addr,
    input wire a_clk,
    input wire[63:0] a_din,
    output reg[63:0] a_dout,
    input wire a_en,
    input wire a_we,
    input wire[7:0] b_addr,
    input wire b_clk,
    input wire[63:0] b_din,
    output reg[63:0] b_dout,
    input wire b_en,
    input wire b_we
);
    reg[63:0] ram_memory[0:255];
    always @(posedge a_clk) begin: assig_process_a_dout
        if (a_we)
            ram_memory[a_addr] <= a_din;
        a_dout <= ram_memory[a_addr];
    end

    always @(posedge b_clk) begin: assig_process_b_dout
        if (b_we)
            ram_memory[b_addr] <= b_din;
        b_dout <= ram_memory[b_addr];
    end

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
    wire[7:0] sig_bramR_a_addr = 8'bxxxxxxxx;
    wire sig_bramR_a_clk = 1'bx;
    wire[63:0] sig_bramR_a_din = 64'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
    wire[63:0] sig_bramR_a_dout = 64'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
    wire sig_bramR_a_en = 1'bx;
    wire sig_bramR_a_we = 1'bx;
    wire[7:0] sig_bramR_b_addr = 8'bxxxxxxxx;
    wire sig_bramR_b_clk = 1'bx;
    wire[63:0] sig_bramR_b_din = 64'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
    wire[63:0] sig_bramR_b_dout = 64'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
    wire sig_bramR_b_en = 1'bx;
    wire sig_bramR_b_we = 1'bx;
    wire[7:0] sig_bramW_a_addr = 8'bxxxxxxxx;
    wire sig_bramW_a_clk = 1'bx;
    wire[63:0] sig_bramW_a_din = 64'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
    wire[63:0] sig_bramW_a_dout = 64'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
    wire sig_bramW_a_en = 1'bx;
    wire sig_bramW_a_we = 1'bx;
    wire[7:0] sig_bramW_b_addr = 8'bxxxxxxxx;
    wire sig_bramW_b_clk = 1'bx;
    wire[63:0] sig_bramW_b_din = 64'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
    wire[63:0] sig_bramW_b_dout = 64'bxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx;
    wire sig_bramW_b_en = 1'bx;
    wire sig_bramW_b_we = 1'bx;
    Ram_dp #(
        .ADDR_WIDTH(8),
        .DATA_WIDTH(64)
    ) bramR_inst (
        .a_addr(sig_bramR_a_addr),
        .a_clk(sig_bramR_a_clk),
        .a_din(sig_bramR_a_din),
        .a_dout(sig_bramR_a_dout),
        .a_en(sig_bramR_a_en),
        .a_we(sig_bramR_a_we),
        .b_addr(sig_bramR_b_addr),
        .b_clk(sig_bramR_b_clk),
        .b_din(sig_bramR_b_din),
        .b_dout(sig_bramR_b_dout),
        .b_en(sig_bramR_b_en),
        .b_we(sig_bramR_b_we)
    );

    Ram_dp #(
        .ADDR_WIDTH(8),
        .DATA_WIDTH(64)
    ) bramW_inst (
        .a_addr(sig_bramW_a_addr),
        .a_clk(sig_bramW_a_clk),
        .a_din(sig_bramW_a_din),
        .a_dout(sig_bramW_a_dout),
        .a_en(sig_bramW_a_en),
        .a_we(sig_bramW_a_we),
        .b_addr(sig_bramW_b_addr),
        .b_clk(sig_bramW_b_clk),
        .b_din(sig_bramW_b_din),
        .b_dout(sig_bramW_b_dout),
        .b_en(sig_bramW_b_en),
        .b_we(sig_bramW_b_we)
    );

    assign out_r_a = sig_bramR_a_dout;
    assign out_r_b = sig_bramR_b_dout;
    assign out_w_a = sig_bramW_a_dout;
    assign out_w_b = sig_bramW_b_dout;
    assign sig_bramR_a_addr = addr;
    assign sig_bramR_a_clk = clk;
    assign sig_bramR_a_din = in_r_a;
    assign sig_bramR_a_en = en;
    assign sig_bramR_a_we = we;
    assign sig_bramR_b_addr = addr;
    assign sig_bramR_b_clk = clk;
    assign sig_bramR_b_din = in_r_b;
    assign sig_bramR_b_en = en;
    assign sig_bramR_b_we = we;
    assign sig_bramW_a_addr = addr;
    assign sig_bramW_a_clk = clk;
    assign sig_bramW_a_din = in_w_a;
    assign sig_bramW_a_en = en;
    assign sig_bramW_a_we = we;
    assign sig_bramW_b_addr = addr;
    assign sig_bramW_b_clk = clk;
    assign sig_bramW_b_din = in_w_b;
    assign sig_bramW_b_en = en;
    assign sig_bramW_b_we = we;
endmodule
