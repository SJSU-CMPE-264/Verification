from cocotb.drivers import BusDriver, Driver
from cocotb.decorators import coroutine

from IEEE754 import IEEE754
from cocotb.binary import BinaryValue
from cocotb.triggers import RisingEdge

"""
ntwong0
We need the Driver to be based on BusDriver, so that we can drive a bus input dut
We have a couple options
1. One Driver driving all inputs to dut
2. Multiple drivers driving separate inputs to dut

Since factory options granularize the inputs of A and B, let's go with option 2.
Expanding from this choice,
1. input_driver_A     - FPMUL_OperandDriver
2. input_driver_B     - FPMUL_OperandDriver
3. input_driver_Start - BusDriver
4. input_driver_Rst   - BusDriver

<s>Wait. Then do we need an FPMUL_Driver? Let's try without.</s>
NOPE. We need to define _driver_send()
"""

class FPMUL_OperandDriver(BusDriver):
    def __init__(self, entity, name, clock, _signals):
        self._signals = _signals
        self.clock = clock
        BusDriver.__init__(self, entity, name, clock)

    @coroutine
    def _driver_send(self, transaction, sync=True):
        '''
        ntwong0
        Transaction must be binaryValue, otherwise we can't properly send it to dut
        
        # sign, exponent, mantissa = self.generator()
        # return IEEE(sign, exponent, mantissa)
        '''
        # if sync:
        #     yield RisingEdge(self.clock)
        A_transaction, B_transaction = transaction

        A = BinaryValue(0, bits=32, bigEndian=False)
        B = BinaryValue(0, bits=32, bigEndian=False)
        
        A.binstr = A_transaction.bitsToStr()
        B.binstr = B_transaction.bitsToStr()

        self.bus.A <= A
        self.bus.B <= B

        self.log.info("_driver_send will send: %s", A)
        self.log.info("_driver_send will send: %s", B)

        yield RisingEdge(self.clock)
        

