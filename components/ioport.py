from typing import Tuple

from ..panels.hoverpanel import HoverPanel
from ..signal.signal import Signal

class IOPort(HoverPanel):

    SIZE = (100, 50)

    def __init__(self, 
                    port_id:str,
                    port_type:str,
                    data_width:int=32
                ):
        HoverPanel.__init__(self, [port_id], [self.get_value], size=IOPort.SIZE)
        self.port_id = port_id
        self.port_type = port_type
        self.data_width = data_width
        self.value = Signal(value=0, data_width=data_width)

    def get_value(self) -> Signal:
        return self.value

    def set_value(self, value:Signal) -> None:
        self.value = value