from typing import List, Tuple

from pygame import Surface
from pygame.event import Event

from .panel import Panel
from ..ui.theme import Theme

class CyclePanel(Panel):
    '''
    A class to extend Panel to allow for multiple slides per panel that can
    be cycled through with right clicks.

    Attributes:
        panels (List[Panel]): The slides of the CyclePanel
        curr_slide (int): The currently displayed slide
    '''

    def __init__(self, label:str, panels:List[Panel]):
        '''
        Initialize the CyclePanel object and extend Panel.

        Parameters:
            label: The object that labels the CyclePanel
        '''
        Panel.__init__(self, label=label)
        self._panels = panels
        self._curr_slide = 0

    def _get_pos(self) -> Tuple[int, int]:
        '''Get the position of the panel's top-left corner.'''
        return super()._get_pos()

    def _set_pos(self, val:Tuple[int, int]) -> None:
        '''Set the position of the panel's top-left corner.'''
        super()._set_pos(val)
        for panel in self._panels:
            panel.pos = val

    pos = property(_get_pos, _set_pos)

    def _get_size(self) -> Tuple[int, int]:
        '''Get the size of the panel.'''
        return super()._get_size()

    def _set_size(self, val:Tuple[int, int]) -> None:
        '''Set the size of the panel.'''
        super()._set_size(val)
        for panel in self._panels:
            panel.size = val

    size = property(_get_size, _set_size)

    def handle_click(self, event:Event) -> None:
        '''Override Panel to handle a click interaction with the panel.'''
        if event.button == 3:
            self._curr_slide = (self._curr_slide + 1) % len(self._panels)
        elif event.button == 1:
            self._panels[self._curr_slide].handle_click(event)

    def handle_hover(self, mouse_pos:Tuple[int, int]) -> None:
        '''Override Panel to handle a hover interaction with the panel.'''
        self._panels[self._curr_slide].handle_hover(mouse_pos)

    def render(self, buffer:Surface, theme:Theme) -> None:
        '''
        Override Panel to render current slide to the buffer.

        Parameters:
            buffer: the pygame surface to render on to
            theme: the color and layout scheme to use for rendering
        '''
        self._panels[self._curr_slide].render(buffer, theme)