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

# from cocotb.scoreboard import Scoreboard
from cocotb.generators.byte import random_data, get_bytes
from cocotb.clock import Clock

class FPMUL_TB(object):
    def __init__(self, dut, initSig, debug=False):
        """
        
        """

        # Some internal state
        self.dut = dut
        self.initSig = initSig
        # self.stopped = False

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
        
        # Reconstruct the input transactions from the pins
        # and send them to our 'model'
        self.input_monitor = FPMUL_InputMonitor(dut, dut.Start, dut.Clk, callback=self.model)
        self.output_monitor = FPMUL_OutputMonitor(dut, dut.Done, dut.Clk, self.initSig)
        # self.output_monitor = FPMUL_OutputMonitor(dut, dut.Done, dut.Clk, callback=self.whywhywhy)
        
        # Create a scoreboard on the outputs
        self.expected_output = []
        self.observed_output = []
        # self.scoreboard = Scoreboard(dut)
        self.scoreboard = FPMUL_Scoreboard(dut) #create a floating point scoreboard? mostly just to check and log flags
        self.scoreboard.add_interface(self.output_monitor, self.expected_output)

    def model(self, transaction):
        self.dut._log.info("model is called")
        # if self.dut.Start is True:
        A, B = transaction
        product = A * B
        """ 
        ntwong0 - just append product, exclude A and B since we are not appending 
            A or B in OutputMonitor
        # self.dut._log.info("model is appending\n A: %s\n B: %s\n product: %s", A, B, product)
        # self.expected_output.append((A, B, product))
         """
        self.dut._log.info("model is appending product: %s", product)
        self.expected_output.append(product)
    
    # def whywhywhy(self, transaction):
    #     self.dut._log.info("whyyyyyyyyy")
    #     # if self.dut.Done is True:
    #     self.observed_output.append((transaction))

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

    # def stop(self):
    #     """
    #     Stop generation of input data. 
    #     Also stop generation of expected output transactions.
    #     One more clock cycle must be executed afterwards, so that, output of
    #     """
    #     # self.input_driver.stop()
    #     self.stopped = True

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
    cocotb.fork(Clock(dut.Clk, 5000).start())
    initSig = [0]
    tb = FPMUL_TB(dut, initSig) # _monitor_recv() fired by both InMon and OutMon here
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
    """
    ntwong0 - the reason test_endian_swapper.py uses dut.stream_out_ready is to guard against 
        the residual dut.Done. So, we need a similar signal here.

        initSig: we declare this before FPMUL_TB, and we manipulate it here in run_test
    """
    initSig[0] = 1


    dut._log.info("Before _driver_send: A is %s, B is %s, P is %s", dut.A, dut.B, dut.P)

    for transaction in A():
        yield tb.input_driver_A._driver_send(transaction)

    for transaction in B():
        yield tb.input_driver_B._driver_send(transaction)

    dut._log.info("After _driver_send: A is %s, B is %s, P is %s", dut.A, dut.B, dut.P)

    # We're not using a driver on Start or Rst yet, since we're not doing tests on those yet.
    DoneFlag = 0
    
    dut.Start <= 1
    yield clk_edge
    dut.Start <= 0

    for i in range(10):
        dut._log.info("Iter %i, Done %i, cnt %i", i, dut.Done, dut.cnt)
        dut._log.info("run_test initSig %i", initSig[0])
        if dut.Done == 1: # ntwong0 - this comparison seems to be most effective
            DoneFlag = 1
            break
        yield clk_edge
    
    initSig[0] = 0
    dut._log.info("After clock cycles: A is %s, B is %s, P is %s", dut.A, dut.B, dut.P)

    if DoneFlag:
        dut._log.info("Done flag raised")
    else:
        raise TestFailure("No done flag here")

    yield clk_edge

    # Stop generation of input data. One more clock cycle is needed to capture
    # the resulting output of the DUT.
    # tb.stop()

    # Print result of scoreboard.
    dut._log.info("about to raise scoreboard.result")
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
