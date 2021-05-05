from .component import Component
from .ioport import IOPort
from ..corium import corium
from ..signal.signal import Signal

class Decoder(Component):
    '''
    A class to represent an instruction decoder that extends Component.

    This class is a functional logic component that splits an instruction into
    its opcode and arguments.
    '''

    def __init__(self):
        '''Initialize the Decoder object and extend Component.'''
        ins_port = IOPort('ins', 'data', 'in', 32, False)
        opcode_port = IOPort('opcode', 'address', 'out', 8, False)
        reg_a_port = IOPort('reg-a', 'control', 'out', 4, False)
        reg_b_port = IOPort('reg-b', 'control', 'out', 4, False)
        reg_w_port = IOPort('reg-w', 'control', 'out', 4, False)
        imm_port = IOPort('imm', 'data', 'out', 16)

        in_ports = [ins_port]
        out_ports = [
                    opcode_port,
                    reg_a_port,
                    reg_b_port,
                    reg_w_port,
                    imm_port
                ]

        Component.__init__(self,
                            comp_name='Decoder',
                            in_ports=in_ports,
                            out_ports=out_ports
                        )
        
    def _execute(self) -> None:
        '''
        Execute the decoder's functional logic.

        The decoder splits an instruction into its opcode and arguments.
        '''
        ins = self.in_by_id['ins'].value
        opcode = Signal(ins[:8], 8, False)
        self.out_by_id['opcode'].value = opcode
        args = corium.get_arg_dests(opcode.value)

        curr_bit = 8
        for port in self.out_ports[1:]:
            if port.id in args:
                port_type = port.id.split('-')[0]
                arg_w = 16 if port_type == 'imm' else 4
                arg_bits = ins[curr_bit:curr_bit + arg_w]
                curr_bit += arg_w
                out_sig = Signal(arg_bits, arg_w, False)
                port.value = out_sig
            else:
                port.zero()