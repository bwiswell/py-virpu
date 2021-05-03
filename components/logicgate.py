

from .component import Component
from .ioport import IOPort
from ..signal.signal import Signal

class LogicGate(Component):

    CYCLES = 1

    def __init__(self, name:str, n_inputs:int=2):
        inputs = []
        inputs.append(IOPort('data-a', 'any', 'in', 1, False))
        if n_inputs > 1:
            inputs.append(IOPort('data-b', 'any', 'in', 1, False))
        outputs = [IOPort('data', 'any', 'out', 1, False)]

        Component.__init__(self,
                            name,
                            inputs,
                            outputs,
                            LogicGate.CYCLES,
                        )