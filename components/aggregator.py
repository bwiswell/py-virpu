from bitarray import bitarray

from .component import Component
from .ioport import IOPort
from ..signal.signal import Signal

class Aggregator(Component):
    '''
    Class to represent a bit aggregator that extends Component.

    This class is a functional component that has 0 < n <= 32 1-bit unsigned
    input ports which are combined into a single n-bit (un)signed output port.
    No logic is performed on the individual bit signals.
    '''

    def __init__(self):
        '''Initialize Aggregator object and extend Component'''
        in_ports = [IOPort('bit-0', 'any', 'in', 1, False)]
        out_ports = [IOPort('data', 'any', 'out', 1, False)]

        Component.__init__(self,
                            comp_name='Aggregator',
                            in_ports=in_ports,
                            out_ports=out_ports,
                            config_options='ws'
                        )

        self._width = 1
        self.signed = False

    def _get_width(self) -> int:
        '''Get the bit width of the component.'''
        return super()._get_width()

    def _set_width(self, val:int) -> None:
        '''Set the bit width of the component.'''
        w = self._width
        super()._set_width(val)
        self.out_by_id['data'].width = self._width
        while w < self._width:
            port_id = f'bit-{w}'
            port = IOPort(port_id, 'any', 'in', 1, False)
            self._add_port(port)
            w += 1
        while w > self._width:
            w -= 1
            port_id = f'bit-{w}'
            port = self.in_by_id[port_id]
            self._remove_port(port)

    width = property(_get_width, _set_width)

    def _get_signed(self) -> bool:
        '''Get the signage of the component.'''
        return super()._get_signed()

    def _set_signed(self, val:bool) -> None:
        '''Set the signage of the component.'''
        super()._set_signed(val)
        self.out_by_id['data'].signed = val

    signed = property(_get_signed, _set_signed)

    def _execute(self) -> None:
        '''
        Execute the aggregator's functional logic.

        The aggregator combines n 1-bit unsigned inputs into one n-bit
        (un)signed output without performing any bit logic on the inputs.
        '''
        bits = bitarray(self._width)
        for i in range(self._width):
            bits[i] = self.in_ports[i].value[0]
        value = Signal(bits, self._width, self._signed)
        self.out_by_id['data'].value = value