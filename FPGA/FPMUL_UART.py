import serial
import struct
import logging
from IEEE754 import IEEE754
from FPMUL_Generator import FPMUL_Generator
import pandas as pd

import json

SERIAL_PORT = "COM17"
BAUD_RATE = 115200


class FPMUL_UART:
    def __init__(self, port="COM4", baudrate=115200, timeout=5):
        self.ser = serial.Serial(baudrate=baudrate, timeout=timeout)
        self.ser.port = port

    def send_transacation(self, A, B):
        self.ser.open()

        start_bytes = FPMUL_UART.intToBytes(1, 0x1)
        A_bytes = FPMUL_UART.intToBytes(4, A)
        B_bytes = FPMUL_UART.intToBytes(4, B)

        data = start_bytes + A_bytes + B_bytes

        self.ser.write(data)
        self.ser.flush()  # Wait for all data to be written

        data = self.ser.read(5)  # Read 5 bytes of return data

        if len(data) != 5:
            print("Error number of bytes is not correct")
            return
        self.ser.close()

        all_flags = FPMUL_UART.bytesToInt(data[0:1])
        product = FPMUL_UART.bytesToInt(data[1:5])

        flag_names = ("OF", "UF", "NaNF", "InfF", "DNF", "ZF")
        flags = {}

        for i, flag in enumerate(flag_names):
            flags[flag] = bool(all_flags >> (len(flag_names) - i - 1) & 0x1)

        P = IEEE754(
            product,
            OF=flags["OF"],
            UF=flags["UF"],
            NaNF=flags["NaNF"],
            InfF=flags["InfF"],
            DNF=flags["DNF"],
            ZF=flags["ZF"]
        )

        return P
        # json.dumps(flags, indent=4)

    @staticmethod
    def intToBytes(byte_count, data):
        c_type = {
            1: "B",  # unsigned char
            2: "H",  # unsigned short
            4: "I",  # unsigned int
            8: "Q",  # unsigned long long
        }

        little_endian = ">"
        byte_format = little_endian + c_type[byte_count]
        return bytearray(struct.pack(byte_format, data))

    @staticmethod
    def bytesToInt(data):
        c_type = {
            1: "B",  # unsigned char
            2: "H",  # unsigned short
            4: "I",  # unsigned int
            8: "Q",  # unsigned long long
        }

        little_endian = ">"
        byte_count = len(data)
        byte_format = little_endian + c_type[byte_count]
        return struct.unpack(byte_format, data)[0]


def compare(received, lhs, rhs, strict_type=True):
    error = False
    expected = lhs * rhs

    # Compare directly
    # if received != expected:
    if received != expected:
        error = True

        logging.error("*****Received transaction differed from expected transaction*****")
        if received.bitsToFloat() != expected.bitsToFloat():
            logging.info("*** Product Mismatch ***\n\
                A = {:.23f} B = {:.23f}\n\
                A Binary String: {}\n\
                B Binary String: {}\n\
                Expected Binary String: {}\n\
                Received Binary String: {}\n\
                Expected Product Float: {:.23f}\n\
                Received Product Float: {:.23f}\n".format(
                lhs.bitsToFloat(), rhs.bitsToFloat(),
                lhs.bitsToStr(), rhs.bitsToStr(),
                expected.bitsToStr(), received.bitsToStr(),
                expected.bitsToFloat(), received.bitsToFloat()
            ))

        if received.flags != expected.flags:
            logging.info("*** Flags Mismatch ***\n\
                A = {:.23f} B = {:.23f}\n".format(
                lhs.bitsToFloat(), rhs.bitsToFloat()))
            for key in received.flags.keys():
                if received.flags[key] != expected.flags[key]:
                    logging.info("{}: Expected {} Received {}".format(
                        key, expected.flags[key], received.flags[key]
                    ))
    else:
        logging.debug("***Received expected transaction***\n\
                A = {:.23f} B = {:.23f} Product = {:.23f}\n".format(
            lhs.bitsToFloat(), rhs.bitsToFloat(), expected.bitsToFloat()))
    return error

logging.basicConfig(level=logging.DEBUG)

uart = FPMUL_UART(SERIAL_PORT)
errors = 0

# FPMUL_Generator()
    


test_function = [
    # Constraint Output
    # FPMUL_Generator.denormalizedProduct,
    # FPMUL_Generator.infinityProduct,
    # FPMUL_Generator.nanProduct,
    # FPMUL_Generator.normalProduct,
    # FPMUL_Generator.overflowProduct,
    # FPMUL_Generator.underflowProduct,
    # FPMUL_Generator.zeroProduct,

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

for i in range(100):
    for generator in test_function:
        for A, B in generator():
            P = uart.send_transacation(A.bitsToInt(), B.bitsToInt())
            if (compare(P, A, B)):
                errors += 1
            input()
