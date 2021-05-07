from .component import Component
from .ioport import IOPort

class Multiplexer(Component):
    '''
    A class to represent a multiplexer that extends Component.
    
    This class is a functional logic component selects a single input among
    multiple according to a control signal.
    '''

    MAX_IN = 4
    MIN_IN = 2

    def __init__(self):
        '''Initialize the MultiPlexer object and extend Component.'''
        in_ports = [IOPort('src', 'control', 'in', 1, False)]
        out_ports = [IOPort('data', 'any', 'out')]

        Component.__init__(self,
                            comp_name='Multiplexer',
                            in_ports=in_ports,
                            out_ports=out_ports,
                            config_options='nws'
                        )

        self._n_inputs = 0
        self.n_inputs = 2

    @property
    def n_inputs(self) -> int:
        '''Get or set the number of inputs.'''
        return self._n_inputs

    @n_inputs.setter
    def n_inputs(self, val:int) -> None:
        n = self._n_inputs
        self._n_inputs = max(Multiplexer.MIN_IN, min(Multiplexer.MAX_IN, val))
        con_w = 1 if self._n_inputs == 2 else 2
        self.in_by_id['src'].width = con_w
        while n < self._n_inputs:
            port_id = f'input-{n}'
            port = IOPort(port_id, 'any', 'in', self._width, self._signed)
            self._add_port(port)
            n += 1
        while n > self._n_inputs:
            n -= 1
            port_id = f'input-{n}'
            port = self.in_by_id[port_id]
            self._remove_port(port)

    def _get_width(self) -> int:
        '''Get the bit width of the component.'''
        return super()._get_width()

    def _set_width(self, val:int) -> None:
        '''Set the bit width of the component.'''
        super()._set_width(val)
        for in_port in self.in_ports[:self._n_inputs]:
            in_port.width = self._width
        self.out_by_id['data'].width = self._width

    width = property(_get_width, _set_width)

    def _get_signed(self) -> bool:
        '''Get the signage of the component.'''
        return super()._get_signed()

    def _set_signed(self, val:bool) -> None:
        '''Set the signage of the component.'''
        super()._set_signed(val)
        for in_port in self.in_ports[:self._n_inputs]:
            in_port.signed = val
        self.out_by_id['data'].signed = val

    signed = property(_get_signed, _set_signed)

    def _execute(self) -> None:
        '''
        Execute the multiplexer's functional logic.

        The multiplexer selects a single input among multiple according to a 
        control signal.
        '''
        address = self.in_by_id['src'].value.value
        value = self.in_by_id[f'input-{address}'].value
        self.out_by_id['data'].value = value