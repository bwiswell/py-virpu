from typing import List

from bitarray import bitarray

from .component import Component
from .ioport import IOPort
from ..signal.signal import Signal

class Memory(Component):

    NAME = 'Memory'
    CYCLES = 4
    SIZE = (300, 400)

    DEF_MEM = 65536
    MAX_MEM = 65536

    def __init__(self):
        address_port = IOPort('address', 'address', 'in', 16, False)
        data_port = IOPort('data', 'data', 'out')
        Component.__init__(self,
                            Memory.NAME,
                            [address_port],
                            [data_port],
                            Memory.CYCLES,
                            (0, 0),
                            Memory.SIZE
                        )
        self.data = [Signal(value=i) for i in range(Memory.DEF_MEM)]

    def load_program(self, program:List[bitarray]) -> None:
        self.get_out_port('data').set_signed(False)
        signals = [Signal.from_bits(bitarr, signed=False) for bitarr in program]
        rem_mem = Memory.MAX_MEM - len(signals)
        signals.extend([Signal(value=i, signed=False) for i in range(rem_mem)])
        self.data = signals
        
    def execute(self) -> None:
        address = self.get_input_value('address')
        data = self.data[address.value]
        self.set_output_value('data', data)