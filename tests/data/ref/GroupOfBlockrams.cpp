#include <systemc.h>

//
//    RAM where each port has an independet clock.
//    It can be configured to true dual port RAM etc.
//    It can also be configured to have write mask or to be composed from multiple smaller memories.
//
//    :note: write-first variant
//
//    .. hwt-autodoc::
//    
SC_MODULE(RamMultiClock) {
    // ports
    sc_in<sc_uint<8>> port_0_addr;
    sc_in<sc_uint<1>> port_0_clk;
    sc_in<sc_uint<64>> port_0_din;
    sc_out<sc_uint<64>> port_0_dout;
    sc_in<sc_uint<1>> port_0_en;
    sc_in<sc_uint<1>> port_0_we;
    sc_in<sc_uint<8>> port_1_addr;
    sc_in<sc_uint<1>> port_1_clk;
    sc_in<sc_uint<64>> port_1_din;
    sc_out<sc_uint<64>> port_1_dout;
    sc_in<sc_uint<1>> port_1_en;
    sc_in<sc_uint<1>> port_1_we;
    // component instances
    // internal signals
    sc_uint<64> ram_memory[256];
    void assig_process_port_0_dout() {
        if (port_0_en.read() == sc_uint<1>("0b1")) {
            if (port_0_we.read() == sc_uint<1>("0b1"))
                (ram_memory[port_0_addr]).write(port_0_din.read());
            port_0_dout = ram_memory[port_0_addr.read()];
        } else
            port_0_dout = sc_uint<64>("0bXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX");
    }

    void assig_process_port_1_dout() {
        if (port_1_en.read() == sc_uint<1>("0b1")) {
            if (port_1_we.read() == sc_uint<1>("0b1"))
                (ram_memory[port_1_addr]).write(port_1_din.read());
            port_1_dout = ram_memory[port_1_addr.read()];
        } else
            port_1_dout = sc_uint<64>("0bXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX");
    }

    SC_CTOR(RamMultiClock) {
        SC_METHOD(assig_process_port_0_dout);
        sensitive << port_0_clk.pos();
        SC_METHOD(assig_process_port_1_dout);
        sensitive << port_1_clk.pos();
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
    RamMultiClock bramR_inst();
    RamMultiClock bramW_inst();
    // internal signals
    sc_signal<sc_uint<8>> sig_bramR_port_0_addr;
    sc_signal<sc_uint<1>> sig_bramR_port_0_clk;
    sc_signal<sc_uint<64>> sig_bramR_port_0_din;
    sc_signal<sc_uint<64>> sig_bramR_port_0_dout;
    sc_signal<sc_uint<1>> sig_bramR_port_0_en;
    sc_signal<sc_uint<1>> sig_bramR_port_0_we;
    sc_signal<sc_uint<8>> sig_bramR_port_1_addr;
    sc_signal<sc_uint<1>> sig_bramR_port_1_clk;
    sc_signal<sc_uint<64>> sig_bramR_port_1_din;
    sc_signal<sc_uint<64>> sig_bramR_port_1_dout;
    sc_signal<sc_uint<1>> sig_bramR_port_1_en;
    sc_signal<sc_uint<1>> sig_bramR_port_1_we;
    sc_signal<sc_uint<8>> sig_bramW_port_0_addr;
    sc_signal<sc_uint<1>> sig_bramW_port_0_clk;
    sc_signal<sc_uint<64>> sig_bramW_port_0_din;
    sc_signal<sc_uint<64>> sig_bramW_port_0_dout;
    sc_signal<sc_uint<1>> sig_bramW_port_0_en;
    sc_signal<sc_uint<1>> sig_bramW_port_0_we;
    sc_signal<sc_uint<8>> sig_bramW_port_1_addr;
    sc_signal<sc_uint<1>> sig_bramW_port_1_clk;
    sc_signal<sc_uint<64>> sig_bramW_port_1_din;
    sc_signal<sc_uint<64>> sig_bramW_port_1_dout;
    sc_signal<sc_uint<1>> sig_bramW_port_1_en;
    sc_signal<sc_uint<1>> sig_bramW_port_1_we;
    void assig_process_out_r_a() {
        out_r_a.write(sig_bramR_port_0_dout.read());
    }

    void assig_process_out_r_b() {
        out_r_b.write(sig_bramR_port_1_dout.read());
    }

    void assig_process_out_w_a() {
        out_w_a.write(sig_bramW_port_0_dout.read());
    }

    void assig_process_out_w_b() {
        out_w_b.write(sig_bramW_port_1_dout.read());
    }

    void assig_process_sig_bramR_port_0_addr() {
        sig_bramR_port_0_addr.write(addr.read());
    }

    void assig_process_sig_bramR_port_0_clk() {
        sig_bramR_port_0_clk.write(clk.read());
    }

    void assig_process_sig_bramR_port_0_din() {
        sig_bramR_port_0_din.write(in_r_a.read());
    }

    void assig_process_sig_bramR_port_0_en() {
        sig_bramR_port_0_en.write(en.read());
    }

    void assig_process_sig_bramR_port_0_we() {
        sig_bramR_port_0_we.write(we.read());
    }

    void assig_process_sig_bramR_port_1_addr() {
        sig_bramR_port_1_addr.write(addr.read());
    }

    void assig_process_sig_bramR_port_1_clk() {
        sig_bramR_port_1_clk.write(clk.read());
    }

    void assig_process_sig_bramR_port_1_din() {
        sig_bramR_port_1_din.write(in_r_b.read());
    }

    void assig_process_sig_bramR_port_1_en() {
        sig_bramR_port_1_en.write(en.read());
    }

    void assig_process_sig_bramR_port_1_we() {
        sig_bramR_port_1_we.write(we.read());
    }

    void assig_process_sig_bramW_port_0_addr() {
        sig_bramW_port_0_addr.write(addr.read());
    }

    void assig_process_sig_bramW_port_0_clk() {
        sig_bramW_port_0_clk.write(clk.read());
    }

    void assig_process_sig_bramW_port_0_din() {
        sig_bramW_port_0_din.write(in_w_a.read());
    }

    void assig_process_sig_bramW_port_0_en() {
        sig_bramW_port_0_en.write(en.read());
    }

    void assig_process_sig_bramW_port_0_we() {
        sig_bramW_port_0_we.write(we.read());
    }

    void assig_process_sig_bramW_port_1_addr() {
        sig_bramW_port_1_addr.write(addr.read());
    }

    void assig_process_sig_bramW_port_1_clk() {
        sig_bramW_port_1_clk.write(clk.read());
    }

    void assig_process_sig_bramW_port_1_din() {
        sig_bramW_port_1_din.write(in_w_b.read());
    }

    void assig_process_sig_bramW_port_1_en() {
        sig_bramW_port_1_en.write(en.read());
    }

    void assig_process_sig_bramW_port_1_we() {
        sig_bramW_port_1_we.write(we.read());
    }

    SC_CTOR(GroupOfBlockrams): bramR_inst("bramR_inst"), bramW_inst("bramW_inst") {
        SC_METHOD(assig_process_out_r_a);
        sensitive << sig_bramR_port_0_dout;
        SC_METHOD(assig_process_out_r_b);
        sensitive << sig_bramR_port_1_dout;
        SC_METHOD(assig_process_out_w_a);
        sensitive << sig_bramW_port_0_dout;
        SC_METHOD(assig_process_out_w_b);
        sensitive << sig_bramW_port_1_dout;
        SC_METHOD(assig_process_sig_bramR_port_0_addr);
        sensitive << addr;
        SC_METHOD(assig_process_sig_bramR_port_0_clk);
        sensitive << clk;
        SC_METHOD(assig_process_sig_bramR_port_0_din);
        sensitive << in_r_a;
        SC_METHOD(assig_process_sig_bramR_port_0_en);
        sensitive << en;
        SC_METHOD(assig_process_sig_bramR_port_0_we);
        sensitive << we;
        SC_METHOD(assig_process_sig_bramR_port_1_addr);
        sensitive << addr;
        SC_METHOD(assig_process_sig_bramR_port_1_clk);
        sensitive << clk;
        SC_METHOD(assig_process_sig_bramR_port_1_din);
        sensitive << in_r_b;
        SC_METHOD(assig_process_sig_bramR_port_1_en);
        sensitive << en;
        SC_METHOD(assig_process_sig_bramR_port_1_we);
        sensitive << we;
        SC_METHOD(assig_process_sig_bramW_port_0_addr);
        sensitive << addr;
        SC_METHOD(assig_process_sig_bramW_port_0_clk);
        sensitive << clk;
        SC_METHOD(assig_process_sig_bramW_port_0_din);
        sensitive << in_w_a;
        SC_METHOD(assig_process_sig_bramW_port_0_en);
        sensitive << en;
        SC_METHOD(assig_process_sig_bramW_port_0_we);
        sensitive << we;
        SC_METHOD(assig_process_sig_bramW_port_1_addr);
        sensitive << addr;
        SC_METHOD(assig_process_sig_bramW_port_1_clk);
        sensitive << clk;
        SC_METHOD(assig_process_sig_bramW_port_1_din);
        sensitive << in_w_b;
        SC_METHOD(assig_process_sig_bramW_port_1_en);
        sensitive << en;
        SC_METHOD(assig_process_sig_bramW_port_1_we);
        sensitive << we;
        // connect ports
        bramR_inst.port_0_addr(sig_bramR_port_0_addr);
        bramR_inst.port_0_clk(sig_bramR_port_0_clk);
        bramR_inst.port_0_din(sig_bramR_port_0_din);
        bramR_inst.port_0_dout(sig_bramR_port_0_dout);
        bramR_inst.port_0_en(sig_bramR_port_0_en);
        bramR_inst.port_0_we(sig_bramR_port_0_we);
        bramR_inst.port_1_addr(sig_bramR_port_1_addr);
        bramR_inst.port_1_clk(sig_bramR_port_1_clk);
        bramR_inst.port_1_din(sig_bramR_port_1_din);
        bramR_inst.port_1_dout(sig_bramR_port_1_dout);
        bramR_inst.port_1_en(sig_bramR_port_1_en);
        bramR_inst.port_1_we(sig_bramR_port_1_we);
        bramW_inst.port_0_addr(sig_bramW_port_0_addr);
        bramW_inst.port_0_clk(sig_bramW_port_0_clk);
        bramW_inst.port_0_din(sig_bramW_port_0_din);
        bramW_inst.port_0_dout(sig_bramW_port_0_dout);
        bramW_inst.port_0_en(sig_bramW_port_0_en);
        bramW_inst.port_0_we(sig_bramW_port_0_we);
        bramW_inst.port_1_addr(sig_bramW_port_1_addr);
        bramW_inst.port_1_clk(sig_bramW_port_1_clk);
        bramW_inst.port_1_din(sig_bramW_port_1_din);
        bramW_inst.port_1_dout(sig_bramW_port_1_dout);
        bramW_inst.port_1_en(sig_bramW_port_1_en);
        bramW_inst.port_1_we(sig_bramW_port_1_we);
    }
};
