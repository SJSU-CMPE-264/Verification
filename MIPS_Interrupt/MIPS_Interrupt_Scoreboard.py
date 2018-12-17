import IEEE754
from cocotb.scoreboard import Scoreboard
from cocotb.result import TestFailure, TestSuccess

import logging
import cocotb

from cocotb.utils import hexdump, hexdiffs
from cocotb.log import SimLog
from cocotb.monitors import Monitor
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
        # if received != expected:
        if received != expected:
            self.errors += 1

            log.error("*****Received transaction differed from expected transaction*****")
            if received.bitsToFloat() != expected.bitsToFloat():
                log.info("*** Product Mismatch ***\n\
                    A = {:.23f} B = {:.23f}\n\
                    A Binary String: {}\n\
                    B Binary String: {}\n\
                    Expected Binary String: {}\n\
                    Received Binary String: {}\n\
                    Expected Product Float: {:.23f}\n\
                    Received Product Float: {:.23f}\n".format(
                            lhs.bitsToFloat(), rhs.bitsToFloat(),
                            lhs.bitsToStr(), rhs.bitsToStr(),
                            expected.bitsToStr(), received.bitsToStr(), 
                            expected.bitsToFloat(), received.bitsToFloat()
                        ))

            if received.flags != expected.flags:
                log.info("*** Flags Mismatch ***\n\
                    A = {:.23f} B = {:.23f}\n".format(
                        lhs.bitsToFloat(), rhs.bitsToFloat()))
                for key in received.flags.keys():
                    if received.flags[key] != expected.flags[key]:
                        log.info("{}: Expected {} Received {}".format(
                                key, expected.flags[key], received.flags[key]
                            ))
        else:
            log.debug("***Received expected transaction***\n\
                    A = {:.23f} B = {:.23f} Product = {:.23f}\n".format(
                    lhs.bitsToFloat(), rhs.bitsToFloat(), expected.bitsToFloat()))


    def add_interface(self, monitor, expected_output, compare_fn=None,
                      reorder_depth=0, strict_type=True):
        """Add an interface to be scoreboarded.

            Provides a function which the monitor will callback with received
            transactions

            Simply check against the expected output.

        """
        # save a handle to the expected output so we can check if all expected
        # data has been received at the end of a test.
        self.expected[monitor] = expected_output

        # Enforce some type checking as we only work with a real monitor
        if not isinstance(monitor, Monitor):
            raise TypeError("Expected monitor on the interface but got %s" %
                            (monitor.__class__.__name__))

        if compare_fn is not None:
            if callable(compare_fn):
                monitor.add_callback(compare_fn)
                return
            raise TypeError("Expected a callable compare function but got %s" %
                            str(type(compare_fn)))

        self.log.info("Created with reorder_depth %d" % reorder_depth)
        
        def check_received_transaction(transaction):
            """Called back by the monitor when a new transaction has been
            received"""

            if monitor.name:
                log_name = self.log.name + '.' + monitor.name
            else:
                log_name = self.log.name + '.' + monitor.__class__.__name__

            log = logging.getLogger(log_name)

            if callable(expected_output):
                exp = expected_output(transaction)

            elif len(expected_output):
                # for i in range(min((reorder_depth + 1), len(expected_output))):
                #     if expected_output[i] == transaction:
                #         break
                # else:
                #     i = 0
                exp = expected_output.pop(0)
            else:
                self.errors += 1
                log.error("Received a transaction but wasn't expecting "
                          "anything")
                log.info("Got: %s" % (hexdump(str(transaction))))
                if self._imm:
                    raise TestFailure("Received a transaction but wasn't "
                                      "expecting anything")
                return

            self.compare(transaction, exp, log, strict_type=strict_type)

        monitor.add_callback(check_received_transaction)
