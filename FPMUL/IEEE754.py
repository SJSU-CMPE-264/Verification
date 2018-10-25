import numpy as np

class IEEE754:      
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            value = args[0]
            if isinstance(value, str):
                self.float = IEEE754.strToFloat(value)
            elif isinstance(value, float) or isinstance(value, int) or isinstance(value, np.float32):
                self.float = np.float3 -2(value)
            else:
                self.float = np.float32(0)
        elif len(args) == 3:
            self.float = IEEE754.bitsToFloat(args[0], args[1], args[2])
        else:
            self.float = np.float32(0)
        
        self.flags = {
            "OF":   False,
            "UF":   False,
            "NaNF": False,
            "InfF": False,
            "DNF":  False,
            "ZF":   False
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
        low  = product & ((2 ** length) - 1)
        return high, low
    
    @staticmethod
    def bitsToStr(sign, exponent, mantissa):
        return "{:01b}{:08b}{:023b}".format(sign, exponent, mantissa)
    
    @staticmethod
    def bitsToFloat(sign, exponent, mantissa):
        if sign not in range(0, 2 ** 1):
            raise ValueError("Sign Bit is Out of Range")
        elif exponent not in range(2 ** 8):
            raise ValueError("Exponent is Out of Range")
        elif mantissa not in range(2 ** 23):
            raise ValueError("Mantissa is Out of Range")
        return IEEE754.strToFloat(IEEE754.bitsToStr(sign, exponent, mantissa))
    
    @staticmethod
    def strToBits(bin_str):
        sign     = int(bin_str[0], 2)
        exponent = int(bin_str[1:9], 2)
        mantissa = int(bin_str[9:32], 2)
        return sign, exponent, mantissa
    
    @staticmethod
    def strToFloat(bin_str):
        if len(bin_str) < 32:
            raise ValueError("Binary String is too short")
        elif len(bin_str) > 32:
            raise ValueError("Binary String is too long")
        byte = int(bin_str, 2).to_bytes(4, byteorder="little")
        return np.frombuffer(byte, dtype=np.float32)[0]

    def floatToStr(self):
        mv = memoryview(self.float)
        bin_str = ""
        for i in range(4):
            bin_str += "{:08b}".format(mv[3-i])
        return bin_str

    def floatToBits(self):
        return IEEE754.strToBits(self.floatToStr())
    
    def setFlags(self):
        _, exponent, mantissa = self.floatToBits()
        
        self.flags["NaNF"] = (exponent == 0xFF) and not (mantissa == 0)
        self.flags["InfF"] = (exponent == 0xFF) and     (mantissa == 0)
        self.flags["DNF" ] = (exponent == 0x00) and not (mantissa == 0)
        self.flags["ZF"  ] = (exponent == 0x00) and     (mantissa == 0)

    def __mul__(self, rhs):        
        signA, exponentA, mantissaA = self.floatToBits()
        signB, exponentB, mantissaB = rhs.floatToBits()
        
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
            
        guard  = bool(mantissa_L & (1 << 23))
        lsb    = bool(mantissa_H & 1)
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
            (self.flags["NaNF"]                      ) or
            (rhs.flags["NaNF"]                       ) or
            (self.flags["InfF"] and rhs.flags["ZF"]  ) or
            (rhs.flags["InfF"]  and self.flags["ZF"])
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
        return ((self.float == rhs.float) or (np.isnan(self.float) and np.isnan(rhs.float))) and (self.flags == rhs.flags)
    
    def __ne__(self, rhs):
        return not (self == rhs)
    
    def __repr__(self):
        return self.floatToStr()