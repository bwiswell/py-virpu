from .component import Component
from .ioport import IOPort
from ..corium import corium
from ..signal.signal import Signal

class ControlUnit(Component):
    '''
    A class to represent a control unit that extends Component.
    
    This class is a functional logic component that splits an opcode into its
    control bits.

    Attributes:
        data (List[Signal]): the control bits corresponding to each opcode
    '''

    OPCODES = 16

    def __init__(self):
        '''Initialize ControlUnit object and extend Component.'''
        in_ports = [IOPort('opcode', 'address', 'in', 8, False)]
        reg_w_port = IOPort('reg-w-con', 'control', 'out', 1, False)
        alu_a_port = IOPort('alu-a-src', 'control', 'out', 1, False)
        alu_b_port = IOPort('alu-b-src', 'control', 'out', 2, False)
        alu_op_port = IOPort('alu-op', 'control', 'out', 4, False)
        branch_port = IOPort('branch', 'control', 'out', 1, False)
        mem_w_port = IOPort('mem-w', 'control', 'out', 1, False)
        wrt_src_port = IOPort('wrt-src', 'control', 'out', 1, False)
        out_ports = [
                    reg_w_port,
                    alu_a_port,
                    alu_b_port,
                    alu_op_port,
                    branch_port,
                    mem_w_port,
                    wrt_src_port
                ]

        Component.__init__(self,
                            comp_name='Control Unit',
                            in_ports=in_ports,
                            out_ports=out_ports
                        )

        raw_bitarrays = corium.get_control_bits()
        self._data = []
        for bitarray in raw_bitarrays:
            self._data.append(Signal(bitarray, 11, False))
        
    def _execute(self) -> None:
        '''
        Execute the control unit's function logic.

        The control unit splits an opcode into its control bits.
        '''
        address = self.in_by_id['opcode'].value
        data = self._data[address.value]

        reg_w = Signal(data[:1], 1, False)
        self.out_by_id['reg-w-con'].value = reg_w

        alu_a = Signal(data[1:2], 1, False)
        self.out_by_id['alu-a-src'].value = alu_a

        alu_b = Signal(data[2:4], 2, False)
        self.out_by_id['alu-b-src'].value = alu_b

        alu_op = Signal(data[4:8], 4, False)
        self.out_by_id['alu-op'].value = alu_op

        branch = Signal(data[8:9], 1, False)
        self.out_by_id['branch'].value = branch

        mem_w = Signal(data[9:10], 1, False)
        self.out_by_id['mem-w'].value = mem_w

        wrt_src = Signal(data[10:], 1, False)
        self.out_by_id['wrt-src'].value = wrt_src