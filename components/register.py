

from .component import Component
from .ioport import IOPort
from ..signal.signal import Signal

class Register(Component):

    NAME = 'Register Bank'
    CYCLES = 4

    REGISTERS = 16

    def __init__(self):
        reg_w_con = IOPort('reg-w-con', 'control', 'in', 1, False)
        reg_a_port = IOPort('reg-a', 'control', 'in', 4, False)
        reg_b_port = IOPort('reg-b', 'control', 'in', 4, False)
        reg_w_port = IOPort('reg-w', 'control', 'in', 4, False)
        data_w_port = IOPort('data-w', 'data', 'in')
        data_a_port = IOPort('data-a', 'data', 'out')
        data_b_port = IOPort('data-b', 'data', 'out')

        inputs = [reg_w_con, reg_a_port, reg_b_port, reg_w_port, data_w_port]
        outputs = [data_a_port, data_b_port]

        Component.__init__(self,
                            Register.NAME,
                            inputs,
                            outputs,
                            Register.CYCLES,
                        )

        self.data = [Signal(0) for _ in range(Register.REGISTERS)]

    def execute(self) -> None:
        reg_a = self.get_input_value('reg-a')
        data = self.data[reg_a.value]
        self.set_output_value('data-a', data)
        reg_b = self.get_input_value('reg-b')
        data = self.data[reg_b.value]
        self.set_output_value('data-b', data)
        if self.get_input_value('reg-w-con').is_nonzero():
            reg_w = self.get_input_value('reg-w')
            data = self.get_input_value('data-w')
            self.data[reg_w] = data