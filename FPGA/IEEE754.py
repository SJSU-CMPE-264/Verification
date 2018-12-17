import struct
import numpy as np


class IEEE754:
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            value = args[0]
            if isinstance(value, str):
                self.sign, self.exponent, self.mantissa = IEEE754.strToBits(value)
            elif isinstance(value, int):
                self.sign, self.exponent, self.mantissa = IEEE754.strToBits("{:032b}".format(value))
            else:
                self.sign, self.exponent, self.mantissa = 0, 0, 0
        elif len(args) == 3:
            self.sign, self.exponent, self.mantissa = args
        else:
            self.sign, self.exponent, self.mantissa = 0, 0, 0

        if self.sign not in range(0, 2 ** 1):
            raise ValueError("Sign Bit is Out of Range")
        elif self.exponent not in range(2 ** 8):
            raise ValueError("Exponent is Out of Range")
        elif self.mantissa not in range(2 ** 23):
            raise ValueError("Mantissa is Out of Range")

        self.flags = {
            "OF": False,
            "UF": False,
            "NaNF": False,
            "InfF": False,
            "DNF": False,
            "ZF": False
        }

        self.setFlags()

        for key, value in kwargs.items():
            self.flags[key] = bool(value)

    @staticmethod
    def bitAddition(A, B, length):
        return ((A + B) % (2 ** length))

    @staticmethod
    def bitMultiplication(A, B, length):
        product = A * B
        high = (product >> length) & ((2 ** length) - 1)
        low = product & ((2 ** length) - 1)
        return high, low

    def bitsToStr(self):
        return "{:01b}{:08b}{:023b}".format(self.sign, self.exponent, self.mantissa)

    def bitsToInt(self):
        return int(self.bitsToStr(), 2)

    def bitsToFloat(self):
        return IEEE754.strToFloat(self.bitsToStr())

    @staticmethod
    def strToBits(bin_str):
        sign = int(bin_str[0], 2)
        exponent = int(bin_str[1:9], 2)
        mantissa = int(bin_str[9:32], 2)
        return sign, exponent, mantissa

    @staticmethod
    def strToFloat(bin_str):
        if len(bin_str) < 32:
            raise ValueError("Binary String is too short")
        elif len(bin_str) > 32:
            raise ValueError("Binary String is too long")
        bin_str = bin_str.lower().replace("z", "0").replace("x", "0")
        byte = struct.pack("<I", int(bin_str, 2))
        return np.frombuffer(byte, dtype=np.float32)[0]

    def setFlags(self):
        self.flags["NaNF"] = (self.exponent == 0xFF) and not (self.mantissa == 0)
        self.flags["InfF"] = (self.exponent == 0xFF) and (self.mantissa == 0)
        self.flags["DNF"] = (self.exponent == 0x00) and not (self.mantissa == 0)
        self.flags["ZF"] = (self.exponent == 0x00) and (self.mantissa == 0)

    def __mul__(self, rhs):
        signA, exponentA, mantissaA = self.sign, self.exponent, self.mantissa
        signB, exponentB, mantissaB = rhs.sign, rhs.exponent, rhs.mantissa

        sign = signA ^ signB

        mantissaA |= (1 << 23)
        mantissaB |= (1 << 23)

        exponent = IEEE754.bitAddition(exponentA, exponentB, 10)
        exponent = IEEE754.bitAddition(exponent, -127, 10)
        mantissa_H, mantissa_L = IEEE754.bitMultiplication(mantissaA, mantissaB, 24)

        if bool(mantissa_H & (1 << 23)):
            exponent += 1
        else:
            mantissa_H = ((mantissa_H & (2 ** 23 - 1)) << 1) | ((mantissa_L >> 23) & 1)
            mantissa_L = ((mantissa_L & (2 ** 23 - 1)) << 1)

        guard = bool(mantissa_L & (1 << 23))
        lsb = bool(mantissa_H & 1)
        sticky = bool(mantissa_L & (2 ** 23 - 1))

        round = guard and (lsb or sticky)
        carry = (mantissa_H == 0xFFFFFF)

        if round and not carry:
            mantissa_H += 1
        if round and carry:
            mantissa_H = 0x800000
            exponent += 1

        underflow = bool(exponent & (1 << 9))
        overflow = (
                (
                        (not (bool(exponent & (1 << 9)))) and
                        bool(exponent & (1 << 8))
                ) or
                (exponent == 0xFF)
        )

        NaNF = (
                (self.flags["NaNF"]) or
                (rhs.flags["NaNF"]) or
                (self.flags["InfF"] and rhs.flags["ZF"]) or
                (rhs.flags["InfF"] and self.flags["ZF"])
        )

        InfF = (
                (
                        self.flags["InfF"] and
                        (not (rhs.flags["NaNF"] or rhs.flags["ZF"]))
                ) or
                (
                        rhs.flags["InfF"] and
                        (not (self.flags["NaNF"] or self.flags["ZF"]))
                )
        )

        ZF = (
                (
                        self.flags["ZF"] and
                        ((not rhs.flags["NaNF"]) or rhs.flags["ZF"])
                ) or
                (
                        rhs.flags["ZF"] and
                        ((not self.flags["NaNF"]) or self.flags["ZF"])
                )
        )

        if NaNF:
            return IEEE754(sign, 0xFF, 0x7FFFFF)
        elif InfF:
            return IEEE754(sign, 0xFF, 0)
        elif ZF:
            return IEEE754(sign, 0, 0)
        elif not underflow and overflow:
            return IEEE754(sign, 0xFF, 0, OF=True)
        elif underflow and not overflow:
            return IEEE754(sign, 0, 0, UF=True)

        return IEEE754(sign, exponent & (2 ** 8 - 1), mantissa_H & (2 ** 23 - 1))

    def __eq__(self, rhs):
        return ((self.bitsToStr() == rhs.bitsToStr())) and (self.flags == rhs.flags)

    def __ne__(self, rhs):
        return not (self == rhs)

    def __repr__(self):
        return self.bitsToStr()
