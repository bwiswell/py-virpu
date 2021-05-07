from .component import Component
from .ioport import IOPort
from ..signal.signal import Signal

class ALU(Component):
    '''
    A class to represent an ALU that extends Component.
    
    This class is a functional logic component that performs logical and 
    arithmatic functions on two incoming values.
    '''
    
    def __init__(self):
        '''Initialize the ALU object and extend Component.'''
        in_a = IOPort('data-a', 'data', 'in')
        in_b = IOPort('data-b', 'data', 'in')
        con_port = IOPort('alu-op', 'control', 'in', 4, False)
        in_ports = [in_a, in_b, con_port]
        zero_flag = IOPort('zero-flag', 'control', 'out', 1, False)
        flow_flag = IOPort('flow-flag', 'control', 'out', 1, False)
        data_port = IOPort('data', 'data', 'out')
        out_ports = [zero_flag, flow_flag, data_port]
        Component.__init__(self,
                            comp_name='ALU',
                            in_ports=in_ports,
                            out_ports=out_ports
                        )

    def _execute(self) -> None:
        '''
        Execute the ALU's function logic.

        The ALU performs logical and arithmatic functions on two incoming 
        values.
        '''
        op = self.in_by_id['alu-op'].value.value
        data_a = self.in_by_id['data-a'].value
        data_b = self.in_by_id['data-b'].value

        value = Signal()
        flag = Signal.from_bool(False)
        if op == 0:
            value = data_a & data_b
        elif op == 1:
            value = data_a | data_b
        elif op == 2:
            value, overflow = data_a + data_b
            flag = Signal.from_bool(overflow)
        elif op == 10:
            value = ~data_a
        elif op == 14:
            value, underflow = data_a - data_b
            flag = Signal.from_bool(underflow)
        elif op == 15:
            if data_a.value < data_b.value:
                value = Signal.from_value(1)

        zero = Signal.from_bool(not value)

        self.out_by_id['data'].value = value
        self.out_by_id['zero-flag'].value = zero
        self.out_by_id['flow-flag'].value = flag
            