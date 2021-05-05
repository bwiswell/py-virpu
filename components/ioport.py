from pygame import Surface

from ..panels.panel import Panel
from ..signal.signal import Signal
from ..ui.theme import Theme

class IOPort(Panel):
    '''
    Class to represent IO ports that extends Panel.

    Attributes:
        id (str): a short name for the port
        type (str): data type ('address', 'any', 'control', or 'data')
        dir (str): port IO direction ('in' or 'out')
        width (int): bit-width of IO signal
        signed (bool): signage of IO signal
        value (Signal): current value in IO port
    '''

    SIZE = (100, 30)

    def __init__(self, 
                    id:str,
                    type:str,
                    dir:str,
                    width:int=32,
                    signed:bool=True
                ):
        '''
        Initialize IO port object and extend Panel.
        
        Parameters:
            id: a short name for the port
            type: data type ('address', 'any', 'control', or 'data')
            dir: port IO direction ('in' or 'out')
            width (int): bit-width of IO signal (default 32)
            signed (bool): signage of IO signal (default True)
        '''
        Panel.__init__(self, [id], size=IOPort.SIZE)
        self.id = id
        self.type = type
        self.dir = dir
        self._width = width
        self._signed = signed
        self._value = Signal(width=width, signed=signed)

    def zero(self) -> None:
        '''Zero out the value of the IO port.'''
        self._value = Signal(width=self._width, signed=self._signed)

    @property
    def width(self) -> int:
        '''Get or set bit width of the IO port.'''
        return self._width

    @width.setter
    def width(self, val:int) -> None:
        self._width = max(1, min(32, val))
        self.zero()

    @property
    def signed(self) -> bool:
        '''Get or set the signage of the IO port.'''
        return self._signed

    @signed.setter
    def signed(self, val:bool) -> None:
        self._signed = val
        self.zero()

    @property
    def value(self) -> Signal:
        '''Get or set the current value of the IO port.'''
        return self._value

    @value.setter
    def value(self, val:Signal):
        if val.width == self._width and val.signed == self._signed:
            self._value = val

    def render(self, buffer:Surface, theme:Theme) -> None:
        '''
        Override Panel render method to show value on hover.
        
        Parameters:
            buffer: the pygame surface to render on to
            theme: the color and layout scheme to use for rendering
        '''
        if self._hovered:
            content = theme.medium_text(self._value)
        else:
            content = theme.medium_text(self.id)
        super().render(
            buffer,
            theme,
            active=self._hovered,
            render_label=False
        )
        content_x = self._rect.centerx - content.get_width() // 2
        content_y = self._rect.centery - content.get_height() // 2
        buffer.blit(content, (content_x, content_y))