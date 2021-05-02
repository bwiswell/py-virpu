from typing import Tuple

from .component import Component
from .ioport import IOPort
from ..panels.configuration import Configuration
from ..signal.signal import Signal


class Constant(Component):

    NAME = 'Constant'
    CYCLES = 1
    SIZE = (300, 200)

    def __init__(self):
        data_port = IOPort('data', 'any', 'out')
        config_labels = [
                            'Bits', 
                            'Signed', 
                            'Value'
                        ]
        config_options = [
                            ['-', '+'], 
                            [True, False], 
                            ['-', '+']
                        ]
        config_getters = [
                            self.get_data_width, 
                            self.get_signed, 
                            self.get_value
                        ]
        config_setters = [
                            self.incr_data_width, 
                            self.set_signed,
                            self.incr_value
                        ]
        config = Configuration(
                                config_labels, 
                                config_options, 
                                config_getters, 
                                config_setters)
        Component.__init__(self,
                            Constant.NAME,
                            [],
                            [data_port],
                            Constant.CYCLES,
                            (0, 0),
                            Constant.SIZE,
                            config
                        )
        self.value = Signal()

    def get_value(self) -> Signal:
        return self.value

    def get_data_width(self) -> int:
        return self.value.data_width

    def get_signed(self) -> bool:
        return self.value.get_signed()

    def incr_value(self, dir:str) -> None:
        self.value.incr_val(dir)

    def incr_data_width(self, dir:str) -> None:
        if dir == '-':
            new_dw = max(1, self.get_data_width() - 1)
        else:
            new_dw = min(32, self.get_data_width() + 1)
        self.out_by_id['data'].set_data_width(new_dw)
        self.value = self.get_output_value('data')

    def set_signed(self, signed:bool) -> None:
        self.out_by_id['data'].set_signed(signed)
        self.value = self.get_output_value('data')

    def execute(self) -> None:
        self.set_output_value('data', self.value)