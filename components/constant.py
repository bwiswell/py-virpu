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
        data_port = IOPort('data', 'any')
        config_labels = ['Bit Length?', 'Signed?']
        config_options = [[4, 8, 16, 32], ['signed', 'unsigned']]
        config_getters = [self.get_data_width, self.get_signed_str]
        config_setters = [self.set_data_width, self.set_signed_str]
        config = Configuration(config_labels, config_options, config_getters, config_setters)
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
        return self.get_output_value('data')

    def get_data_width(self) -> int:
        return self.value.data_width

    def get_signed_str(self) -> str:
        return self.value.get_signed_str()

    def set_value(self, value:Signal) -> None:
        self.set_output_value('data', value)

    def set_data_width(self, data_width:int) -> None:
        self.out_by_id['data'].set_data_width(data_width)
        self.value = self.out_by_id['data'].get_value()

    def set_signed_str(self, signed_str:str) -> None:
        self.out_by_id['data'].set_signed_str(signed_str)
        self.value = self.out_by_id['data'].get_value()