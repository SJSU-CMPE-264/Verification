from IEEE754 import IEEE754
from cocotb.decorators import coroutine
from cocotb.monitors import Monitor
from cocotb.triggers import RisingEdge

'''
ntwong0
Perhaps we need to use BusMonitor rather than Monitor
How do we restrict the InputMonitor from sending data?
'''

class FPMUL_InputMonitor(Monitor):
    def __init__(self, dut, txn_valid, clock, callback=None, event=None):
        self.name = "input"
        self.txn_valid = txn_valid
        self.clock = clock
        self.dut = dut
        Monitor.__init__(self, callback, event)

    @coroutine
    def _monitor_recv(self):
        self.dut._log.info("InputMonitor received something")
        clk_edge = RisingEdge(self.clock)

        while True:
            yield clk_edge

            if self.txn_valid:
                lhs = IEEE754(self.dut.A.value.binstr.zfill(32))
                rhs = IEEE754(self.dut.B.value.binstr.zfill(32))
                ## grab needed info off the bus to create
                ## floating point class
                self._recv((lhs, rhs))