from IEEE754 import IEEE754
from cocotb.decorators import coroutine
from cocotb.monitors import Monitor
from cocotb.triggers import RisingEdge

from cocotb.binary import BinaryValue

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
        # self.dut._log.info("InputMonitor _monitor_recv started")
        clk_edge = RisingEdge(self.clock)
        count = 0

        while True:
            # self.dut._log.info("InputMonitor _monitor_recv iter %i", count)
            count = count + 1

            if str(self.txn_valid.value) == "1":
                # self.dut._log.info("InputMonitor: dut.Start asserted, forming lhs and rhs")
                lhs = IEEE754(self.dut.A.value.binstr.zfill(32))
                rhs = IEEE754(self.dut.B.value.binstr.zfill(32))
                ## grab needed info off the bus to create
                ## floating point class
                self._recv((lhs, rhs))

            yield clk_edge