from cocotb.drivers import BusDriver, Driver
from cocotb.decorators import coroutine

from IEEE754 import IEEE754
from cocotb.binary import BinaryValue
from cocotb.triggers import RisingEdge

class FPMUL_OperandDriver(BusDriver):
    def __init__(self, entity, name, clock, _signals):
        self._signals = _signals
        self.clock = clock
        BusDriver.__init__(self, entity, name, clock)

    @coroutine
    def _driver_send(self, transaction, sync=True):

        sendA, sendB, sendStart, nop, target_instr, isr_return = transaction

        # Write A to FPMUL
        for instr in sendA:
            self.bus.instr = instr
            yield RisingEdge(self.clock)

        # Write B to FPMUL
        for instr in sendB:
            self.bus.instr = instr
            yield RisingEdge(self.clock)

        # Write Start Bit to FPMUL
        for instr in sendStart:
            self.bus.instr = instr
            yield RisingEdge(self.clock)

        # Wait for ex_int Signal
        while ex_int.value == 0:
            self.bus.instr = nop
            yield RisingEdge(self.clock)

        # Change Instruction to Desired Current Instruction
        self.bus.instr = target_instr
        yield RisingEdge(self.clock)

        # Execute Some Instructions in the ISR
        for i in range(5):
            self.bus.instr = nop
            yield RisingEdge(self.clock)

        # Return from ISR
        self.bus.instr = isr_return
        yield RisingEdge(self.clock)