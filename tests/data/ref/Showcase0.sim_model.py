from pyMathBitPrecise.array3t import Array3t, Array3val
from pyMathBitPrecise.bits3t import Bits3t, Bits3val
from pyMathBitPrecise.enum3t import define_Enum3t

from hwtSimApi.basic_hdl_simulator.model import BasicRtlSimModel
from hwtSimApi.basic_hdl_simulator.model_utils import sensitivity, connectSimPort
from hwtSimApi.basic_hdl_simulator.proxy import BasicRtlSimProxy
from hwtSimApi.basic_hdl_simulator.sim_utils import sim_eval_cond

#
#    Every HW component class has to be derived from Unit class
#
#    .. hwt-autodoc::
#    
class Showcase0(BasicRtlSimModel):
    arr_t_0 = Bits3t(8, 1)[4]
    arr_t_1 = Bits3t(8, 0)[4]
    def __init__(self, sim: "BasicRtlSimulator", name="Showcase0"):
        BasicRtlSimModel.__init__(self, sim, name=name)
        # ports
        self.io.a = BasicRtlSimProxy(
            sim, self, "a",
            Bits3t(32, 0), None)
        self.io.b = BasicRtlSimProxy(
            sim, self, "b",
            Bits3t(32, 1), None)
        self.io.c = BasicRtlSimProxy(
            sim, self, "c",
            Bits3t(32, 0), None)
        self.io.clk = BasicRtlSimProxy(
            sim, self, "clk",
            Bits3t(1, 0), None)
        self.io.cmp_0 = BasicRtlSimProxy(
            sim, self, "cmp_0",
            Bits3t(1, 0), None)
        self.io.cmp_1 = BasicRtlSimProxy(
            sim, self, "cmp_1",
            Bits3t(1, 0), None)
        self.io.cmp_2 = BasicRtlSimProxy(
            sim, self, "cmp_2",
            Bits3t(1, 0), None)
        self.io.cmp_3 = BasicRtlSimProxy(
            sim, self, "cmp_3",
            Bits3t(1, 0), None)
        self.io.cmp_4 = BasicRtlSimProxy(
            sim, self, "cmp_4",
            Bits3t(1, 0), None)
        self.io.cmp_5 = BasicRtlSimProxy(
            sim, self, "cmp_5",
            Bits3t(1, 0), None)
        self.io.contOut = BasicRtlSimProxy(
            sim, self, "contOut",
            Bits3t(32, 0), None)
        self.io.d = BasicRtlSimProxy(
            sim, self, "d",
            Bits3t(32, 0), None)
        self.io.e = BasicRtlSimProxy(
            sim, self, "e",
            Bits3t(1, 0), None)
        self.io.f = BasicRtlSimProxy(
            sim, self, "f",
            Bits3t(1, 0), None)
        self.io.fitted = BasicRtlSimProxy(
            sim, self, "fitted",
            Bits3t(16, 0), None)
        self.io.g = BasicRtlSimProxy(
            sim, self, "g",
            Bits3t(8, 0), None)
        self.io.h = BasicRtlSimProxy(
            sim, self, "h",
            Bits3t(8, 0), None)
        self.io.i = BasicRtlSimProxy(
            sim, self, "i",
            Bits3t(2, 0), None)
        self.io.j = BasicRtlSimProxy(
            sim, self, "j",
            Bits3t(8, 0), None)
        self.io.k = BasicRtlSimProxy(
            sim, self, "k",
            Bits3t(32, 0), None)
        self.io.out = BasicRtlSimProxy(
            sim, self, "out",
            Bits3t(1, 0), None)
        self.io.output = BasicRtlSimProxy(
            sim, self, "output",
            Bits3t(1, 0), None)
        self.io.rst_n = BasicRtlSimProxy(
            sim, self, "rst_n",
            Bits3t(1, 0), None)
        self.io.sc_signal = BasicRtlSimProxy(
            sim, self, "sc_signal",
            Bits3t(8, 0), None)
        # internal signals
        self.const_private_signal = Bits3val(Bits3t(32, 0), 123, 4294967295)
        self.io.fallingEdgeRam = BasicRtlSimProxy(
            sim, self, "fallingEdgeRam",
            self.arr_t_0, None)
        self.io.r = BasicRtlSimProxy(
            sim, self, "r",
            Bits3t(1, 0), Bits3val(Bits3t(1, 0), 0, 1))
        self.io.r_0 = BasicRtlSimProxy(
            sim, self, "r_0",
            Bits3t(2, 0), Bits3val(Bits3t(2, 0), 0, 3))
        self.io.r_1 = BasicRtlSimProxy(
            sim, self, "r_1",
            Bits3t(2, 0), Bits3val(Bits3t(2, 0), 0, 3))
        self.io.r_next = BasicRtlSimProxy(
            sim, self, "r_next",
            Bits3t(1, 0), None)
        self.io.r_next_0 = BasicRtlSimProxy(
            sim, self, "r_next_0",
            Bits3t(2, 0), None)
        self.io.r_next_1 = BasicRtlSimProxy(
            sim, self, "r_next_1",
            Bits3t(2, 0), None)
        self.rom = Array3val(self.arr_t_1, {0: Bits3val(Bits3t(8, 0), 0, 255),
            1: Bits3val(Bits3t(8, 0), 1, 255),
            2: Bits3val(Bits3t(8, 0), 2, 255),
            3: Bits3val(Bits3t(8, 0), 3, 255)
        }, 1)
        self.const_4_0 = Bits3val(Bits3t(32, 0), 4, 4294967295)
        self.const_4_1 = Bits3val(Bits3t(32, 1), 4, 4294967295)
        self.const_0 = Array3val(self.arr_t_0, {}, 0)
        self.const_0_0 = Bits3val(Bits3t(32, 0), 0, 0)
        self.const_1 = slice(8, 0, -1)
        self.const_0_1 = Bits3val(Bits3t(24, 0), 0, 16777215)
        self.const_2 = slice(16, 0, -1)
        self.const_1_0 = Bits3val(Bits3t(32, 1), 1, 4294967295)
        self.const_0_2 = Bits3val(Bits3t(32, 1), 0, 4294967295)
        self.const_3 = slice(6, 0, -1)
        self.const_0_3 = Bits3val(Bits3t(8, 0), 0, 0)
        self.const_2_0 = Bits3val(Bits3t(32, 1), 2, 4294967295)
        self.const_1_1 = Bits3val(Bits3t(1, 0), 1, 1)
        self.const_0_4 = Bits3val(Bits3t(8, 0), 0, 255)
        self.const_1_2 = Bits3val(Bits3t(8, 0), 1, 255)
        self.const_2_1 = Bits3val(Bits3t(8, 0), 2, 255)
        self.const_0_5 = Bits3val(Bits3t(1, 0), 0, 1)
        self.const_0_6 = Bits3val(Bits3t(1, 0), 0, 0)
        self.const_0_7 = Bits3val(Bits3t(2, 0), 0, 0)
        self.const_0_8 = Bits3val(Bits3t(2, 0), 0, 3)
        self.const_1_3 = Bits3val(Bits3t(32, 0), 1, 4294967295)
        self.const_2_2 = Bits3val(Bits3t(32, 0), 2, 4294967295)
        self.const_3_0 = Bits3val(Bits3t(32, 0), 3, 4294967295)
        self.const_3_1 = Bits3val(Bits3t(8, 0), 3, 255)
        self.const_4_2 = Bits3val(Bits3t(8, 0), 4, 255)
        # component instances
    def _init_body(self):
        self._interfaces = (
            self.io.a,
            self.io.b,
            self.io.c,
            self.io.clk,
            self.io.cmp_0,
            self.io.cmp_1,
            self.io.cmp_2,
            self.io.cmp_3,
            self.io.cmp_4,
            self.io.cmp_5,
            self.io.contOut,
            self.io.d,
            self.io.e,
            self.io.f,
            self.io.fitted,
            self.io.g,
            self.io.h,
            self.io.i,
            self.io.j,
            self.io.k,
            self.io.out,
            self.io.output,
            self.io.rst_n,
            self.io.sc_signal,
            self.io.fallingEdgeRam,
            self.io.r,
            self.io.r_0,
            self.io.r_1,
            self.io.r_next,
            self.io.r_next_0,
            self.io.r_next_1,
        )
        self._processes = (
            self.assig_process_c,
            self.assig_process_cmp_0,
            self.assig_process_cmp_1,
            self.assig_process_cmp_2,
            self.assig_process_cmp_3,
            self.assig_process_cmp_4,
            self.assig_process_cmp_5,
            self.assig_process_contOut,
            self.assig_process_f,
            self.assig_process_fallingEdgeRam,
            self.assig_process_fitted,
            self.assig_process_g,
            self.assig_process_h,
            self.assig_process_j,
            self.assig_process_out,
            self.assig_process_output,
            self.assig_process_r,
            self.assig_process_r_next,
            self.assig_process_r_next_0,
            self.assig_process_r_next_1,
            self.assig_process_sc_signal,
        )
        self._units = ()
        sensitivity(self.assig_process_c, self.io.a, self.io.b)
        self._outputs[self.assig_process_c] = (
            self.io.c,
        )
        sensitivity(self.assig_process_cmp_0, self.io.a)
        self._outputs[self.assig_process_cmp_0] = (
            self.io.cmp_0,
        )
        sensitivity(self.assig_process_cmp_1, self.io.a)
        self._outputs[self.assig_process_cmp_1] = (
            self.io.cmp_1,
        )
        sensitivity(self.assig_process_cmp_2, self.io.b)
        self._outputs[self.assig_process_cmp_2] = (
            self.io.cmp_2,
        )
        sensitivity(self.assig_process_cmp_3, self.io.b)
        self._outputs[self.assig_process_cmp_3] = (
            self.io.cmp_3,
        )
        sensitivity(self.assig_process_cmp_4, self.io.b)
        self._outputs[self.assig_process_cmp_4] = (
            self.io.cmp_4,
        )
        sensitivity(self.assig_process_cmp_5, self.io.b)
        self._outputs[self.assig_process_cmp_5] = (
            self.io.cmp_5,
        )
        sensitivity(self.assig_process_contOut, )
        self._outputs[self.assig_process_contOut] = (
            self.io.contOut,
        )
        sensitivity(self.assig_process_f, self.io.r)
        self._outputs[self.assig_process_f] = (
            self.io.f,
        )
        sensitivity(self.assig_process_fallingEdgeRam, ((False, True), self.io.clk))
        self._outputs[self.assig_process_fallingEdgeRam] = (
            self.io.fallingEdgeRam,
            self.io.k,
        )
        sensitivity(self.assig_process_fitted, self.io.a)
        self._outputs[self.assig_process_fitted] = (
            self.io.fitted,
        )
        sensitivity(self.assig_process_g, self.io.a, self.io.b)
        self._outputs[self.assig_process_g] = (
            self.io.g,
        )
        sensitivity(self.assig_process_h, self.io.a, self.io.r)
        self._outputs[self.assig_process_h] = (
            self.io.h,
        )
        sensitivity(self.assig_process_j, ((True, False), self.io.clk))
        self._outputs[self.assig_process_j] = (
            self.io.j,
        )
        sensitivity(self.assig_process_out, )
        self._outputs[self.assig_process_out] = (
            self.io.out,
        )
        sensitivity(self.assig_process_output, )
        self._outputs[self.assig_process_output] = (
            self.io.output,
        )
        sensitivity(self.assig_process_r, ((True, False), self.io.clk))
        self._outputs[self.assig_process_r] = (
            self.io.r,
            self.io.r_0,
            self.io.r_1,
        )
        sensitivity(self.assig_process_r_next, self.io.i)
        self._outputs[self.assig_process_r_next] = (
            self.io.r_next_0,
        )
        sensitivity(self.assig_process_r_next_0, self.io.r_0)
        self._outputs[self.assig_process_r_next_0] = (
            self.io.r_next_1,
        )
        sensitivity(self.assig_process_r_next_1, self.io.e, self.io.r)
        self._outputs[self.assig_process_r_next_1] = (
            self.io.r_next,
        )
        sensitivity(self.assig_process_sc_signal, self.io.a)
        self._outputs[self.assig_process_sc_signal] = (
            self.io.sc_signal,
        )
        for u in self._units:
            u._init_body()

    # sensitivity: a, b
    def assig_process_c(self):
        self.io.c.val_next = (self.io.a.val + self.io.b.val.cast_sign(True), 0, )

    # sensitivity: a
    def assig_process_cmp_0(self):
        self.io.cmp_0.val_next = (self.io.a.val < self.const_4_0, 0, )

    # sensitivity: a
    def assig_process_cmp_1(self):
        self.io.cmp_1.val_next = (self.io.a.val > self.const_4_0, 0, )

    # sensitivity: b
    def assig_process_cmp_2(self):
        self.io.cmp_2.val_next = (self.io.b.val <= self.const_4_1, 0, )

    # sensitivity: b
    def assig_process_cmp_3(self):
        self.io.cmp_3.val_next = (self.io.b.val >= self.const_4_1, 0, )

    # sensitivity: b
    def assig_process_cmp_4(self):
        self.io.cmp_4.val_next = (self.io.b.val != self.const_4_1, 0, )

    # sensitivity: b
    def assig_process_cmp_5(self):
        self.io.cmp_5.val_next = (self.io.b.val._eq(self.const_4_1), 0, )

    # sensitivity: 
    def assig_process_contOut(self):
        self.io.contOut.val_next = (self.const_private_signal, 0, )

    # sensitivity: r
    def assig_process_f(self):
        self.io.f.val_next = (self.io.r.val, 0, )

    # sensitivity: HdlOpType.FALLING clk
    def assig_process_fallingEdgeRam(self):
        (c, cVld, ) = sim_eval_cond(self.io.clk._onFallingEdge())
        if not cVld:
            self.io.fallingEdgeRam.val_next = (self.const_0, 1, )
            self.io.k.val_next = (self.const_0_0, 1, )
        elif c:
            self.io.fallingEdgeRam.val_next = (self.io.a.val[self.const_1].cast_sign(False), (self.io.r_1.val, ), 1, )
            self.io.k.val_next = (self.const_0_1._concat(self.io.fallingEdgeRam.val[self.io.r_1.val].cast_sign(True)), 1, )
        else:
            pass

    # sensitivity: a
    def assig_process_fitted(self):
        self.io.fitted.val_next = (self.io.a.val[self.const_2], 0, )

    # sensitivity: a, b
    def assig_process_g(self):
        self.io.g.val_next = ((self.io.a.val[self.const_1_0] & self.io.b.val[self.const_1_0])._concat(self.io.a.val[self.const_0_2] ^ self.io.b.val[self.const_0_2] | self.io.a.val[self.const_1_0])._concat(self.io.a.val[self.const_3]), 0, )

    # sensitivity: a, r
    def assig_process_h(self):
        (c, cVld, ) = sim_eval_cond(self.io.a.val[self.const_2_0]._eq(self.const_1_1))
        if not cVld:
            self.io.h.val_next = (self.const_0_3, 0, )
        elif c:
            (c, cVld, ) = sim_eval_cond(self.io.r.val._eq(self.const_1_1))
            if not cVld:
                self.io.h.val_next = (self.const_0_3, 0, )
            elif c:
                self.io.h.val_next = (self.const_0_4, 0, )
            else:
                (c, cVld, ) = sim_eval_cond(self.io.a.val[self.const_1_0]._eq(self.const_1_1))
                if not cVld:
                    self.io.h.val_next = (self.const_0_3, 0, )
                elif c:
                    self.io.h.val_next = (self.const_1_2, 0, )
                else:
                    self.io.h.val_next = (self.const_2_1, 0, )
        else:
            pass

    # sensitivity: HdlOpType.RISING clk
    def assig_process_j(self):
        (c, cVld, ) = sim_eval_cond(self.io.clk._onRisingEdge())
        if not cVld:
            self.io.j.val_next = (self.const_0_3, 1, )
        elif c:
            self.io.j.val_next = (self.rom[self.io.r_1.val], 1, )
        else:
            pass

    # sensitivity: 
    def assig_process_out(self):
        self.io.out.val_next = (self.const_0_5, 0, )

    # sensitivity: 
    def assig_process_output(self):
        self.io.output.val_next = (self.const_0_6, 0, )

    # sensitivity: HdlOpType.RISING clk
    def assig_process_r(self):
        (c, cVld, ) = sim_eval_cond(self.io.clk._onRisingEdge())
        if not cVld:
            self.io.r_1.val_next = (self.const_0_7, 1, )
            self.io.r_0.val_next = (self.const_0_7, 1, )
            self.io.r.val_next = (self.const_0_6, 1, )
        elif c:
            (c, cVld, ) = sim_eval_cond(self.io.rst_n.val._eq(self.const_0_5))
            if not cVld:
                self.io.r_1.val_next = (self.const_0_7, 1, )
                self.io.r_0.val_next = (self.const_0_7, 1, )
                self.io.r.val_next = (self.const_0_6, 1, )
            elif c:
                self.io.r_1.val_next = (self.const_0_8, 1, )
                self.io.r_0.val_next = (self.const_0_8, 1, )
                self.io.r.val_next = (self.const_0_5, 1, )
            else:
                self.io.r_1.val_next = (self.io.r_next_1.val, 1, )
                self.io.r_0.val_next = (self.io.r_next_0.val, 1, )
                self.io.r.val_next = (self.io.r_next.val, 1, )
        else:
            pass

    # sensitivity: i
    def assig_process_r_next(self):
        self.io.r_next_0.val_next = (self.io.i.val, 0, )

    # sensitivity: r_0
    def assig_process_r_next_0(self):
        self.io.r_next_1.val_next = (self.io.r_0.val, 0, )

    # sensitivity: e, r
    def assig_process_r_next_1(self):
        (c, cVld, ) = sim_eval_cond((~self.io.r.val)._eq(self.const_1_1))
        if not cVld:
            self.io.r_next.val_next = (self.const_0_6, 0, )
        elif c:
            self.io.r_next.val_next = (self.io.e.val, 0, )
        else:
            self.io.r_next.val_next = (self.io.r.val, 0, )

    # sensitivity: a
    def assig_process_sc_signal(self):
        (c, cVld, ) = sim_eval_cond(self.io.a.val._eq(self.const_1_3))
        if not cVld:
            self.io.sc_signal.val_next = (self.const_0_3, 0, )
        elif c:
            self.io.sc_signal.val_next = (self.const_0_4, 0, )
        else:
            (c, cVld, ) = sim_eval_cond(self.io.a.val._eq(self.const_2_2))
            if not cVld:
                self.io.sc_signal.val_next = (self.const_0_3, 0, )
            elif c:
                self.io.sc_signal.val_next = (self.const_1_2, 0, )
            else:
                (c, cVld, ) = sim_eval_cond(self.io.a.val._eq(self.const_3_0))
                if not cVld:
                    self.io.sc_signal.val_next = (self.const_0_3, 0, )
                elif c:
                    self.io.sc_signal.val_next = (self.const_3_1, 0, )
                else:
                    self.io.sc_signal.val_next = (self.const_4_2, 0, )

