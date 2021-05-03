from .logicgate import LogicGate
from ..signal.signal import Signal

class AndGate(LogicGate):

    NAME = 'AND'

    def __init__(self):
        LogicGate.__init__(self, AndGate.NAME)

    def execute(self) -> None:
        data_a = self.get_input_value('data-a')
        data_b = self.get_input_value('data-b')
        value = data_a.is_nonzero() and data_b.is_nonzero()
        data = Signal(int(value), 1, False)
        self.set_output_value('data', data)