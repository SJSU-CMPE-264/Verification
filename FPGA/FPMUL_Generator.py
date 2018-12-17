from IEEE754 import IEEE754
from random import randint
import pandas as pd

class FPMUL_Generator():

    initialized = False
    df = {}
    file_names = ("denormalized")

    def __init__(self):
        if not FPMUL_Generator.initialized:
            print("Initializing...")
            for file in FPMUL_Generator.file_names:
                print("Initializing " + file)
                raw_df = pd.read_csv("data/" + file + ".csv")
                FPMUL_Generator.df[file] = pd.DataFrame()
                FPMUL_Generator.df[file]["A"] = raw_df["A"].apply(lambda x: IEEE754("{:032b}".format(int(x, 16))))
                FPMUL_Generator.df[file]["B"] = raw_df["B"].apply(lambda x: IEEE754("{:032b}".format(int(x, 16))))
            FPMUL_Generator.initialized = True
    
    @staticmethod
    def denormalizedProduct():
        """denormalizedProduct"""
        for index, row in FPMUL_Generator.df["denormalized"].iterrows():
            yield (row.A, row.B)
    
    @staticmethod
    def infinityProduct():
        """infinityProduct"""
        for index, row in FPMUL_Generator.df["infinity"].iterrows():
            yield (row.A, row.B)
    
    @staticmethod
    def nanProduct():
        """nanProduct"""
        for index, row in FPMUL_Generator.df["nan"].iterrows():
            yield (row.A, row.B)
    
    @staticmethod
    def normalProduct():
        """normalProduct"""
        for index, row in FPMUL_Generator.df["normal"].iterrows():
            yield (row.A, row.B)
    
    @staticmethod
    def overflowProduct():
        """overflowProduct"""
        for index, row in FPMUL_Generator.df["overflow"].iterrows():
            yield (row.A, row.B)
    
    @staticmethod
    def underflowProduct():
        """underflowProduct"""
        for index, row in FPMUL_Generator.df["underflow"].iterrows():
            yield (row.A, row.B)
    
    @staticmethod
    def zeroProduct():
        """zeroProduct"""
        for index, row in FPMUL_Generator.df["zero"].iterrows():
            yield (row.A, row.B)

    #############################################
    ###  This Snippet Produces The Different  ###
    ###    Random Permutations of Operands    ###
    #############################################
    # functions = ("randomFloat",
    # "randomNormalFloat",
    # "randomNanFloat",
    # "randomDenormalizedFloat",
    # "randomZeroFloat",
    # "randomInfinityFloat")

    # for A in functions:
    #     for B in functions:
    #         print("@staticmethod")
    #         print("def {}_and_{}():".format(A, B))
    #         print("\tA = FPMUL_Generator.{}()".format(A))
    #         print("\tB = FPMUL_Generator.{}()".format(B))
    #         print("\tyield (A, B)")"
    #         print()

    @staticmethod
    def randomFloat_and_randomFloat():
        """randomFloat_and_randomFloat"""
        A = FPMUL_Generator.randomFloat()
        B = FPMUL_Generator.randomFloat()
        yield (A, B)


    @staticmethod
    def randomFloat_and_randomNormalFloat():
        """randomFloat_and_randomNormalFloat"""
        A = FPMUL_Generator.randomFloat()
        B = FPMUL_Generator.randomNormalFloat()
        yield (A, B)


    @staticmethod
    def randomFloat_and_randomNanFloat():
        """randomFloat_and_randomNanFloat"""
        A = FPMUL_Generator.randomFloat()
        B = FPMUL_Generator.randomNanFloat()
        yield (A, B)


    @staticmethod
    def randomFloat_and_randomDenormalizedFloat():
        """randomFloat_and_randomDenormalizedFloat"""
        A = FPMUL_Generator.randomFloat()
        B = FPMUL_Generator.randomDenormalizedFloat()
        yield (A, B)


    @staticmethod
    def randomFloat_and_randomZeroFloat():
        """randomFloat_and_randomZeroFloat"""
        A = FPMUL_Generator.randomFloat()
        B = FPMUL_Generator.randomZeroFloat()
        yield (A, B)


    @staticmethod
    def randomFloat_and_randomInfinityFloat():
        """randomFloat_and_randomInfinityFloat"""
        A = FPMUL_Generator.randomFloat()
        B = FPMUL_Generator.randomInfinityFloat()
        yield (A, B)


    @staticmethod
    def randomNormalFloat_and_randomFloat():
        """randomNormalFloat_and_randomFloat"""
        A = FPMUL_Generator.randomNormalFloat()
        B = FPMUL_Generator.randomFloat()
        yield (A, B)


    @staticmethod
    def randomNormalFloat_and_randomNormalFloat():
        """randomNormalFloat_and_randomNormalFloat"""
        A = FPMUL_Generator.randomNormalFloat()
        B = FPMUL_Generator.randomNormalFloat()
        yield (A, B)


    @staticmethod
    def randomNormalFloat_and_randomNanFloat():
        """randomNormalFloat_and_randomNanFloat"""
        A = FPMUL_Generator.randomNormalFloat()
        B = FPMUL_Generator.randomNanFloat()
        yield (A, B)


    @staticmethod
    def randomNormalFloat_and_randomDenormalizedFloat():
        """randomNormalFloat_and_randomDenormalizedFloat"""
        A = FPMUL_Generator.randomNormalFloat()
        B = FPMUL_Generator.randomDenormalizedFloat()
        yield (A, B)


    @staticmethod
    def randomNormalFloat_and_randomZeroFloat():
        """randomNormalFloat_and_randomZeroFloat"""
        A = FPMUL_Generator.randomNormalFloat()
        B = FPMUL_Generator.randomZeroFloat()
        yield (A, B)


    @staticmethod
    def randomNormalFloat_and_randomInfinityFloat():
        """randomNormalFloat_and_randomInfinityFloat"""
        A = FPMUL_Generator.randomNormalFloat()
        B = FPMUL_Generator.randomInfinityFloat()
        yield (A, B)


    @staticmethod
    def randomNanFloat_and_randomFloat():
        """randomNanFloat_and_randomFloat"""
        A = FPMUL_Generator.randomNanFloat()
        B = FPMUL_Generator.randomFloat()
        yield (A, B)


    @staticmethod
    def randomNanFloat_and_randomNormalFloat():
        """randomNanFloat_and_randomNormalFloat"""
        A = FPMUL_Generator.randomNanFloat()
        B = FPMUL_Generator.randomNormalFloat()
        yield (A, B)


    @staticmethod
    def randomNanFloat_and_randomNanFloat():
        """randomNanFloat_and_randomNanFloat"""
        A = FPMUL_Generator.randomNanFloat()
        B = FPMUL_Generator.randomNanFloat()
        yield (A, B)


    @staticmethod
    def randomNanFloat_and_randomDenormalizedFloat():
        """randomNanFloat_and_randomDenormalizedFloat"""
        A = FPMUL_Generator.randomNanFloat()
        B = FPMUL_Generator.randomDenormalizedFloat()
        yield (A, B)


    @staticmethod
    def randomNanFloat_and_randomZeroFloat():
        """randomNanFloat_and_randomZeroFloat"""
        A = FPMUL_Generator.randomNanFloat()
        B = FPMUL_Generator.randomZeroFloat()
        yield (A, B)


    @staticmethod
    def randomNanFloat_and_randomInfinityFloat():
        """randomNanFloat_and_randomInfinityFloat"""
        A = FPMUL_Generator.randomNanFloat()
        B = FPMUL_Generator.randomInfinityFloat()
        yield (A, B)


    @staticmethod
    def randomDenormalizedFloat_and_randomFloat():
        """randomDenormalizedFloat_and_randomFloat"""
        A = FPMUL_Generator.randomDenormalizedFloat()
        B = FPMUL_Generator.randomFloat()
        yield (A, B)


    @staticmethod
    def randomDenormalizedFloat_and_randomNormalFloat():
        """randomDenormalizedFloat_and_randomNormalFloat"""
        A = FPMUL_Generator.randomDenormalizedFloat()
        B = FPMUL_Generator.randomNormalFloat()
        yield (A, B)


    @staticmethod
    def randomDenormalizedFloat_and_randomNanFloat():
        """randomDenormalizedFloat_and_randomNanFloat"""
        A = FPMUL_Generator.randomDenormalizedFloat()
        B = FPMUL_Generator.randomNanFloat()
        yield (A, B)


    @staticmethod
    def randomDenormalizedFloat_and_randomDenormalizedFloat():
        """randomDenormalizedFloat_and_randomDenormalizedFloat"""
        A = FPMUL_Generator.randomDenormalizedFloat()
        B = FPMUL_Generator.randomDenormalizedFloat()
        yield (A, B)


    @staticmethod
    def randomDenormalizedFloat_and_randomZeroFloat():
        """randomDenormalizedFloat_and_randomZeroFloat"""
        A = FPMUL_Generator.randomDenormalizedFloat()
        B = FPMUL_Generator.randomZeroFloat()
        yield (A, B)


    @staticmethod
    def randomDenormalizedFloat_and_randomInfinityFloat():
        """randomDenormalizedFloat_and_randomInfinityFloat"""
        A = FPMUL_Generator.randomDenormalizedFloat()
        B = FPMUL_Generator.randomInfinityFloat()
        yield (A, B)


    @staticmethod
    def randomZeroFloat_and_randomFloat():
        """randomZeroFloat_and_randomFloat"""
        A = FPMUL_Generator.randomZeroFloat()
        B = FPMUL_Generator.randomFloat()
        yield (A, B)


    @staticmethod
    def randomZeroFloat_and_randomNormalFloat():
        """randomZeroFloat_and_randomNormalFloat"""
        A = FPMUL_Generator.randomZeroFloat()
        B = FPMUL_Generator.randomNormalFloat()
        yield (A, B)


    @staticmethod
    def randomZeroFloat_and_randomNanFloat():
        """randomZeroFloat_and_randomNanFloat"""
        A = FPMUL_Generator.randomZeroFloat()
        B = FPMUL_Generator.randomNanFloat()
        yield (A, B)


    @staticmethod
    def randomZeroFloat_and_randomDenormalizedFloat():
        """randomZeroFloat_and_randomDenormalizedFloat"""
        A = FPMUL_Generator.randomZeroFloat()
        B = FPMUL_Generator.randomDenormalizedFloat()
        yield (A, B)


    @staticmethod
    def randomZeroFloat_and_randomZeroFloat():
        """randomZeroFloat_and_randomZeroFloat"""
        A = FPMUL_Generator.randomZeroFloat()
        B = FPMUL_Generator.randomZeroFloat()
        yield (A, B)


    @staticmethod
    def randomZeroFloat_and_randomInfinityFloat():
        """randomZeroFloat_and_randomInfinityFloat"""
        A = FPMUL_Generator.randomZeroFloat()
        B = FPMUL_Generator.randomInfinityFloat()
        yield (A, B)


    @staticmethod
    def randomInfinityFloat_and_randomFloat():
        """randomInfinityFloat_and_randomFloat"""
        A = FPMUL_Generator.randomInfinityFloat()
        B = FPMUL_Generator.randomFloat()
        yield (A, B)


    @staticmethod
    def randomInfinityFloat_and_randomNormalFloat():
        """randomInfinityFloat_and_randomNormalFloat"""
        A = FPMUL_Generator.randomInfinityFloat()
        B = FPMUL_Generator.randomNormalFloat()
        yield (A, B)


    @staticmethod
    def randomInfinityFloat_and_randomNanFloat():
        """randomInfinityFloat_and_randomNanFloat"""
        A = FPMUL_Generator.randomInfinityFloat()
        B = FPMUL_Generator.randomNanFloat()
        yield (A, B)


    @staticmethod
    def randomInfinityFloat_and_randomDenormalizedFloat():
        """randomInfinityFloat_and_randomDenormalizedFloat"""
        A = FPMUL_Generator.randomInfinityFloat()
        B = FPMUL_Generator.randomDenormalizedFloat()
        yield (A, B)


    @staticmethod
    def randomInfinityFloat_and_randomZeroFloat():
        """randomInfinityFloat_and_randomZeroFloat"""
        A = FPMUL_Generator.randomInfinityFloat()
        B = FPMUL_Generator.randomZeroFloat()
        yield (A, B)


    @staticmethod
    def randomInfinityFloat_and_randomInfinityFloat():
        """randomInfinityFloat_and_randomInfinityFloat"""
        A = FPMUL_Generator.randomInfinityFloat()
        B = FPMUL_Generator.randomInfinityFloat()
        yield (A, B)


    @staticmethod
    def randomFloat():
        """Random Float"""
        sign     = randint(0, 1)
        exponent = randint(0, 0xFF)
        mantissa = randint(0, 0x7FFFFF)
        return IEEE754(sign, exponent, mantissa)

    @staticmethod
    def randomNormalFloat():
        """Random Normal Float"""
        sign     = randint(0, 1)
        exponent = randint(1, 0xFE)
        mantissa = randint(0, 0x7FFFFF)
        return IEEE754(sign, exponent, mantissa)

    @staticmethod
    def randomNanFloat():
        """Random NaN Float"""
        sign     = randint(0, 1)
        exponent = 0xFF
        mantissa = randint(1, 0x7FFFFF)
        return IEEE754(sign, exponent, mantissa)

    @staticmethod
    def randomDenormalizedFloat():
        """Random Denormalized Float"""
        sign     = randint(0, 1)
        exponent = 0
        mantissa = randint(1, 0x7FFFFF)
        return IEEE754(sign, exponent, mantissa)

    @staticmethod
    def randomZeroFloat():
        """Random Zero Float"""
        sign     = randint(0, 1)
        exponent = 0
        mantissa = 0
        return IEEE754(sign, exponent, mantissa)

    @staticmethod
    def randomInfinityFloat():
        """Random Infinity Float"""
        sign     = randint(0, 1)
        exponent = 0xFF
        mantissa = 0
        return IEEE754(sign, exponent, mantissa)
