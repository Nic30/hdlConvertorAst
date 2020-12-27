from pyMathBitPrecise.array3t import Array3t, Array3val
from pyMathBitPrecise.bits3t import Bits3t, Bits3val
from pyMathBitPrecise.enum3t import define_Enum3t

from hwtSimApi.basic_hdl_simulator.model import BasicRtlSimModel
from hwtSimApi.basic_hdl_simulator.model_utils import sensitivity, connectSimPort
from hwtSimApi.basic_hdl_simulator.proxy import BasicRtlSimProxy
from hwtSimApi.basic_hdl_simulator.sim_utils import sim_eval_cond

#
#    True dual port RAM.
#    :note: write-first variant 
#
#    .. hwt-autodoc::
#    
class Ram_dp(BasicRtlSimModel):
    arr_t_0 = Bits3t(64, 0)[256]
    def __init__(self, sim: "BasicRtlSimulator", name="Ram_dp"):
        BasicRtlSimModel.__init__(self, sim, name=name)
        # ports
        self.io.a_addr = BasicRtlSimProxy(
            sim, self, "a_addr",
            Bits3t(8, 0), None)
        self.io.a_clk = BasicRtlSimProxy(
            sim, self, "a_clk",
            Bits3t(1, 0), None)
        self.io.a_din = BasicRtlSimProxy(
            sim, self, "a_din",
            Bits3t(64, 0), None)
        self.io.a_dout = BasicRtlSimProxy(
            sim, self, "a_dout",
            Bits3t(64, 0), None)
        self.io.a_en = BasicRtlSimProxy(
            sim, self, "a_en",
            Bits3t(1, 0), None)
        self.io.a_we = BasicRtlSimProxy(
            sim, self, "a_we",
            Bits3t(1, 0), None)
        self.io.b_addr = BasicRtlSimProxy(
            sim, self, "b_addr",
            Bits3t(8, 0), None)
        self.io.b_clk = BasicRtlSimProxy(
            sim, self, "b_clk",
            Bits3t(1, 0), None)
        self.io.b_din = BasicRtlSimProxy(
            sim, self, "b_din",
            Bits3t(64, 0), None)
        self.io.b_dout = BasicRtlSimProxy(
            sim, self, "b_dout",
            Bits3t(64, 0), None)
        self.io.b_en = BasicRtlSimProxy(
            sim, self, "b_en",
            Bits3t(1, 0), None)
        self.io.b_we = BasicRtlSimProxy(
            sim, self, "b_we",
            Bits3t(1, 0), None)
        # internal signals
        self.io.ram_memory = BasicRtlSimProxy(
            sim, self, "ram_memory",
            self.arr_t_0, None)
        self.const_0 = Array3val(self.arr_t_0, {}, 0)
        self.const_0_0 = Bits3val(Bits3t(64, 0), 0, 0)
        self.const_1_0 = Bits3val(Bits3t(1, 0), 1, 1)
        # component instances
    def _init_body(self):
        self._interfaces = (
            self.io.a_addr,
            self.io.a_clk,
            self.io.a_din,
            self.io.a_dout,
            self.io.a_en,
            self.io.a_we,
            self.io.b_addr,
            self.io.b_clk,
            self.io.b_din,
            self.io.b_dout,
            self.io.b_en,
            self.io.b_we,
            self.io.ram_memory,
        )
        self._processes = (
            self.assig_process_a_dout,
            self.assig_process_b_dout,
        )
        self._units = ()
        sensitivity(self.assig_process_a_dout, ((True, False), self.io.a_clk))
        self._outputs[self.assig_process_a_dout] = (
            self.io.a_dout,
            self.io.ram_memory,
        )
        sensitivity(self.assig_process_b_dout, ((True, False), self.io.b_clk))
        self._outputs[self.assig_process_b_dout] = (
            self.io.b_dout,
            self.io.ram_memory,
        )
        for u in self._units:
            u._init_body()

    # sensitivity: HdlOpType.RISING a_clk
    def assig_process_a_dout(self):
        (c, cVld, ) = sim_eval_cond(self.io.a_clk._onRisingEdge() & self.io.a_en.val._eq(self.const_1_0))
        if not cVld:
            self.io.ram_memory.val_next = (self.const_0, 1, )
            self.io.a_dout.val_next = (self.const_0_0, 1, )
        elif c:
            (c, cVld, ) = sim_eval_cond(self.io.a_we.val._eq(self.const_1_0))
            if not cVld:
                self.io.ram_memory.val_next = (self.const_0, 1, )
            elif c:
                self.io.ram_memory.val_next = (self.io.a_din.val, (self.io.a_addr.val, ), 1, )
            else:
                pass
            self.io.a_dout.val_next = (self.io.ram_memory.val[self.io.a_addr.val], 1, )
        else:
            pass

    # sensitivity: HdlOpType.RISING b_clk
    def assig_process_b_dout(self):
        (c, cVld, ) = sim_eval_cond(self.io.b_clk._onRisingEdge() & self.io.b_en.val._eq(self.const_1_0))
        if not cVld:
            self.io.ram_memory.val_next = (self.const_0, 1, )
            self.io.b_dout.val_next = (self.const_0_0, 1, )
        elif c:
            (c, cVld, ) = sim_eval_cond(self.io.b_we.val._eq(self.const_1_0))
            if not cVld:
                self.io.ram_memory.val_next = (self.const_0, 1, )
            elif c:
                self.io.ram_memory.val_next = (self.io.b_din.val, (self.io.b_addr.val, ), 1, )
            else:
                pass
            self.io.b_dout.val_next = (self.io.ram_memory.val[self.io.b_addr.val], 1, )
        else:
            pass

