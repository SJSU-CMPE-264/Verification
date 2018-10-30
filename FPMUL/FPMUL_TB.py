from IEEE754 import IEEE754

from FPMUL_InputMonitor import FPMUL_InputMonitor
from FPMUL_OutputMonitor import FPMUL_OutputMonitor
from FPMUL_Scoreboard import FPMUL_Scoreboard
from FPMUL_Driver import FPMUL_OperandDriver
from FPMUL_Generator import FPMUL_Generator

import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.drivers import BitDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory

from cocotb.scoreboard import Scoreboard
from cocotb.generators.byte import random_data, get_bytes
from cocotb.clock import Clock

class FPMUL_TB(object):
    def __init__(self, dut, debug=False):
        """
        
        """

        # Some internal state
        self.dut = dut
        self.stopped = False
        self.done = dut.Done

        # Create input driver and output monitor
        """
        ntwong0
        Since we're using BusDriver and Driver to drive the dut inputs, we don't
        need to use FPMUL_Driver()

        # self.input_driver = FPMUL_Driver()
        """
        self.input_driver_A     = FPMUL_OperandDriver(dut, "", dut.Clk, "A")
        self.input_driver_B     = FPMUL_OperandDriver(dut, "", dut.Clk, "B")
        # self.input_driver_Start = FPMUL_BusDriver(dut, "", dut.Clk, "Start")
        # self.input_driver_Rst   = FPMUL_BusDriver(dut, "", dut.Clk, "Rst")
        
        self.output_monitor = FPMUL_OutputMonitor(dut, dut.Done, dut.Clk)
        
        # Create a scoreboard on the outputs
        self.expected_output = []
        self.scoreboard = Scoreboard(dut)
        #self.scoreboard = FPMUL_Scoreboard(dut) #create a floating point scoreboard? mostly just to check and log flags
        self.scoreboard.add_interface(self.output_monitor, self.expected_output)

        # Reconstruct the input transactions from the pins
        # and send them to our 'model'
        self.input_monitor = FPMUL_InputMonitor(dut, dut.Start, dut.Clk, callback=self.model)

    def model(self, transaction):
        if self.done:
            A, B = transaction
            product = A * B
            self.expected_output.append((A, B, product))

    def start(self):
        """Start generation of input data."""
        # self.input_driver.start()

    @cocotb.coroutine
    def reset(self, duration=10000):
        self.dut._log.info("Resetting DUT")
        self.dut.Rst   <= 1
        self.dut.Start <= 0
        yield Timer(duration)
        yield RisingEdge(self.dut.Clk)
        self.dut.Rst   <= 0
        self.dut._log.info("Out of reset")

    def stop(self):
        """
        Stop generation of input data. 
        Also stop generation of expected output transactions.
        One more clock cycle must be executed afterwards, so that, output of
        """
        # self.input_driver.stop()
        self.stopped = True

# ==============================================================================
# @cocotb.coroutine
# def clock_gen(signal):
#     """Generate the clock signal."""
#     while True:
#         signal <= 0
#         yield Timer(5000) # ps
#         signal <= 1
#         yield Timer(5000) # ps

# ==============================================================================
@cocotb.coroutine
def run_test(dut, A, B):
    """Setup testbench and run a test."""
    # cocotb.fork(clock_gen(dut.Clk))
    cocotb.fork(Clock(dut.Clk, 5000).start())
    tb = FPMUL_TB(dut)
    clk_edge = RisingEdge(dut.Clk)

    """
    ntwong0
    Wait no - don't do this; the driver is supposed to set the bits
    run_test() shouldn't set the bits directly on the dut

    # Apply random input data by input_gen via Driver for 100 clock cycle.
    # tb.start()
    dut.Start = 0

    for lhs in A(): 
        dut.A = int(lhs.floatToStr(), 2)
    for rhs in B():
        dut.B = int(rhs.floatToStr(), 2)
    yield clk_edge
    dut.Start = 1
    yield clk_edge
    while not dut.Done:
        yield clk_edge
    """

    yield tb.reset()
    dut.Start <= 1 
    
    for transaction in A():
        yield tb.input_driver_A._driver_send(transaction)
    
    for transaction in B():
        yield tb.input_driver_B._driver_send(transaction)

    # We're not using a driver on Start or Rst yet, since we're not doing tests on those yet.
    DoneFlag = 0

    for i in range(5):
        if dut.Done:
            DoneFlag = 1
        yield clk_edge

    if DoneFlag:
        dut._log.info("Done flag raised")
    else:
        raise TestFailure("No done flag here")

    # Stop generation of input data. One more clock cycle is needed to capture
    # the resulting output of the DUT.
    # tb.stop()

    # Print result of scoreboard.
    raise tb.scoreboard.result

# ==============================================================================
# Register test.
factory = TestFactory(run_test)

factory.add_option("A", [
            FPMUL_Generator.randomFloat,
            FPMUL_Generator.randomNormalFloat,
            FPMUL_Generator.randomNanFloat,
            FPMUL_Generator.randomDenormalizedFloat,
            FPMUL_Generator.randomZeroFloat,
            FPMUL_Generator.randomInfinityFloat
        ]
    )

factory.add_option("B", [
            FPMUL_Generator.randomFloat,
            FPMUL_Generator.randomNormalFloat,
            FPMUL_Generator.randomNanFloat,
            FPMUL_Generator.randomDenormalizedFloat,
            FPMUL_Generator.randomZeroFloat,
            FPMUL_Generator.randomInfinityFloat
        ]
    )

factory.generate_tests()
