from .component import Component
from .ioport import IOPort
from ..panels.configuration import Configuration
from ..signal.signal import Signal

class Counter(Component):

    NAME = 'Counter'
    CYCLES = 4

    def __init__(self):
        out_port = IOPort('data', 'any', 'out', 16, False)
        config_labels = [
                            'Bits',
                            'Signed'
                        ]
        config_options = [
                            ['-', '+'],
                            [True, False]
                        ]   
        config_getters = [
                            self.get_data_width,
                            self.get_signed
                        ]
        config_setters = [
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
                            Counter.NAME,
                            [],
                            [out_port],
                            Counter.CYCLES,
                            config
                        )
        
        self.value = 0

    def get_data_width(self) -> int:
        return self.out_ports[0].data_width

    def get_signed(self) -> bool:
        signed = self.out_ports[0].get_signed()
        print(signed)
        return signed

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
        data = Signal(self.value, self.get_data_width(), self.get_signed())
        self.set_output_value('data', data)
        self.value += 1