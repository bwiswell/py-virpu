from ..panels.configuration import Configuration
from ..panels.hoverpanel import HoverPanel
from ..signal.signal import Signal

class IOPort(HoverPanel):

    SIZE = (100, 50)

    def __init__(self, 
                    port_id:str,
                    port_type:str,
                    port_dir:str,
                    data_width:int=32,
                    signed:bool=True
                ):
        HoverPanel.__init__(
                            self, 
                            [port_id], 
                            [self.get_value], 
                            size=IOPort.SIZE
                        )
        self.port_id = port_id
        self.port_type = port_type
        self.port_dir = port_dir
        self.data_width = data_width
        self.value = Signal(0, data_width, signed)
        self.configuration = Configuration()

    def get_configuration(self) -> Configuration:
        return self.configuration

    def get_signed(self) -> bool:
        return self.value.signed

    def get_value(self) -> Signal:
        return self.value

    def set_data_width(self, data_width:int) -> None:
        self.data_width = data_width
        self.value = Signal(0, data_width, self.value.signed)

    def set_signed(self, signed:bool) -> None:
        self.value = Signal(0, self.data_width, signed)

    def set_signed_str(self, signed_str:str) -> None:
        signed = signed_str == 'signed'
        self.set_signed(signed)

    def set_value(self, value:Signal) -> None:
        self.value = value