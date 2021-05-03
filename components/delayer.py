

from typing import IO
from .component import Component
from .ioport import IOPort
from ..panels.configuration import Configuration
from ..signal.signal import Signal

class Delayer(Component):

    NAME = 'Delayer'
    DEF_CYCLES = 4

    def __init__(self):
        in_port = IOPort('data', 'any', 'in')
        out_port = IOPort('data', 'any', 'out')
        
        config_labels = [
                            'Delay', 
                            'Bits', 
                            'Signed'
                        ]
        config_options = [
                            ['-', '+'], 
                            ['-', '+'], 
                            [True, False]
                        ]
        config_getters = [
                            self.get_cycles, 
                            self.get_data_width, 
                            self.get_signed
                        ]
        config_setters = [
                            self.incr_cycles,
                            self.incr_data_width,
                            self.set_signed
                        ]
        config = Configuration(
                                config_labels,
                                config_options,
                                config_getters,
                                config_setters
                            )

        Component.__init__(self,
                            Delayer.NAME,
                            [in_port],
                            [out_port],
                            Delayer.DEF_CYCLES,
                            config
                        )

    
    def get_data_width(self) -> int:
        return self.in_ports[0].data_width

    def get_signed(self) -> bool:
        return self.in_ports[0].get_signed()

    def incr_data_width(self, dir:str) -> None:
        if dir == '-':
            new_dw = max(1, self.get_data_width() - 1)
        else:
            new_dw = min(32, self.get_data_width() + 1)
        self.in_by_id['data'].set_data_width(new_dw)
        self.out_by_id['data'].set_data_width(new_dw)

    def set_signed(self, signed:bool) -> None:
        self.in_by_id['data'].set_signed(signed)
        self.out_by_id['data'].set_signed(signed)

    def execute(self) -> None:
        data = self.get_input_value('data')
        self.set_output_value('data', data)