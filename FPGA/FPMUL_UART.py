import serial
import struct

import json

SERIAL_PORT = "COM4"
BAUD_RATE   = 115200


class FPMUL_UART:
    def __init__(self, port="COM4", baudrate=115200, timeout=5):
        self.ser      = serial.Serial(baudrate=baudrate, timeout=timeout)
        self.ser.port = port

    def send_transacation(self, A, B):
        self.ser.open()

        start_bytes = FPMUL_UART.intToBytes(1, 0x1)
        A_bytes     = FPMUL_UART.intToBytes(4, A)
        B_bytes     = FPMUL_UART.intToBytes(4, B)

        data = start_bytes + A_bytes + B_bytes

        self.ser.write(data)  
        self.ser.flush()      # Wait for all data to be written

        data = self.ser.read(5) # Read 5 bytes of return data

        if len(data) != 5:
            print("Error number of bytes is not correct")
            return
        self.ser.close()

        all_flags =  FPMUL_UART.bytesToInt(data[0:1])
        P     =  FPMUL_UART.bytesToInt(data[1:5])


        flag_names = ("OF", "UF", "NaN", "Inf", "DNF", "ZF")
        flags = {}

        for i, flag in enumerate(flag_names):
            flags[flag] = bool(all_flags >> (len(flag_names) - i - 1) & 0x1)

        print("""A: {:08X}\n
            B: {:08X}\n
            Expected P: {:08X}\n
            Received P: {:08X}\n
            Flags:      {}\n
            """.format(A, B, (A + B) % (2**32), P, json.dumps(flags, indent=4)))


    @staticmethod
    def intToBytes(byte_count, data):
        c_type = {
            1: "B", # unsigned char
            2: "H", # unsigned short
            4: "I", # unsigned int
            8: "Q", # unsigned long long
        }

        little_endian = ">"
        byte_format = little_endian + c_type[byte_count]
        return bytearray(struct.pack(byte_format, data))

    @staticmethod
    def bytesToInt(data):
        c_type = {
            1: "B", # unsigned char
            2: "H", # unsigned short
            4: "I", # unsigned int
            8: "Q", # unsigned long long
        }

        little_endian = ">"
        byte_count = len(data)
        byte_format = little_endian + c_type[byte_count]
        return struct.unpack(byte_format, data)[0]


uart = FPMUL_UART()

operands = [
    (0x01, 0x02),
    (0x01234567, 0x89ABCDEF),
    (0x10000000, 0xF0000001)
]

for A, B in operands:
    uart.send_transacation(A, B)

    input("enter")
