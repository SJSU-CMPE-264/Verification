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

        """
        self.input_driver = FPMUL_OperandDriver(dut, "", dut.Clk, ["A", "B"])

        # self.input_driver_Start = FPMUL_BusDriver(dut, "", dut.Clk, "Start")
        # self.input_driver_Rst   = FPMUL_BusDriver(dut, "", dut.Clk, "Rst")
        
        # Reconstruct the input transactions from the pins
        # and send them to our 'model'
        self.input_monitor  = FPMUL_InputMonitor(dut, dut.Start, dut.Clk, callback=self.model)
        self.output_monitor = FPMUL_OutputMonitor(dut, dut.Done, dut.Clk, self.initSig)
        # self.output_monitor = FPMUL_OutputMonitor(dut, dut.Done, dut.Clk, callback=self.whywhywhy)
        
        # Create a scoreboard on the outputs
        self.expected_output = []
        self.observed_output = []
        # self.scoreboard = Scoreboard(dut)
        self.scoreboard = FPMUL_Scoreboard(dut) #create a floating point scoreboard? mostly just to check and log flags
        self.scoreboard.add_interface(self.output_monitor, self.expected_output)

    def model(self, transaction):
        #self.dut._log.info("model is called")
        # if self.dut.Start is True:
        A, B = transaction
        product = A * B
        #self.dut._log.info("model is appending product: %s", product)
        self.expected_output.append((A, B, product))

    def start(self):
        """Start generation of input data."""
        # self.input_driver.start()

    @cocotb.coroutine
    def reset(self, duration=10000):
        #self.dut._log.info("Resetting DUT")
        self.dut.Rst   <= 1
        self.dut.Start <= 0
        yield Timer(duration)
        yield RisingEdge(self.dut.Clk)
        self.dut.Rst   <= 0
        #self.dut._log.info("Out of reset")

    # def stop(self):
    #     """
    #     Stop generation of input data. 
    #     Also stop generation of expected output transactions.
    #     One more clock cycle must be executed afterwards, so that, output of
    #     """
    #     # self.input_driver.stop()
    #     self.stopped = True

# ==============================================================================
@cocotb.coroutine
def run_test(dut, Operands):
    """Setup testbench and run a test."""
    cocotb.fork(Clock(dut.Clk, 5000).start())
    initSig = [0]
    tb = FPMUL_TB(dut, initSig) # _monitor_recv() fired by both InMon and OutMon here
    clk_edge = RisingEdge(dut.Clk)

    yield tb.reset()

    initSig = 1

    #dut._log.info("Before _driver_send: A is %s, B is %s, P is %s", dut.A, dut.B, dut.P)

    for transaction in Operands():
        yield tb.input_driver._driver_send(transaction)

    #dut._log.info("After _driver_send: A is %s, B is %s, P is %s", dut.A, dut.B, dut.P)

    # We're not using a driver on Start or Rst yet, since we're not doing tests on those yet.
    DoneFlag = 0
    
    dut.Start <= 1
    yield clk_edge
    dut.Start <= 0

    for i in range(10):
        #dut._log.info("Iter %i, Done %i", i, dut.Done)
        #dut._log.info("run_test initSig %i", initSig)
        if dut.Done == 1: # ntwong0 - this comparison seems to be most effective
            DoneFlag = 1
            break
        yield clk_edge
    
    initSig = 0
    # dut._log.info("After clock cycles: A is %s, B is %s, P is %s", dut.A, dut.B, dut.P)

    if not DoneFlag:
        raise TestFailure("No done flag here")

    yield clk_edge

    # Print result of scoreboard.
    #dut._log.info("about to raise scoreboard.result")
    raise tb.scoreboard.result

# ==============================================================================
# Register test.

FPMUL_Generator(10)
factory = TestFactory(run_test)

factory.add_option("Operands", [
            # Constraint Output
            FPMUL_Generator.denormalizedProduct,
            FPMUL_Generator.infinityProduct,
            FPMUL_Generator.nanProduct,
            FPMUL_Generator.normalProduct,
            FPMUL_Generator.overflowProduct,
            FPMUL_Generator.underflowProduct,
            FPMUL_Generator.zeroProduct,

            # Random Output
            FPMUL_Generator.randomFloat_and_randomFloat,
            FPMUL_Generator.randomFloat_and_randomNormalFloat,
            FPMUL_Generator.randomFloat_and_randomNanFloat,
            FPMUL_Generator.randomFloat_and_randomDenormalizedFloat,
            FPMUL_Generator.randomFloat_and_randomZeroFloat,
            FPMUL_Generator.randomFloat_and_randomInfinityFloat,
            FPMUL_Generator.randomNormalFloat_and_randomFloat,
            FPMUL_Generator.randomNormalFloat_and_randomNormalFloat,
            FPMUL_Generator.randomNormalFloat_and_randomNanFloat,
            FPMUL_Generator.randomNormalFloat_and_randomDenormalizedFloat,
            FPMUL_Generator.randomNormalFloat_and_randomZeroFloat,
            FPMUL_Generator.randomNormalFloat_and_randomInfinityFloat,
            FPMUL_Generator.randomNanFloat_and_randomFloat,
            FPMUL_Generator.randomNanFloat_and_randomNormalFloat,
            FPMUL_Generator.randomNanFloat_and_randomNanFloat,
            FPMUL_Generator.randomNanFloat_and_randomDenormalizedFloat,
            FPMUL_Generator.randomNanFloat_and_randomZeroFloat,
            FPMUL_Generator.randomNanFloat_and_randomInfinityFloat,
            FPMUL_Generator.randomDenormalizedFloat_and_randomFloat,
            FPMUL_Generator.randomDenormalizedFloat_and_randomNormalFloat,
            FPMUL_Generator.randomDenormalizedFloat_and_randomNanFloat,
            FPMUL_Generator.randomDenormalizedFloat_and_randomDenormalizedFloat,
            FPMUL_Generator.randomDenormalizedFloat_and_randomZeroFloat,
            FPMUL_Generator.randomDenormalizedFloat_and_randomInfinityFloat,
            FPMUL_Generator.randomZeroFloat_and_randomFloat,
            FPMUL_Generator.randomZeroFloat_and_randomNormalFloat,
            FPMUL_Generator.randomZeroFloat_and_randomNanFloat,
            FPMUL_Generator.randomZeroFloat_and_randomDenormalizedFloat,
            FPMUL_Generator.randomZeroFloat_and_randomZeroFloat,
            FPMUL_Generator.randomZeroFloat_and_randomInfinityFloat,
            FPMUL_Generator.randomInfinityFloat_and_randomFloat,
            FPMUL_Generator.randomInfinityFloat_and_randomNormalFloat,
            FPMUL_Generator.randomInfinityFloat_and_randomNanFloat,
            FPMUL_Generator.randomInfinityFloat_and_randomDenormalizedFloat,
            FPMUL_Generator.randomInfinityFloat_and_randomZeroFloat,
            FPMUL_Generator.randomInfinityFloat_and_randomInfinityFloat
        ]
    )

factory.generate_tests()
