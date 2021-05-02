

from .component import Component
from .ioport import IOPort
from ..corium import corium
from ..signal.signal import Signal

class Opdecoder(Component):

    NAME = 'Opdecoder'
    CYCLES = 1
    SIZE = (300, 400)

    OPCODES = 16

    def __init__(self):
        opcode_port = IOPort('opcode', 'address', 'in', 8, False)
        reg_w_port = IOPort('reg-w', 'control', 'out', 1, False)
        alu_a_port = IOPort('alu-a-src', 'control', 'out', 1, False)
        alu_b_port = IOPort('alu-b-src', 'control', 'out', 2, False)
        alu_op_port = IOPort('alu-op', 'control', 'out', 4, False)
        branch_port = IOPort('branch', 'control', 'out', 1, False)
        mem_w_port = IOPort('mem-w', 'control', 'out', 1, False)
        wrt_src_port = IOPort('wrt-src', 'control', 'out', 1, False)
        inputs = [opcode_port]
        outputs = [
                    reg_w_port,
                    alu_a_port,
                    alu_b_port,
                    alu_op_port,
                    branch_port,
                    mem_w_port,
                    wrt_src_port
                ]

        Component.__init__(self,
                            Opdecoder.NAME,
                            inputs,
                            outputs,
                            Opdecoder.CYCLES,
                            (0, 0),
                            Opdecoder.SIZE
                        )

        raw_bitarrays = corium.get_control_bits()
        self.data = []
        for bitarray in raw_bitarrays:
            self.data.append(Signal.from_bits(bitarray, 11, False))
        
    def execute(self) -> None:
        address = self.get_input_value('opcode')
        data = self.data[address.value]

        reg_w_bits = data[:1]
        reg_w_sig = Signal.from_bits(reg_w_bits, 1, False)
        self.set_output_value('reg-w', reg_w_sig)

        alu_a_bits = data[1:2]
        alu_a_sig = Signal.from_bits(alu_a_bits, 1, False)
        self.set_output_value('alu-a-src', alu_a_sig)

        alu_b_bits = data[2:4]
        alu_b_sig = Signal.from_bits(alu_b_bits, 2, False)
        self.set_output_value('alu-b-src', alu_b_sig)

        alu_op_bits = data[4:8]
        alu_op_sig = Signal.from_bits(alu_op_bits, 4, False)
        self.set_output_value('alu-op', alu_op_sig)

        branch_bits = data[8:9]
        branch_sig = Signal.from_bits(branch_bits, 1, False)
        self.set_output_value('branch', branch_sig)

        mem_w_bits = data[9:10]
        mem_w_sig = Signal.from_bits(mem_w_bits, 1, False)
        self.set_output_value('mem-w', mem_w_sig)

        wrt_src_bits = data[10:]
        wrt_src_sig = Signal.from_bits(wrt_src_bits, 1, False)
        self.set_output_value('wrt-src', wrt_src_sig)