from hwt.code import If, Switch, Concat
from hwt.code_utils import rename_signal
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import INT, SLICE, STR, BIT, FLOAT64
from hwt.hdl.types.enum import HEnum
from hwt.interfaces.std import Signal
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit

class Ram_dp(Unit):
    """
        True dual port RAM.
        :note: write-first variant 
    
        .. hwt-autodoc::
        
    """
    def _config(self):
        self.ADDR_WIDTH = Param(8)
        self.DATA_WIDTH = Param(64)

    def _declr(self):
        ADDR_WIDTH, DATA_WIDTH = \
        self.ADDR_WIDTH, self.DATA_WIDTH
        # ports
        self.a_addr = Signal(Bits(8))
        self.a_clk = Signal(Bits(1))
        self.a_din = Signal(Bits(64))
        self.a_dout = Signal(Bits(64))._m()
        self.a_en = Signal(Bits(1))
        self.a_we = Signal(Bits(1))
        self.b_addr = Signal(Bits(8))
        self.b_clk = Signal(Bits(1))
        self.b_din = Signal(Bits(64))
        self.b_dout = Signal(Bits(64))._m()
        self.b_en = Signal(Bits(1))
        self.b_we = Signal(Bits(1))
        # component instances

    def _impl(self):
        ADDR_WIDTH, DATA_WIDTH, a_addr, a_clk, a_din, a_dout, a_en, a_we, b_addr, b_clk, b_din, \
        b_dout, b_en, b_we = \
        self.ADDR_WIDTH, self.DATA_WIDTH, self.a_addr, self.a_clk, self.a_din, self.a_dout, self.a_en, self.a_we, self.b_addr, self.b_clk, self.b_din, \
        self.b_dout, self.b_en, self.b_we
        # internal signals
        ram_memory = self._sig("ram_memory", Bits(64)[256], def_val=None)
        # assig_process_a_dout
        If(a_clk._onRisingEdge() & a_en._eq(1),
            If(a_we._eq(1),
                ram_memory[a_addr](a_din)
            ),
            a_dout(ram_memory[a_addr])
        )
        # assig_process_b_dout
        If(b_clk._onRisingEdge() & b_en._eq(1),
            If(b_we._eq(1),
                ram_memory[b_addr](b_din)
            ),
            b_dout(ram_memory[b_addr])
        )
