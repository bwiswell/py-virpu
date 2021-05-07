from .component import Component
from .ioport import IOPort
from ..signal.signal import Signal

class PCAdder(Component):
    '''
    A class to represent a program counter adder that extends Component.
    
    This class is a functional logic component that adds an offset to the
    program counter.
    '''
    
    def __init__(self):
        '''Initialize the PCAdder object and extend Component.'''
        in_a = IOPort('data-a', 'any', 'in', 16, False)
        in_b = IOPort('data-b', 'any', 'in', 16, True)
        in_ports = [in_a, in_b]
        out_ports = [IOPort('data', 'any', 'out', 16, False)]
        Component.__init__(self,
                            comp_name='PC Adder',
                            in_ports=in_ports,
                            out_ports=out_ports,
                        )

    def _execute(self) -> None:
        '''
        Execute the adder's function logic.

        The adder adds an offset to the program counter.
        '''
        val_a = self.in_by_id['data-a'].value.value
        val_b = self.in_by_id['data-b'].value.value
        value = Signal.from_value(val_a + val_b, 16, False)
        self.out_by_id['data'].value = value