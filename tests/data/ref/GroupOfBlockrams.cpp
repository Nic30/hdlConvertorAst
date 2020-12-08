#include <systemc.h>

//
//    True dual port RAM.
//    :note: write-first variant 
//
//    .. hwt-autodoc::
//    
SC_MODULE(Ram_dp) {
    // ports
    sc_in<sc_uint<8>> a_addr;
    sc_in<sc_uint<1>> a_clk;
    sc_in<sc_uint<64>> a_din;
    sc_out<sc_uint<64>> a_dout;
    sc_in<sc_uint<1>> a_en;
    sc_in<sc_uint<1>> a_we;
    sc_in<sc_uint<8>> b_addr;
    sc_in<sc_uint<1>> b_clk;
    sc_in<sc_uint<64>> b_din;
    sc_out<sc_uint<64>> b_dout;
    sc_in<sc_uint<1>> b_en;
    sc_in<sc_uint<1>> b_we;
    // component instances
    // internal signals
    sc_uint<64> ram_memory[256];
    void assig_process_a_dout() {
        if (a_we.read() == sc_uint<1>("0b1"))
            (ram_memory[a_addr]).write(a_din.read());
        a_dout = ram_memory[a_addr.read()];
    }

    void assig_process_b_dout() {
        if (b_we.read() == sc_uint<1>("0b1"))
            (ram_memory[b_addr]).write(b_din.read());
        b_dout = ram_memory[b_addr.read()];
    }

    SC_CTOR(Ram_dp) {
        SC_METHOD(assig_process_a_dout);
        sensitive << a_clk.pos();
        SC_METHOD(assig_process_b_dout);
        sensitive << b_clk.pos();
        // connect ports
    }
};
#include <systemc.h>

