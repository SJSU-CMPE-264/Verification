from IEEE754 import IEEE754
from cocotb.decorators import coroutine
from cocotb.monitors import Monitor
from cocotb.triggers import RisingEdge

class FPMUL_InputMonitor(Monitor):
    def __init__(self, dut, txn_valid, clock, callback=None, event=None):
        self.name = "input"
        self.txn_valid = txn_valid
        self.clock = clock
        self.dut = dut
        Monitor.__init__(self, callback, event)

    @coroutine
    def _monitor_recv(self):

        clk_edge = RisingEdge(self.clock)

        while True:
            yield clk_edge

            if self.txn_valid:
                lhs = IEEE754(self.dut.A.value.binstr.zfill(0))
                rhs = IEEE754(self.dut.B.value.binstr.zfill(0))
                ## grab needed info off the bus to create
                ## floating point class
                self._recv((lhs, rhs))