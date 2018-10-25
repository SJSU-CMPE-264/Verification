import IEEE754
from cocotb.scoreboard import Scoreboard
from cocotb.result import TestFailure, TestSuccess


class FPMUL_Scoreboard(Scoreboard):
    def __init__(self, dut, reorder_depth=0, fail_immediately=True):
        Scoreboard.__init__(self, dut, reorder_depth, fail_immediately)

        def compare(self, received, exp, log, strict_type=True):
            lhs, rhs, expected = exp

            # Compare the types
            if strict_type and type(received) != type(expected):
                self.errors += 1
                log.error("Received transaction is a different type to expected "
                          "transaction")
                log.info("received: %s but expected %s" %
                         (str(type(received)), str(type(expected))))
                if self._imm:
                    raise TestFailure("Received transaction of wrong type")
                return

            # Compare directly
            if received != expected:
                self.errors += 1

                log.error("*****Received transaction differed from expected transaction*****")

                if received.float != expected.float:
                    log.info("*** Product Mismatch ***\n\
                        A = {:.23f} B = {:.23f}\n\
                        Expected Binary String: {}\n\
                        Received Binary String: {}\n\
                        Expected Product Float: {:.23f}\n\
                        Received Product Float: {:.23f}\n".format(
                                lhs.float, rhs.float,
                                expected.floatToStr(), received.floatToStr(), 
                                expected.float, received.float
                            ))

                if received.flags != expected.flags:
                    log.info("*** Flags Mismatch ***\n\
                        A = {:.23f} B = {:.23f}\n".format(
                            lhs.float, rhs.float))
                    for key in received.flags.keys():
                        if received[key] != expected[key]:
                            log.info("{}: Expected {} Received{}\n".format(
                                    key, expected[key], received[key]
                                ))
            else:
                log.debug("***Received expected transaction***\n\
                        A = {:.23f} B = {:.23f} Product = {:.23f}\n".format(
                        lhs.float, rhs.float, expected.float))