from typing import Callable, List, Tuple

from pygame import Surface
from pygame.event import Event

from .panel import Panel
from ..ui.theme import Theme

class Button(Panel):
    '''
    A class to extend Panel to provide on-click functionality.

    Attributes:
        on_click (Callable[[Event], None]): Method to call upon click
    '''
    def __init__(self, label:object, on_click:Callable[[Event], None]):
        '''
        Initialize Button object and extend Panel.
        
        Parameters:
            label: the object that labels the button
            on_click: the method to call on a click event
        '''
        Panel.__init__(self, label)
        self._on_click = on_click

    def handle_click(self, event:Event) -> None:
        '''Extend Panel to handle a button click.'''
        super().handle_click(event)
        if event.button == 1:
            self._on_click(event)

    def render(self, buffer:Surface, theme:Theme, active:bool=False) -> None:
        '''
        Render panel on to the buffer using the theme.
        
        Parameters:
            buffer: the pygame surface to render on to
            theme: the color and layout scheme to use for rendering
            active: boolean indicating if the button is active (default False)
        '''
        super().render(buffer, theme, active=active or self._hovered)