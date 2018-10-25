import IEEE754
from cocotb.monitors import Monitor
from cocotb.triggers import RisingEdge

class FPMUL_OutputMonitor(Monitor):
    def __init__(self, txn_valid, clock, callback=None, event=None):
        self.txn_valid = txn_valid
        self.clock = clock
        Monitor.__init__(self, callback, event)

    @coroutine
    def _monitor_recv(self):
        clk_edge = RisingEdge(self.clock)

        while True:
            yield clk_edge
            if self.txn_valid:
                product = IEEE754(
                            dut.P.binstr.zfill(32),
                            OF   = int(dut.OF),
                            UF   = int(dut.UF),
                            NaNF = int(dut.NaNF),
                            InfF = int(dut.InfF),
                            DNF  = int(dut.DNF),
                            ZF   = int(dut.ZF)
                        )
                self._recv(product)