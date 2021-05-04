from .component import Component
from .ioport import IOPort
from ..signal.signal import Signal

class LogicGate(Component):
    '''
    A class to represent a logic gate that extends Component.

    This is the base class for all bit-level logic gate components, and should
    not be directly instantiated.
    '''

    def __init__(self, comp_name:str, n_inputs:int=2):
        '''
        Initialize LogicGate object and extend Component.

        Parameters:
            comp_name: the name of the component
            n_inputs: the number of inputs to the logic gate (default 2)
        '''
        in_ports = [IOPort('data-a', 'any', 'in', 1, False)]
        if n_inputs > 1:
            in_ports.append(IOPort('data-b', 'any', 'in', 1, False))
        out_ports = [IOPort('data', 'any', 'out', 1, False)]

        Component.__init__(self,
                            comp_name=comp_name,
                            in_ports=in_ports,
                            out_ports=out_ports,
                        )



class AndGate(LogicGate):
    '''A class to represent an AND gate that extends LogicGate.'''

    def __init__(self):
        '''Initialize AndGate object and extend LogicGate.'''
        LogicGate.__init__(self, comp_name='AND')

    def execute(self) -> None:
        
        '''
        Execute the AND gate's functional logic.

        The AND gate sets its output to 1 if and only if both of its inputs are
        1.
        '''
        data_a = self.in_by_id['data-a']
        data_b = self.in_by_id['data-b']
        value = data_a.is_nonzero() and data_b.is_nonzero()
        data = Signal(int(value), 1, False)
        self.out_by_id['data'].value = data



class OrGate(LogicGate):
    '''A class to represent an OR gate that extends LogicGate.'''

    def __init__(self):
        '''Initialize OrGate object and extend LogicGate.'''
        LogicGate.__init__(self, comp_name='OR')

    def execute(self) -> None:
        
        '''
        Execute the OR gate's functional logic.

        The OR gate sets its output to 1 if either of its inputs are 1.
        '''
        data_a = self.in_by_id['data-a']
        data_b = self.in_by_id['data-b']
        value = data_a.is_nonzero() or data_b.is_nonzero()
        data = Signal(int(value), 1, False)
        self.out_by_id['data'].value = data