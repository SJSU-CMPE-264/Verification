# Simple tests for an small calculator module
import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
from small_calculator_model import small_calculator_model

from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from random import randint

import random

def reset(dut):
    dut.rst = 0
    yield Timer(100)
    dut.rst = 1
    yield Timer(100)
    dut.rst = 0


@cocotb.test()
def add_test(dut):
    """Test for 5 + 10"""
    dut.go = 0
    cocotb.fork(Clock(dut.clk, 100).start())

    reset(dut)
    OP = 0
    A = 5
    B = 10

    dut.go = 0
    dut.in1 = A
    dut.in2 = B
    dut.op = OP
    dut.go = 1
    yield Timer(5)
    yield RisingEdge(dut.clk)
    yield Timer(5)

    dut.go = 0
    
    while dut.done == 0:
        yield RisingEdge(dut.clk)
    
    test_out = small_calculator_model(OP, A, B)
    if dut.out != test_out:
        raise TestFailure(
            "Model result is incorrect: {} != {}".format(dut.out, int(test_out)))
    else:  # these last two lines are not strictly necessary
        dut._log.info("Ok!")


@cocotb.test()
def sub_test(dut):
    dut.go = 0
    cocotb.fork(Clock(dut.clk, 100).start())

    reset(dut)
    OP = 1
    A = 5
    B = 10

    dut.go = 0
    dut.in1 = A
    dut.in2 = B
    dut.op = OP
    dut.go = 1
    yield Timer(5)
    yield RisingEdge(dut.clk)
    yield Timer(5)

    dut.go = 0
    
    while dut.done == 0:
        yield RisingEdge(dut.clk)
    
    test_out = small_calculator_model(OP, A, B)
    if dut.out != test_out:
        raise TestFailure(
            "Model result is incorrect: {} != {}".format(dut.out, int(test_out)))
    else:  # these last two lines are not strictly necessary
        dut._log.info("Ok!")

@cocotb.test()
def and_test(dut):
    dut.go = 0
    cocotb.fork(Clock(dut.clk, 100).start())

    reset(dut)
    OP = 2
    A = 5
    B = 10

    dut.go = 0
    dut.in1 = A
    dut.in2 = B
    dut.op = OP
    dut.go = 1
    yield Timer(5)
    yield RisingEdge(dut.clk)
    yield Timer(5)

    dut.go = 0
    
    while dut.done == 0:
        yield RisingEdge(dut.clk)
    
    test_out = small_calculator_model(OP, A, B)
    if dut.out != test_out:
        raise TestFailure(
            "Model result is incorrect: {} != {}".format(dut.out, int(test_out)))
    else:  # these last two lines are not strictly necessary
        dut._log.info("Ok!")

@cocotb.test()
def or_test(dut):
    dut.go = 0
    cocotb.fork(Clock(dut.clk, 100).start())

    reset(dut)
    OP = 3
    A = 5
    B = 10

    dut.go = 0
    dut.in1 = A
    dut.in2 = B
    dut.op = OP
    dut.go = 1
    yield Timer(5)
    yield RisingEdge(dut.clk)
    yield Timer(5)

    dut.go = 0
    
    while dut.done == 0:
        yield RisingEdge(dut.clk)
    
    test_out = small_calculator_model(OP, A, B)
    if dut.out != test_out:
        raise TestFailure(
            "Model result is incorrect: {} != {}".format(dut.out, int(test_out)))
    else:  # these last two lines are not strictly necessary
        dut._log.info("Ok!")