#
#    .. hwt-autodoc::
#    
class GroupOfBlockrams(BasicRtlSimModel):
    def __init__(self, sim: "BasicRtlSimulator", name="GroupOfBlockrams"):
        BasicRtlSimModel.__init__(self, sim, name=name)
        # ports
        self.io.addr = BasicRtlSimProxy(
            sim, self, "addr",
            Bits3t(8, 0), None)
        self.io.clk = BasicRtlSimProxy(
            sim, self, "clk",
            Bits3t(1, 0), None)
        self.io.en = BasicRtlSimProxy(
            sim, self, "en",
            Bits3t(1, 0), None)
        self.io.in_r_a = BasicRtlSimProxy(
            sim, self, "in_r_a",
            Bits3t(64, 0), None)
        self.io.in_r_b = BasicRtlSimProxy(
            sim, self, "in_r_b",
            Bits3t(64, 0), None)
        self.io.in_w_a = BasicRtlSimProxy(
            sim, self, "in_w_a",
            Bits3t(64, 0), None)
        self.io.in_w_b = BasicRtlSimProxy(
            sim, self, "in_w_b",
            Bits3t(64, 0), None)
        self.io.out_r_a = BasicRtlSimProxy(
            sim, self, "out_r_a",
            Bits3t(64, 0), None)
        self.io.out_r_b = BasicRtlSimProxy(
            sim, self, "out_r_b",
            Bits3t(64, 0), None)
        self.io.out_w_a = BasicRtlSimProxy(
            sim, self, "out_w_a",
            Bits3t(64, 0), None)
        self.io.out_w_b = BasicRtlSimProxy(
            sim, self, "out_w_b",
            Bits3t(64, 0), None)
        self.io.we = BasicRtlSimProxy(
            sim, self, "we",
            Bits3t(1, 0), None)
        # internal signals
        self.io.sig_bramR_a_addr = BasicRtlSimProxy(
            sim, self, "sig_bramR_a_addr",
            Bits3t(8, 0), None)
        self.io.sig_bramR_a_clk = BasicRtlSimProxy(
            sim, self, "sig_bramR_a_clk",
            Bits3t(1, 0), None)
        self.io.sig_bramR_a_din = BasicRtlSimProxy(
            sim, self, "sig_bramR_a_din",
            Bits3t(64, 0), None)
        self.io.sig_bramR_a_dout = BasicRtlSimProxy(
            sim, self, "sig_bramR_a_dout",
            Bits3t(64, 0), None)
        self.io.sig_bramR_a_en = BasicRtlSimProxy(
            sim, self, "sig_bramR_a_en",
            Bits3t(1, 0), None)
        self.io.sig_bramR_a_we = BasicRtlSimProxy(
            sim, self, "sig_bramR_a_we",
            Bits3t(1, 0), None)
        self.io.sig_bramR_b_addr = BasicRtlSimProxy(
            sim, self, "sig_bramR_b_addr",
            Bits3t(8, 0), None)
        self.io.sig_bramR_b_clk = BasicRtlSimProxy(
            sim, self, "sig_bramR_b_clk",
            Bits3t(1, 0), None)
        self.io.sig_bramR_b_din = BasicRtlSimProxy(
            sim, self, "sig_bramR_b_din",
            Bits3t(64, 0), None)
        self.io.sig_bramR_b_dout = BasicRtlSimProxy(
            sim, self, "sig_bramR_b_dout",
            Bits3t(64, 0), None)
        self.io.sig_bramR_b_en = BasicRtlSimProxy(
            sim, self, "sig_bramR_b_en",
            Bits3t(1, 0), None)
        self.io.sig_bramR_b_we = BasicRtlSimProxy(
            sim, self, "sig_bramR_b_we",
            Bits3t(1, 0), None)
        self.io.sig_bramW_a_addr = BasicRtlSimProxy(
            sim, self, "sig_bramW_a_addr",
            Bits3t(8, 0), None)
        self.io.sig_bramW_a_clk = BasicRtlSimProxy(
            sim, self, "sig_bramW_a_clk",
            Bits3t(1, 0), None)
        self.io.sig_bramW_a_din = BasicRtlSimProxy(
            sim, self, "sig_bramW_a_din",
            Bits3t(64, 0), None)
        self.io.sig_bramW_a_dout = BasicRtlSimProxy(
            sim, self, "sig_bramW_a_dout",
            Bits3t(64, 0), None)
        self.io.sig_bramW_a_en = BasicRtlSimProxy(
            sim, self, "sig_bramW_a_en",
            Bits3t(1, 0), None)
        self.io.sig_bramW_a_we = BasicRtlSimProxy(
            sim, self, "sig_bramW_a_we",
            Bits3t(1, 0), None)
        self.io.sig_bramW_b_addr = BasicRtlSimProxy(
            sim, self, "sig_bramW_b_addr",
            Bits3t(8, 0), None)
        self.io.sig_bramW_b_clk = BasicRtlSimProxy(
            sim, self, "sig_bramW_b_clk",
            Bits3t(1, 0), None)
        self.io.sig_bramW_b_din = BasicRtlSimProxy(
            sim, self, "sig_bramW_b_din",
            Bits3t(64, 0), None)
        self.io.sig_bramW_b_dout = BasicRtlSimProxy(
            sim, self, "sig_bramW_b_dout",
            Bits3t(64, 0), None)
        self.io.sig_bramW_b_en = BasicRtlSimProxy(
            sim, self, "sig_bramW_b_en",
            Bits3t(1, 0), None)
        self.io.sig_bramW_b_we = BasicRtlSimProxy(
            sim, self, "sig_bramW_b_we",
            Bits3t(1, 0), None)
        # component instances
        self.bramR_inst = Ram_dp(sim, "bramR_inst")
        self.bramW_inst = Ram_dp(sim, "bramW_inst")
    def _init_body(self):
        connectSimPort(self, self.bramR_inst, "sig_bramR_a_addr", "a_addr")
        connectSimPort(self, self.bramR_inst, "sig_bramR_a_clk", "a_clk")
        connectSimPort(self, self.bramR_inst, "sig_bramR_a_din", "a_din")
        connectSimPort(self, self.bramR_inst, "sig_bramR_a_dout", "a_dout")
        connectSimPort(self, self.bramR_inst, "sig_bramR_a_en", "a_en")
        connectSimPort(self, self.bramR_inst, "sig_bramR_a_we", "a_we")
        connectSimPort(self, self.bramR_inst, "sig_bramR_b_addr", "b_addr")
        connectSimPort(self, self.bramR_inst, "sig_bramR_b_clk", "b_clk")
        connectSimPort(self, self.bramR_inst, "sig_bramR_b_din", "b_din")
        connectSimPort(self, self.bramR_inst, "sig_bramR_b_dout", "b_dout")
        connectSimPort(self, self.bramR_inst, "sig_bramR_b_en", "b_en")
        connectSimPort(self, self.bramR_inst, "sig_bramR_b_we", "b_we")
        connectSimPort(self, self.bramW_inst, "sig_bramW_a_addr", "a_addr")
        connectSimPort(self, self.bramW_inst, "sig_bramW_a_clk", "a_clk")
        connectSimPort(self, self.bramW_inst, "sig_bramW_a_din", "a_din")
        connectSimPort(self, self.bramW_inst, "sig_bramW_a_dout", "a_dout")
        connectSimPort(self, self.bramW_inst, "sig_bramW_a_en", "a_en")
        connectSimPort(self, self.bramW_inst, "sig_bramW_a_we", "a_we")
        connectSimPort(self, self.bramW_inst, "sig_bramW_b_addr", "b_addr")
        connectSimPort(self, self.bramW_inst, "sig_bramW_b_clk", "b_clk")
        connectSimPort(self, self.bramW_inst, "sig_bramW_b_din", "b_din")
        connectSimPort(self, self.bramW_inst, "sig_bramW_b_dout", "b_dout")
        connectSimPort(self, self.bramW_inst, "sig_bramW_b_en", "b_en")
        connectSimPort(self, self.bramW_inst, "sig_bramW_b_we", "b_we")
        self._interfaces = (
            self.io.addr,
            self.io.clk,
            self.io.en,
            self.io.in_r_a,
            self.io.in_r_b,
            self.io.in_w_a,
            self.io.in_w_b,
            self.io.out_r_a,
            self.io.out_r_b,
            self.io.out_w_a,
            self.io.out_w_b,
            self.io.we,
            self.io.sig_bramR_a_addr,
            self.io.sig_bramR_a_clk,
            self.io.sig_bramR_a_din,
            self.io.sig_bramR_a_dout,
            self.io.sig_bramR_a_en,
            self.io.sig_bramR_a_we,
            self.io.sig_bramR_b_addr,
            self.io.sig_bramR_b_clk,
            self.io.sig_bramR_b_din,
            self.io.sig_bramR_b_dout,
            self.io.sig_bramR_b_en,
            self.io.sig_bramR_b_we,
            self.io.sig_bramW_a_addr,
            self.io.sig_bramW_a_clk,
            self.io.sig_bramW_a_din,
            self.io.sig_bramW_a_dout,
            self.io.sig_bramW_a_en,
            self.io.sig_bramW_a_we,
            self.io.sig_bramW_b_addr,
            self.io.sig_bramW_b_clk,
            self.io.sig_bramW_b_din,
            self.io.sig_bramW_b_dout,
            self.io.sig_bramW_b_en,
            self.io.sig_bramW_b_we,
        )
        self._processes = (
            self.assig_process_out_r_a,
            self.assig_process_out_r_b,
            self.assig_process_out_w_a,
            self.assig_process_out_w_b,
            self.assig_process_sig_bramR_a_addr,
            self.assig_process_sig_bramR_a_clk,
            self.assig_process_sig_bramR_a_din,
            self.assig_process_sig_bramR_a_en,
            self.assig_process_sig_bramR_a_we,
            self.assig_process_sig_bramR_b_addr,
            self.assig_process_sig_bramR_b_clk,
            self.assig_process_sig_bramR_b_din,
            self.assig_process_sig_bramR_b_en,
            self.assig_process_sig_bramR_b_we,
            self.assig_process_sig_bramW_a_addr,
            self.assig_process_sig_bramW_a_clk,
            self.assig_process_sig_bramW_a_din,
            self.assig_process_sig_bramW_a_en,
            self.assig_process_sig_bramW_a_we,
            self.assig_process_sig_bramW_b_addr,
            self.assig_process_sig_bramW_b_clk,
            self.assig_process_sig_bramW_b_din,
            self.assig_process_sig_bramW_b_en,
            self.assig_process_sig_bramW_b_we,
        )
        self._units = (self.bramR_inst,
            self.bramW_inst,
        )
        sensitivity(self.assig_process_out_r_a, self.io.sig_bramR_a_dout)
        self._outputs[self.assig_process_out_r_a] = (
            self.io.out_r_a,
        )
        sensitivity(self.assig_process_out_r_b, self.io.sig_bramR_b_dout)
        self._outputs[self.assig_process_out_r_b] = (
            self.io.out_r_b,
        )
        sensitivity(self.assig_process_out_w_a, self.io.sig_bramW_a_dout)
        self._outputs[self.assig_process_out_w_a] = (
            self.io.out_w_a,
        )
        sensitivity(self.assig_process_out_w_b, self.io.sig_bramW_b_dout)
        self._outputs[self.assig_process_out_w_b] = (
            self.io.out_w_b,
        )
        sensitivity(self.assig_process_sig_bramR_a_addr, self.io.addr)
        self._outputs[self.assig_process_sig_bramR_a_addr] = (
            self.io.sig_bramR_a_addr,
        )
        sensitivity(self.assig_process_sig_bramR_a_clk, self.io.clk)
        self._outputs[self.assig_process_sig_bramR_a_clk] = (
            self.io.sig_bramR_a_clk,
        )
        sensitivity(self.assig_process_sig_bramR_a_din, self.io.in_r_a)
        self._outputs[self.assig_process_sig_bramR_a_din] = (
            self.io.sig_bramR_a_din,
        )
        sensitivity(self.assig_process_sig_bramR_a_en, self.io.en)
        self._outputs[self.assig_process_sig_bramR_a_en] = (
            self.io.sig_bramR_a_en,
        )
        sensitivity(self.assig_process_sig_bramR_a_we, self.io.we)
        self._outputs[self.assig_process_sig_bramR_a_we] = (
            self.io.sig_bramR_a_we,
        )
        sensitivity(self.assig_process_sig_bramR_b_addr, self.io.addr)
        self._outputs[self.assig_process_sig_bramR_b_addr] = (
            self.io.sig_bramR_b_addr,
        )
        sensitivity(self.assig_process_sig_bramR_b_clk, self.io.clk)
        self._outputs[self.assig_process_sig_bramR_b_clk] = (
            self.io.sig_bramR_b_clk,
        )
        sensitivity(self.assig_process_sig_bramR_b_din, self.io.in_r_b)
        self._outputs[self.assig_process_sig_bramR_b_din] = (
            self.io.sig_bramR_b_din,
        )
        sensitivity(self.assig_process_sig_bramR_b_en, self.io.en)
        self._outputs[self.assig_process_sig_bramR_b_en] = (
            self.io.sig_bramR_b_en,
        )
        sensitivity(self.assig_process_sig_bramR_b_we, self.io.we)
        self._outputs[self.assig_process_sig_bramR_b_we] = (
            self.io.sig_bramR_b_we,
        )
        sensitivity(self.assig_process_sig_bramW_a_addr, self.io.addr)
        self._outputs[self.assig_process_sig_bramW_a_addr] = (
            self.io.sig_bramW_a_addr,
        )
        sensitivity(self.assig_process_sig_bramW_a_clk, self.io.clk)
        self._outputs[self.assig_process_sig_bramW_a_clk] = (
            self.io.sig_bramW_a_clk,
        )
        sensitivity(self.assig_process_sig_bramW_a_din, self.io.in_w_a)
        self._outputs[self.assig_process_sig_bramW_a_din] = (
            self.io.sig_bramW_a_din,
        )
        sensitivity(self.assig_process_sig_bramW_a_en, self.io.en)
        self._outputs[self.assig_process_sig_bramW_a_en] = (
            self.io.sig_bramW_a_en,
        )
        sensitivity(self.assig_process_sig_bramW_a_we, self.io.we)
        self._outputs[self.assig_process_sig_bramW_a_we] = (
            self.io.sig_bramW_a_we,
        )
        sensitivity(self.assig_process_sig_bramW_b_addr, self.io.addr)
        self._outputs[self.assig_process_sig_bramW_b_addr] = (
            self.io.sig_bramW_b_addr,
        )
        sensitivity(self.assig_process_sig_bramW_b_clk, self.io.clk)
        self._outputs[self.assig_process_sig_bramW_b_clk] = (
            self.io.sig_bramW_b_clk,
        )
        sensitivity(self.assig_process_sig_bramW_b_din, self.io.in_w_b)
        self._outputs[self.assig_process_sig_bramW_b_din] = (
            self.io.sig_bramW_b_din,
        )
        sensitivity(self.assig_process_sig_bramW_b_en, self.io.en)
        self._outputs[self.assig_process_sig_bramW_b_en] = (
            self.io.sig_bramW_b_en,
        )
        sensitivity(self.assig_process_sig_bramW_b_we, self.io.we)
        self._outputs[self.assig_process_sig_bramW_b_we] = (
            self.io.sig_bramW_b_we,
        )
        for u in self._units:
            u._init_body()

    # sensitivity: sig_bramR_a_dout
    def assig_process_out_r_a(self):
        self.io.out_r_a.val_next = (self.io.sig_bramR_a_dout.val, 0, )

    # sensitivity: sig_bramR_b_dout
    def assig_process_out_r_b(self):
        self.io.out_r_b.val_next = (self.io.sig_bramR_b_dout.val, 0, )

    # sensitivity: sig_bramW_a_dout
    def assig_process_out_w_a(self):
        self.io.out_w_a.val_next = (self.io.sig_bramW_a_dout.val, 0, )

    # sensitivity: sig_bramW_b_dout
    def assig_process_out_w_b(self):
        self.io.out_w_b.val_next = (self.io.sig_bramW_b_dout.val, 0, )

    # sensitivity: addr
    def assig_process_sig_bramR_a_addr(self):
        self.io.sig_bramR_a_addr.val_next = (self.io.addr.val, 0, )

    # sensitivity: clk
    def assig_process_sig_bramR_a_clk(self):
        self.io.sig_bramR_a_clk.val_next = (self.io.clk.val, 0, )

    # sensitivity: in_r_a
    def assig_process_sig_bramR_a_din(self):
        self.io.sig_bramR_a_din.val_next = (self.io.in_r_a.val, 0, )

    # sensitivity: en
    def assig_process_sig_bramR_a_en(self):
        self.io.sig_bramR_a_en.val_next = (self.io.en.val, 0, )

    # sensitivity: we
    def assig_process_sig_bramR_a_we(self):
        self.io.sig_bramR_a_we.val_next = (self.io.we.val, 0, )

    # sensitivity: addr
    def assig_process_sig_bramR_b_addr(self):
        self.io.sig_bramR_b_addr.val_next = (self.io.addr.val, 0, )

    # sensitivity: clk
    def assig_process_sig_bramR_b_clk(self):
        self.io.sig_bramR_b_clk.val_next = (self.io.clk.val, 0, )

    # sensitivity: in_r_b
    def assig_process_sig_bramR_b_din(self):
        self.io.sig_bramR_b_din.val_next = (self.io.in_r_b.val, 0, )

    # sensitivity: en
    def assig_process_sig_bramR_b_en(self):
        self.io.sig_bramR_b_en.val_next = (self.io.en.val, 0, )

    # sensitivity: we
    def assig_process_sig_bramR_b_we(self):
        self.io.sig_bramR_b_we.val_next = (self.io.we.val, 0, )

    # sensitivity: addr
    def assig_process_sig_bramW_a_addr(self):
        self.io.sig_bramW_a_addr.val_next = (self.io.addr.val, 0, )

    # sensitivity: clk
    def assig_process_sig_bramW_a_clk(self):
        self.io.sig_bramW_a_clk.val_next = (self.io.clk.val, 0, )

    # sensitivity: in_w_a
    def assig_process_sig_bramW_a_din(self):
        self.io.sig_bramW_a_din.val_next = (self.io.in_w_a.val, 0, )

    # sensitivity: en
    def assig_process_sig_bramW_a_en(self):
        self.io.sig_bramW_a_en.val_next = (self.io.en.val, 0, )

    # sensitivity: we
    def assig_process_sig_bramW_a_we(self):
        self.io.sig_bramW_a_we.val_next = (self.io.we.val, 0, )

    # sensitivity: addr
    def assig_process_sig_bramW_b_addr(self):
        self.io.sig_bramW_b_addr.val_next = (self.io.addr.val, 0, )

    # sensitivity: clk
    def assig_process_sig_bramW_b_clk(self):
        self.io.sig_bramW_b_clk.val_next = (self.io.clk.val, 0, )

    # sensitivity: in_w_b
    def assig_process_sig_bramW_b_din(self):
        self.io.sig_bramW_b_din.val_next = (self.io.in_w_b.val, 0, )

    # sensitivity: en
    def assig_process_sig_bramW_b_en(self):
        self.io.sig_bramW_b_en.val_next = (self.io.en.val, 0, )

    # sensitivity: we
    def assig_process_sig_bramW_b_we(self):
        self.io.sig_bramW_b_we.val_next = (self.io.we.val, 0, )

