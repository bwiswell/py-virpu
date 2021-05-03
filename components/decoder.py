from .component import Component
from .ioport import IOPort
from ..corium import corium
from ..signal.signal import Signal

class Decoder(Component):

    NAME = 'Decoder'
    CYCLES = 1

    def __init__(self):
        ins_port = IOPort('ins', 'data', 'in', 32, False)
        opcode_port = IOPort('opcode', 'address', 'out', 8, False)
        reg_a_port = IOPort('reg-a', 'control', 'out', 4, False)
        reg_b_port = IOPort('reg-b', 'control', 'out', 4, False)
        reg_w_port = IOPort('reg-w', 'control', 'out', 4, False)
        imm_port = IOPort('imm', 'data', 'out', 16)

        inputs = [ins_port]
        outputs = [
                    opcode_port,
                    reg_a_port,
                    reg_b_port,
                    reg_w_port,
                    imm_port
                ]

        Component.__init__(self,
                            Decoder.NAME,
                            inputs,
                            outputs,
                            Decoder.CYCLES,
                        )
        
    def execute(self) -> None:
        ins = self.get_input_value('ins')
        opcode = Signal.from_bits(ins[:8], 8, False)
        self.set_output_value('opcode', opcode)
        args = corium.get_arg_dests(opcode.value)

        curr_bit = 8
        for port in self.out_ports[1:]:
            if port.port_id in args:
                port_type = port.port_id.split('-')[0]
                arg_w = 16 if port_type == 'imm' else 4
                arg_bits = ins[curr_bit:curr_bit + arg_w]
                curr_bit += arg_w
                out_sig = Signal.from_bits(arg_bits, arg_w, False)
                port.set_value(out_sig)
            else:
                data_w = port.data_width
                out_sig = Signal(0, data_w, False)
                port.set_value(out_sig)