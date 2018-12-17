class MIPS:
    R = {
        "$0"  : 0,
        "$at" : 1,
        "$v0" : 2,
        "$v1" : 3,
        "$a0" : 4,
        "$a1" : 5,
        "$a2" : 6,
        "$a3" : 7,
        "$t0" : 8,
        "$t1" : 9,
        "$t2" : 10,
        "$t3" : 11,
        "$t4" : 12,
        "$t5" : 13,
        "$t6" : 14,
        "$t7" : 15,
        "$s0" : 16,
        "$s1" : 17,
        "$s2" : 18,
        "$s3" : 19,
        "$s4" : 20,
        "$s5" : 21,
        "$s6" : 22,
        "$s7" : 23,
        "$t8" : 24,
        "$t9" : 25,
        "$k0" : 26,
        "$k1" : 27,
        "$gp" : 28,
        "$sp" : 29,
        "$fp" : 30,
        "$ra" : 31
    }

    INSTR = {
        "lui" : 0x0F,
        "ori" : 0x0D,
        "sw"  : 0x2B,
        "addi": 0x08,
        "j"   : 0x02,
        "jal" : 0x03,
        "jr"  : 0x08,
        "beq" : 0x04,
        "bne" : 0x05,
        "sll" : 0x00
    }

    @staticmethod
    def r_type(opcode, rs, rt, rd, shamt, funct):
        return "{:06b}{:05b}{:05b}{:05b}{:05b}{:06b}".format(opcode, rs, rt, rd, shamt, funct)
    
    @staticmethod
    def i_type(opcode, rs, rt, immediate):
        return "{:06b}{:05b}{:05b}{:016b}".format(opcode, rs, rt, immediate)
    
    @staticmethod
    def j_type(opcode, address):
        return "{:06b}{:024b}".format(opcode, address)
   
    @staticmethod
    def sendOperand(value, address):
        upper = value >> 16
        lower = value & (2 ** 16 - 1)

        instr = []
        instr.append(MIPS.i_type(MIPS.INSTR["lui"], MIPS.R["$0"], MIPS.R["$t0"], upper))
        instr.append(MIPS.i_type(MIPS.INSTR["ori"], MIPS.R["$t0"], MIPS.R["$t0"], lower))
        instr.append(MIPS.i_type(MIPS.INSTR["sw"],  MIPS.R["$0"], MIPS.R["$t0"], address))

        return instr

    @staticmethod
    def sendBEQ(address):
        instr = []
        instr.append(MIPS.i_type(MIPS.INSTR["beq"], MIPS.R["$0"], MIPS.R["$0"], address))

        return instr

    @staticmethod
    def sendJump(address):
        instr = []
        instr.append(MIPS.j_type(MIPS.INSTR["j"], address))

        return instr

    @staticmethod
    def sendStart(value, address):
        instr = []
        instr.append(MIPS.i_type(MIPS.INSTR["addi"], MIPS.R["$0"], MIPS.R["$t0"], value))
        instr.append(MIPS.i_type(MIPS.INSTR["sw"],   MIPS.R["$0"], MIPS.R["$t0"], address))

        return instr

    @staticmethod
    def sendNOP():
        instr = []
        instr.append(MIPS.r_type(0, MIPS.R["$0"], MIPS.R["$0"], MIPS.R["$0"], 0, MIPS.INSTR["sll"]))\
        return instr


for instr in MIPS.sendOperand(0x12345678, 0x40C):
    print(hex(int(instr, 2)))

for instr in MIPS.sendStart(0x40C):
    print(hex(int(instr, 2)))