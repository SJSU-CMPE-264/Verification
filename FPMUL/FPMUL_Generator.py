from IEEE754 import IEEE754
from random import randint
import pandas as pd

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

   




raw_df = pd.read_csv("constraint.csv")

constraint_df = pd.DataFrame()
for index, row in raw_df.iterrows():
    A    = "{:032b}".format(int(row.A, 16))
    B    = "{:032b}".format(int(row.B, 16))
    P    = "{:032b}".format(int(row.P, 16))
    UF   = row.UF
    OF   = row.OF
    NaNF = row.NaNF
    InfF = row.InfF
    DNF  = row.DNF
    ZF   = row.ZF

    A = IEEE754(A)
    B = IEEE754(B)
    P = IEEE754(P, UF=UF, OF=OF, NaNF=NaNF, InfF=InfF, DNF=DNF, ZF=ZF)

    data = {
        "A": A,
        "B": B,
        "P": P
    }
    constraint_df = constraint_df.append(data, ignore_index=True)
# print(constraint_df)
print("done")
constraint_df["P_exp"] = constraint_df["A"] * constraint_df["B"]
print("done")
wrong = constraint_df[constraint_df["P"] != constraint_df["P_exp"]]