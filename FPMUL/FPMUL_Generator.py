from IEEE754 import IEEE754
from random import randint

class FPMUL_Generator():
    @staticmethod
    def randomFloat():
        """Random Float"""
        sign     = randint(0, 1)
        exponent = randint(0, 0xFF)
        mantissa = randint(0, 0x7FFFFF)
        yield IEEE754(sign, exponent, mantissa)

    @staticmethod
    def randomNormalFloat():
        """Random Normal Float"""
        sign     = randint(0, 1)
        exponent = randint(1, 0xFE)
        mantissa = randint(0, 0x7FFFFF)
        yield IEEE754(sign, exponent, mantissa)

    @staticmethod
    def randomNanFloat():
        """Random NaN Float"""
        sign     = randint(0, 1)
        exponent = 0xFF
        mantissa = randint(1, 0x7FFFFF)
        yield IEEE754(sign, exponent, mantissa)

    @staticmethod
    def randomDenormalizedFloat():
        """Random Denormalized Float"""
        sign     = randint(0, 1)
        exponent = 0
        mantissa = randint(1, 0x7FFFFF)
        yield IEEE754(sign, exponent, mantissa)

    @staticmethod
    def randomZeroFloat():
        """Random Zero Float"""
        sign     = randint(0, 1)
        exponent = 0
        mantissa = 0
        yield IEEE754(sign, exponent, mantissa)

    @staticmethod
    def randomInfinityFloat():
        """Random Infinity Float"""
        sign     = randint(0, 1)
        exponent = 0xFF
        mantissa = 0
        yield IEEE754(sign, exponent, mantissa)

   

