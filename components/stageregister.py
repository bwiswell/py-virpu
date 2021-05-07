from .component import Component
from .ioport import IOPort

class StageRegister(Component):
    '''
    A class to represent an interstage register that extends Component.

    This class is a functional logic component that temporarily stores data
    and control bits between stages.

    Attributes:
        n_inputs (int): the number of values the register should store and pass
    '''

    def __init__(self):
        '''Initialize the StageRegister object and extend Component.'''
        Component.__init__(self,
                            comp_name='Interstage',
                            config_options='np'
                        )

        self._n_inputs = 0

    @property
    def n_inputs(self) -> int:
        '''Get or set the number of inputs.'''
        return self._n_inputs

    @n_inputs.setter
    def n_inputs(self, val:int) -> None:
        n = self._n_inputs
        self._n_inputs = max(0, min(32, val))
        while n < self._n_inputs:
            port_id = f'data-{n}'
            in_port = IOPort(port_id, 'any', 'in')
            self._add_port(in_port)
            out_port = IOPort(port_id, 'any', 'out')
            self._add_port(out_port)
            n += 1
        while n > self._n_inputs:
            n -= 1
            in_port = self.in_ports[0]
            self._remove_port(in_port)
            out_port = self.out_by_id[in_port.id]
            self._remove_port(out_port)

    def add_interstage_port(self, 
                            port_id:str, 
                            width:int=32, 
                            signed:bool=True
                            ) -> None:
        '''
        Add both inbound and outbound ports of custom name, width, and signage.
        
        Parameters:
            port_id: The ID that identifies both in and out ports
            width: The bit-width of the in and out ports
            signed: The signage of the in and out ports
        '''
        in_port = IOPort(port_id, 'any', 'in', width, signed)
        self._add_port(in_port)
        out_port = IOPort(port_id, 'any', 'out', width, signed)
        self._add_port(out_port)
        self._n_inputs = self._ins

    def _execute(self) -> None:
        '''Execute the interstage register's functional logic.

        The interstage register saves and passes through data between
        processor stages.
        '''
        for port_id, in_port in self.in_by_id.items():
            self.out_by_id[port_id].value = in_port.value