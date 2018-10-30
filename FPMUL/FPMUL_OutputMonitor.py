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
        self.dut._log.info("OutputMonitor received something")
        clk_edge = RisingEdge(self.clock)

        while True:
            yield clk_edge
            if self.txn_valid is True: # ntwong0 - looks like you need to explicitly specify that you are checking this parameter against True, because Python
                self.dut._log.info("OutputMonitor thinks dut.Done is asserted, even though dut.Done is %x. Compare to %x", self.dut.Done, self.txn_valid)
                product = IEEE754(
                            self.dut.P.value.binstr.zfill(32),
                            OF   = int(self.dut.OF),
                            UF   = int(self.dut.UF),
                            NaNF = int(self.dut.NaNF),
                            InfF = int(self.dut.InfF),
                            DNF  = int(self.dut.DNF),
                            ZF   = int(self.dut.ZF)
                        )
            '''
            ntwong0
            It seems that the OutputMonitor is sending data even though it's not supposed to
            #     self._recv(product)
            '''