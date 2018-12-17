from MIPS import MIPS

config = {
    "group-awesome": {
        "aAddress":     0xA00,
        "bAddress":     0xA04,
        "startAddress": 0xA08,
        "startValue": 0x10
    },
    "group-1": {
        "aAddress":     0xA00,
        "bAddress":     0xA04,
        "startAddress": 0xA08,
        "startValue": 0x01    
    }
}

class MIPS_Interrupt_Generator():
    def BEQ():
        sendA        = MIPS.sendOperand(A, config["group-awesome"]["aAddress"])
        sendB        = MIPS.sendOperand(B, config["group-awesome"]["bAddress"])
        sendStart    = MIPS.sendStart(config["group-awesome"]["startValue"], config["group-awesome"]["startAddress"])
        nop          = MIPS.sendNOP()
        target_instr = MIPS.sendBEQ(0x20) # Offset from current PC
        isr_return   = MIPS.sendRFE()

        yield sendA, sendB, sendStart, nop, target_instr, isr_return