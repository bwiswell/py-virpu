from bitarray import bitarray

from .component import Component
from .ioport import IOPort
from ..panels.configuration import Configuration
from ..signal.signal import Signal

class Aggregator(Component):

    NAME = 'Aggregator'
    CYCLES = 1

    def __init__(self):
        in_port = IOPort('bit-0', 'any', 'in', 1, False)
        out_port = IOPort('data', 'any', 'out', 1, False)

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
                            self.incr_bits,
                            self.set_signed
                        ]
        
        config = Configuration(
                                config_labels,
                                config_options,
                                config_getters,
                                config_setters
                            )

        Component.__init__(self,
                            Aggregator.NAME,
                            [in_port],
                            [out_port],
                            Aggregator.CYCLES,
                            config
                        )

    def get_data_width(self) -> int:
        return self.get_out_port('data').data_width

    def incr_bits(self, dir:str) -> None:
        if dir == '-' and self.ins - 1 > 0:
            new_dw = self.ins - 1
            self.get_out_port('data').set_data_width(new_dw)
            port_id = f'bit-{new_dw}'
            port = self.get_in_port(port_id)
            self.remove_port(port)
        elif dir == '+' and self.ins + 1 <= 32:
            new_dw = self.ins + 1
            self.get_out_port('data').set_data_width(new_dw)
            port_id = f'bit-{self.ins}'
            port = IOPort(port_id, 'any', 'in', 1, False)
            self.add_port(port)

    def get_signed(self) -> bool:
        return self.get_out_port('data').get_signed()

    def set_signed(self, signed:bool) -> None:
        self.get_out_port('data').set_signed(signed)

    def execute(self) -> None:
        out_chr = ['1' if p.value.is_nonzero() else '0' for p in self.in_ports]
        out_str = ''.join(out_chr)
        out_bit = bitarray(out_str)
        out_sig = Signal.from_bits(
                                    out_bit, 
                                    self.get_data_width(),
                                    self.get_signed()
                                )
        self.set_output_value('data', out_sig)