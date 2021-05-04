from .component import Component
from .ioport import IOPort
from ..signal.signal import Signal

class Register(Component):
    '''
    A class to represent a register bank that extends Component.
    
    This class is a functional logic component that retrieves data at a given
    memory address.

    Attributes:
        data (List[Signal]): the register contents indexed by register address
    '''

    REGISTERS = 16

    def __init__(self):
        '''Initialize the Register object and extend Component.'''
        reg_w_con = IOPort('reg-w-con', 'control', 'in', 1, False)
        reg_a_port = IOPort('reg-a', 'control', 'in', 4, False)
        reg_b_port = IOPort('reg-b', 'control', 'in', 4, False)
        reg_w_port = IOPort('reg-w', 'control', 'in', 4, False)
        data_w_port = IOPort('data-w', 'data', 'in')
        data_a_port = IOPort('data-a', 'data', 'out')
        data_b_port = IOPort('data-b', 'data', 'out')

        in_ports = [
                        reg_w_con, 
                        reg_a_port, 
                        reg_b_port, 
                        reg_w_port, 
                        data_w_port
                    ]
        out_ports = [data_a_port, data_b_port]

        Component.__init__(self,
                            comp_name='Register Bank',
                            in_ports=in_ports,
                            out_ports=out_ports,
                            cycles=4,
                            config_options='t'
                        )

        self._data = [Signal(0) for _ in range(Register.REGISTERS)]

    def execute(self) -> None:
        '''
        Execute the memory's functional logic.

        The register bank retrieves data at a given register address.
        '''
        reg_a_add = self.in_by_id['reg-a'].value
        reg_a_val = self._data[reg_a_add.value]
        self.out_by_id['data-a', reg_a_val]

        reg_b_add = self.in_by_id['reg-b'].value
        reg_b_val = self._data[reg_b_add.value]
        self.out_by_id['data-b', reg_b_val]

        if self.in_by_id['reg-w-con'].value:
            reg_w_add = self.in_by_id['reg-w']
            reg_w_val = self.in_by_id['data-w']
            self._data[reg_w_add.value] = reg_w_val