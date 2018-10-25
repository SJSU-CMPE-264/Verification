from random import randint

class FPMUL_Generator():
    @staticmethod
    def randomFloat():
        while True:
            sign     = randint(0, 1)
            exponent = randint(0, 0xFF)
            mantissa = randint(0, 0x7FFFFF)
            yield sign, exponent, mantissa

    @staticmethod
    def randomNormalFloat():
        while True:
            sign     = randint(0, 1)
            exponent = randint(1, 0xFE)
            mantissa = randint(0, 0x7FFFFF)
            yield sign, exponent, mantissa

    @staticmethod
    def randomNanFloat():
        while True:
            sign     = randint(0, 1)
            exponent = 0xFF
            mantissa = randint(1, 0x7FFFFF)
            yield sign, exponent, mantissa

    @staticmethod
    def randomDenormalizedFloat():
        while True:
            sign     = randint(0, 1)
            exponent = 0
            mantissa = randint(1, 0x7FFFFF)
            yield sign, exponent, mantissa

    @staticmethod
    def randomZeroFloat():
        while True:
            sign     = randint(0, 1)
            exponent = 0
            mantissa = 0
            yield sign, exponent, mantissa

    @staticmethod
    def randomInfinityFloat():
        while True:
            sign     = randint(0, 1)
            exponent = 0xFF
            mantissa = 0
            yield sign, exponent, mantissa