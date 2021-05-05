from typing import Callable

from pygame import Surface

from .panel import Panel
from ..ui.theme import Theme

class ValuePanel(Panel):
    '''
    A class to extend Panel for showing current variable values.

    Attributes:
        value_getter (Callable[[], object]): Method to update current value
    '''

    def __init__(self, label:object, value_getter:Callable[[], object]):
        '''
        Initialize the ValuePanel object and extend Panel.
        
        Parameters:
            label: the object that labels the panel
            value_getter: the method to update the current value
        '''
        Panel.__init__(self, label)
        self._value_getter = value_getter

    def render(self, buffer:Surface, theme:Theme):
        '''
        Render panel on to the buffer using the theme.
        
        Parameters:
            buffer: the pygame surface to render on to
            theme: the color and layout scheme to use for rendering
        '''
        super().render(buffer, theme, render_label=False)
        y_off = self._h // 3
        label = theme.large_text(self._label)
        label_x = self._rect.centerx - label.get_width() // 2
        label_y = self._y + y_off - label.get_height() // 2
        buffer.blit(label, (label_x, label_y))
        value = theme.medium_text(self._value_getter())
        value_x = self._rect.centerx - value.get_width() // 2
        value_y = self._y + 2 * y_off - value.get_height() // 2
        buffer.blit(value, (value_x, value_y))