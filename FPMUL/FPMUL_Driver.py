from cocotb.drivers import Driver

class FPMUL_Driver(Driver):
    def __init__(self, entity, name, clock, generator=None):
        Driver.__init__(self)
        self.generator = generator

    @coroutine
    def _driver_send(self, transaction, sync=True):
        sign, exponent, mantissa = self.generator()
        return IEEE(sign, exponent, mantissa)