class GroupOfBlockrams(Unit):
    """
        .. hwt-autodoc::
        
    """
    def _config(self):
        self.ADDR_WIDTH = Param(8)
        self.DATA_WIDTH = Param(64)

    def _declr(self):
        ADDR_WIDTH, DATA_WIDTH = \
        self.ADDR_WIDTH, self.DATA_WIDTH
        # ports
        self.addr = Signal(Bits(8))
        self.clk = Signal(Bits(1))
        self.en = Signal(Bits(1))
        self.in_r_a = Signal(Bits(64))
        self.in_r_b = Signal(Bits(64))
        self.in_w_a = Signal(Bits(64))
        self.in_w_b = Signal(Bits(64))
        self.out_r_a = Signal(Bits(64))._m()
        self.out_r_b = Signal(Bits(64))._m()
        self.out_w_a = Signal(Bits(64))._m()
        self.out_w_b = Signal(Bits(64))._m()
        self.we = Signal(Bits(1))
        # component instances
        bramR_inst = self.bramR_inst = Ram_dp()
        bramR_inst.ADDR_WIDTH = 8
        bramR_inst.DATA_WIDTH = 64
        bramW_inst = self.bramW_inst = Ram_dp()
        bramW_inst.ADDR_WIDTH = 8
        bramW_inst.DATA_WIDTH = 64

    def _impl(self):
        ADDR_WIDTH, DATA_WIDTH, addr, clk, en, in_r_a, in_r_b, in_w_a, in_w_b, out_r_a, out_r_b, \
        out_w_a, out_w_b, we, bramR_inst, bramW_inst = \
        self.ADDR_WIDTH, self.DATA_WIDTH, self.addr, self.clk, self.en, self.in_r_a, self.in_r_b, self.in_w_a, self.in_w_b, self.out_r_a, self.out_r_b, \
        self.out_w_a, self.out_w_b, self.we, self.bramR_inst, self.bramW_inst
        # internal signals
        sig_bramR_a_addr = self._sig("sig_bramR_a_addr", Bits(8), def_val=None)
        sig_bramR_a_clk = self._sig("sig_bramR_a_clk", Bits(1), def_val=None)
        sig_bramR_a_din = self._sig("sig_bramR_a_din", Bits(64), def_val=None)
        sig_bramR_a_dout = self._sig("sig_bramR_a_dout", Bits(64), def_val=None)
        sig_bramR_a_en = self._sig("sig_bramR_a_en", Bits(1), def_val=None)
        sig_bramR_a_we = self._sig("sig_bramR_a_we", Bits(1), def_val=None)
        sig_bramR_b_addr = self._sig("sig_bramR_b_addr", Bits(8), def_val=None)
        sig_bramR_b_clk = self._sig("sig_bramR_b_clk", Bits(1), def_val=None)
        sig_bramR_b_din = self._sig("sig_bramR_b_din", Bits(64), def_val=None)
        sig_bramR_b_dout = self._sig("sig_bramR_b_dout", Bits(64), def_val=None)
        sig_bramR_b_en = self._sig("sig_bramR_b_en", Bits(1), def_val=None)
        sig_bramR_b_we = self._sig("sig_bramR_b_we", Bits(1), def_val=None)
        sig_bramW_a_addr = self._sig("sig_bramW_a_addr", Bits(8), def_val=None)
        sig_bramW_a_clk = self._sig("sig_bramW_a_clk", Bits(1), def_val=None)
        sig_bramW_a_din = self._sig("sig_bramW_a_din", Bits(64), def_val=None)
        sig_bramW_a_dout = self._sig("sig_bramW_a_dout", Bits(64), def_val=None)
        sig_bramW_a_en = self._sig("sig_bramW_a_en", Bits(1), def_val=None)
        sig_bramW_a_we = self._sig("sig_bramW_a_we", Bits(1), def_val=None)
        sig_bramW_b_addr = self._sig("sig_bramW_b_addr", Bits(8), def_val=None)
        sig_bramW_b_clk = self._sig("sig_bramW_b_clk", Bits(1), def_val=None)
        sig_bramW_b_din = self._sig("sig_bramW_b_din", Bits(64), def_val=None)
        sig_bramW_b_dout = self._sig("sig_bramW_b_dout", Bits(64), def_val=None)
        sig_bramW_b_en = self._sig("sig_bramW_b_en", Bits(1), def_val=None)
        sig_bramW_b_we = self._sig("sig_bramW_b_we", Bits(1), def_val=None)
        bramR_inst.a_addr(sig_bramR_a_addr)
        bramR_inst.a_clk(sig_bramR_a_clk)
        bramR_inst.a_din(sig_bramR_a_din)
        sig_bramR_a_dout(bramR_inst.a_dout)
        bramR_inst.a_en(sig_bramR_a_en)
        bramR_inst.a_we(sig_bramR_a_we)
        bramR_inst.b_addr(sig_bramR_b_addr)
        bramR_inst.b_clk(sig_bramR_b_clk)
        bramR_inst.b_din(sig_bramR_b_din)
        sig_bramR_b_dout(bramR_inst.b_dout)
        bramR_inst.b_en(sig_bramR_b_en)
        bramR_inst.b_we(sig_bramR_b_we)
        bramW_inst.a_addr(sig_bramW_a_addr)
        bramW_inst.a_clk(sig_bramW_a_clk)
        bramW_inst.a_din(sig_bramW_a_din)
        sig_bramW_a_dout(bramW_inst.a_dout)
        bramW_inst.a_en(sig_bramW_a_en)
        bramW_inst.a_we(sig_bramW_a_we)
        bramW_inst.b_addr(sig_bramW_b_addr)
        bramW_inst.b_clk(sig_bramW_b_clk)
        bramW_inst.b_din(sig_bramW_b_din)
        sig_bramW_b_dout(bramW_inst.b_dout)
        bramW_inst.b_en(sig_bramW_b_en)
        bramW_inst.b_we(sig_bramW_b_we)
        # assig_process_out_r_a
        out_r_a(sig_bramR_a_dout)
        # assig_process_out_r_b
        out_r_b(sig_bramR_b_dout)
        # assig_process_out_w_a
        out_w_a(sig_bramW_a_dout)
        # assig_process_out_w_b
        out_w_b(sig_bramW_b_dout)
        # assig_process_sig_bramR_a_addr
        sig_bramR_a_addr(addr)
        # assig_process_sig_bramR_a_clk
        sig_bramR_a_clk(clk)
        # assig_process_sig_bramR_a_din
        sig_bramR_a_din(in_r_a)
        # assig_process_sig_bramR_a_en
        sig_bramR_a_en(en)
        # assig_process_sig_bramR_a_we
        sig_bramR_a_we(we)
        # assig_process_sig_bramR_b_addr
        sig_bramR_b_addr(addr)
        # assig_process_sig_bramR_b_clk
        sig_bramR_b_clk(clk)
        # assig_process_sig_bramR_b_din
        sig_bramR_b_din(in_r_b)
        # assig_process_sig_bramR_b_en
        sig_bramR_b_en(en)
        # assig_process_sig_bramR_b_we
        sig_bramR_b_we(we)
        # assig_process_sig_bramW_a_addr
        sig_bramW_a_addr(addr)
        # assig_process_sig_bramW_a_clk
        sig_bramW_a_clk(clk)
        # assig_process_sig_bramW_a_din
        sig_bramW_a_din(in_w_a)
        # assig_process_sig_bramW_a_en
        sig_bramW_a_en(en)
        # assig_process_sig_bramW_a_we
        sig_bramW_a_we(we)
        # assig_process_sig_bramW_b_addr
        sig_bramW_b_addr(addr)
        # assig_process_sig_bramW_b_clk
        sig_bramW_b_clk(clk)
        # assig_process_sig_bramW_b_din
        sig_bramW_b_din(in_w_b)
        # assig_process_sig_bramW_b_en
        sig_bramW_b_en(en)
        # assig_process_sig_bramW_b_we
        sig_bramW_b_we(we)