//
//    .. hwt-autodoc::
//    
SC_MODULE(GroupOfBlockrams) {
    // ports
    sc_in<sc_uint<8>> addr;
    sc_in_clk clk;
    sc_in<sc_uint<1>> en;
    sc_in<sc_uint<64>> in_r_a;
    sc_in<sc_uint<64>> in_r_b;
    sc_in<sc_uint<64>> in_w_a;
    sc_in<sc_uint<64>> in_w_b;
    sc_out<sc_uint<64>> out_r_a;
    sc_out<sc_uint<64>> out_r_b;
    sc_out<sc_uint<64>> out_w_a;
    sc_out<sc_uint<64>> out_w_b;
    sc_in<sc_uint<1>> we;
    // component instances
    Ram_dp bramR_inst();
    Ram_dp bramW_inst();
    // internal signals
    sc_signal<sc_uint<8>> sig_bramR_a_addr;
    sc_signal<sc_uint<1>> sig_bramR_a_clk;
    sc_signal<sc_uint<64>> sig_bramR_a_din;
    sc_signal<sc_uint<64>> sig_bramR_a_dout;
    sc_signal<sc_uint<1>> sig_bramR_a_en;
    sc_signal<sc_uint<1>> sig_bramR_a_we;
    sc_signal<sc_uint<8>> sig_bramR_b_addr;
    sc_signal<sc_uint<1>> sig_bramR_b_clk;
    sc_signal<sc_uint<64>> sig_bramR_b_din;
    sc_signal<sc_uint<64>> sig_bramR_b_dout;
    sc_signal<sc_uint<1>> sig_bramR_b_en;
    sc_signal<sc_uint<1>> sig_bramR_b_we;
    sc_signal<sc_uint<8>> sig_bramW_a_addr;
    sc_signal<sc_uint<1>> sig_bramW_a_clk;
    sc_signal<sc_uint<64>> sig_bramW_a_din;
    sc_signal<sc_uint<64>> sig_bramW_a_dout;
    sc_signal<sc_uint<1>> sig_bramW_a_en;
    sc_signal<sc_uint<1>> sig_bramW_a_we;
    sc_signal<sc_uint<8>> sig_bramW_b_addr;
    sc_signal<sc_uint<1>> sig_bramW_b_clk;
    sc_signal<sc_uint<64>> sig_bramW_b_din;
    sc_signal<sc_uint<64>> sig_bramW_b_dout;
    sc_signal<sc_uint<1>> sig_bramW_b_en;
    sc_signal<sc_uint<1>> sig_bramW_b_we;
    void assig_process_out_r_a() {
        out_r_a.write(sig_bramR_a_dout.read());
    }

    void assig_process_out_r_b() {
        out_r_b.write(sig_bramR_b_dout.read());
    }

    void assig_process_out_w_a() {
        out_w_a.write(sig_bramW_a_dout.read());
    }

    void assig_process_out_w_b() {
        out_w_b.write(sig_bramW_b_dout.read());
    }

    void assig_process_sig_bramR_a_addr() {
        sig_bramR_a_addr.write(addr.read());
    }

    void assig_process_sig_bramR_a_clk() {
        sig_bramR_a_clk.write(clk.read());
    }

    void assig_process_sig_bramR_a_din() {
        sig_bramR_a_din.write(in_r_a.read());
    }

    void assig_process_sig_bramR_a_en() {
        sig_bramR_a_en.write(en.read());
    }

    void assig_process_sig_bramR_a_we() {
        sig_bramR_a_we.write(we.read());
    }

    void assig_process_sig_bramR_b_addr() {
        sig_bramR_b_addr.write(addr.read());
    }

    void assig_process_sig_bramR_b_clk() {
        sig_bramR_b_clk.write(clk.read());
    }

    void assig_process_sig_bramR_b_din() {
        sig_bramR_b_din.write(in_r_b.read());
    }

    void assig_process_sig_bramR_b_en() {
        sig_bramR_b_en.write(en.read());
    }

    void assig_process_sig_bramR_b_we() {
        sig_bramR_b_we.write(we.read());
    }

    void assig_process_sig_bramW_a_addr() {
        sig_bramW_a_addr.write(addr.read());
    }

    void assig_process_sig_bramW_a_clk() {
        sig_bramW_a_clk.write(clk.read());
    }

    void assig_process_sig_bramW_a_din() {
        sig_bramW_a_din.write(in_w_a.read());
    }

    void assig_process_sig_bramW_a_en() {
        sig_bramW_a_en.write(en.read());
    }

    void assig_process_sig_bramW_a_we() {
        sig_bramW_a_we.write(we.read());
    }

    void assig_process_sig_bramW_b_addr() {
        sig_bramW_b_addr.write(addr.read());
    }

    void assig_process_sig_bramW_b_clk() {
        sig_bramW_b_clk.write(clk.read());
    }

    void assig_process_sig_bramW_b_din() {
        sig_bramW_b_din.write(in_w_b.read());
    }

    void assig_process_sig_bramW_b_en() {
        sig_bramW_b_en.write(en.read());
    }

    void assig_process_sig_bramW_b_we() {
        sig_bramW_b_we.write(we.read());
    }

    SC_CTOR(GroupOfBlockrams): bramR_inst("bramR_inst"), bramW_inst("bramW_inst") {
        SC_METHOD(assig_process_out_r_a);
        sensitive << sig_bramR_a_dout;
        SC_METHOD(assig_process_out_r_b);
        sensitive << sig_bramR_b_dout;
        SC_METHOD(assig_process_out_w_a);
        sensitive << sig_bramW_a_dout;
        SC_METHOD(assig_process_out_w_b);
        sensitive << sig_bramW_b_dout;
        SC_METHOD(assig_process_sig_bramR_a_addr);
        sensitive << addr;
        SC_METHOD(assig_process_sig_bramR_a_clk);
        sensitive << clk;
        SC_METHOD(assig_process_sig_bramR_a_din);
        sensitive << in_r_a;
        SC_METHOD(assig_process_sig_bramR_a_en);
        sensitive << en;
        SC_METHOD(assig_process_sig_bramR_a_we);
        sensitive << we;
        SC_METHOD(assig_process_sig_bramR_b_addr);
        sensitive << addr;
        SC_METHOD(assig_process_sig_bramR_b_clk);
        sensitive << clk;
        SC_METHOD(assig_process_sig_bramR_b_din);
        sensitive << in_r_b;
        SC_METHOD(assig_process_sig_bramR_b_en);
        sensitive << en;
        SC_METHOD(assig_process_sig_bramR_b_we);
        sensitive << we;
        SC_METHOD(assig_process_sig_bramW_a_addr);
        sensitive << addr;
        SC_METHOD(assig_process_sig_bramW_a_clk);
        sensitive << clk;
        SC_METHOD(assig_process_sig_bramW_a_din);
        sensitive << in_w_a;
        SC_METHOD(assig_process_sig_bramW_a_en);
        sensitive << en;
        SC_METHOD(assig_process_sig_bramW_a_we);
        sensitive << we;
        SC_METHOD(assig_process_sig_bramW_b_addr);
        sensitive << addr;
        SC_METHOD(assig_process_sig_bramW_b_clk);
        sensitive << clk;
        SC_METHOD(assig_process_sig_bramW_b_din);
        sensitive << in_w_b;
        SC_METHOD(assig_process_sig_bramW_b_en);
        sensitive << en;
        SC_METHOD(assig_process_sig_bramW_b_we);
        sensitive << we;
        // connect ports
        bramR_inst.a_addr(sig_bramR_a_addr);
        bramR_inst.a_clk(sig_bramR_a_clk);
        bramR_inst.a_din(sig_bramR_a_din);
        bramR_inst.a_dout(sig_bramR_a_dout);
        bramR_inst.a_en(sig_bramR_a_en);
        bramR_inst.a_we(sig_bramR_a_we);
        bramR_inst.b_addr(sig_bramR_b_addr);
        bramR_inst.b_clk(sig_bramR_b_clk);
        bramR_inst.b_din(sig_bramR_b_din);
        bramR_inst.b_dout(sig_bramR_b_dout);
        bramR_inst.b_en(sig_bramR_b_en);
        bramR_inst.b_we(sig_bramR_b_we);
        bramW_inst.a_addr(sig_bramW_a_addr);
        bramW_inst.a_clk(sig_bramW_a_clk);
        bramW_inst.a_din(sig_bramW_a_din);
        bramW_inst.a_dout(sig_bramW_a_dout);
        bramW_inst.a_en(sig_bramW_a_en);
        bramW_inst.a_we(sig_bramW_a_we);
        bramW_inst.b_addr(sig_bramW_b_addr);
        bramW_inst.b_clk(sig_bramW_b_clk);
        bramW_inst.b_din(sig_bramW_b_din);
        bramW_inst.b_dout(sig_bramW_b_dout);
        bramW_inst.b_en(sig_bramW_b_en);
        bramW_inst.b_we(sig_bramW_b_we);
    }
};
