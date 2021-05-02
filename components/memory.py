from __future__ import annotations
from typing import Tuple

from pygame.event import Event

from .component import Component
from .ioport import IOPort
from ..signal.signal import Signal

class Memory(Component):

    NAME = 'Memory'
    CYCLES = 4
    SIZE = (300, 400)

    DEF_MEM = 65536
    MAX_MEM = 65536

    def __init__(self, pos:Tuple[int, int]=(0, 0)):
        address_port = IOPort('address', 'address', 16)
        data_port = IOPort('data', 'data')
        Component.__init__(self,
                            Memory.NAME,
                            [address_port],
                            [data_port],
                            Memory.CYCLES,
                            pos,
                            Memory.SIZE
                        )
        self.data = [Signal(value=i) for i in range(Memory.DEF_MEM)]
        
    def execute(self) -> None:
        address = self.get_input_value('address')
        return self.data[address.value]