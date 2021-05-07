from bitarray import bitarray

from .component import Component
from .ioport import IOPort
from ..signal.signal import Signal

class LeftShifter(Component):
    '''
    A class to represent a left shift module that extends Component.

    This class is a functional component that extends a 16-bit signed
    immediate into a 32-bit signed value by shifting it left 16 bits.
    '''

    def __init__(self):
        '''Initialize the LeftShifter object and extend Component.'''
        in_ports = [IOPort('imm', 'data', 'in', 16)]
        out_ports = [IOPort('data', 'data', 'out')]
        Component.__init__(self,
                            comp_name='Left Shifter',
                            in_ports=in_ports,
                            out_ports=out_ports,
                        )

    def _execute(self) -> None:
        '''
        Execute the left shifter's function logic.

        The left shifter extends a 16-bit signed immediate into a 32-bit
        signed value by shifting it left 16 bits.
        '''
        zeros = bitarray(16)
        zeros.setall(0)
        bits = self.in_by_id['imm'].value.bits + zeros
        value = Signal(bits)
        self.out_by_id['data'].value = value



class SignExtender(Component):
    '''
    A class to represent a sign extension module that extends Component.

    This class is a functional component that extends a 16-bit signed
    immediate into a 32-bit signed value by replicating its sign bit.
    '''

    def __init__(self):
        '''Initialize the SignExtender object and extend Component.'''
        in_ports = [IOPort('imm', 'data', 'in', 16)]
        out_ports = [IOPort('data', 'data', 'out')]
        Component.__init__(self,
                            comp_name='Sign Extender',
                            in_ports=in_ports,
                            out_ports=out_ports,
                        )

    def _execute(self) -> None:
        '''
        Execute the sign extender's function logic.

        The sign extender extends a 16-bit signed immediate into a 32-bit
        signed value by replicating its sign bit.
        '''
        dec_val = self.in_by_id['imm'].value.value
        value = Signal.from_value(dec_val)
        self.out_by_id['data'].value = value