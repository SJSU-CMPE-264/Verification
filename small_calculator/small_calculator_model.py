from cocotb.binary import BinaryValue

def small_calculator_model(op, in1, in2):
    """ model of small calculator model """
    out = 0

    if op == 0:
        out = in1 + in2
    elif op == 1:
        out = in1 - in2
    elif op == 2:
        out = in1 & in2
    else:
        out = in1 ^ in2

    return out % 16
