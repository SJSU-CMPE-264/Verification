from IEEE754 import IEEE754
from cocotb.decorators import coroutine
from cocotb.monitors import Monitor
from cocotb.triggers import RisingEdge

class FPMUL_OutputMonitor(Monitor):
    def __init__(self, dut, txn_valid, clock, callback=None, event=None):
        self.name = "output"
        self.txn_valid = txn_valid
        self.clock = clock
        self.dut = dut
        Monitor.__init__(self, callback, event)

    @coroutine
    def _monitor_recv(self):
        self.dut._log.info("OutputMonitor _monitor_recv started")
        clk_edge = RisingEdge(self.clock)
        count = 0

        while True:
            self.dut._log.info("OutputMonitor _monitor_recv iter %i", count)
            count = count + 1

            if str(self.txn_valid.value) == "1": # ntwong0 - looks like you need to explicitly specify that you are checking this parameter against True, because Python
                self.dut._log.info("OutputMonitor: dut.Done asserted, forming product ")
                product = IEEE754(
                            self.dut.P.value.binstr.zfill(32),
                            OF   = int(self.dut.OF),
                            UF   = int(self.dut.UF),
                            NaNF = int(self.dut.NaNF),
                            InfF = int(self.dut.InfF),
                            DNF  = int(self.dut.DNF),
                            ZF   = int(self.dut.ZF)
                        )
                self._recv(product)
            
            yield clk_edge