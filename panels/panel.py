from typing import Tuple

from pygame import draw, Rect, Surface
from pygame.event import Event

from ..ui.theme import Theme

class Panel:
    '''
    A class to represent an interactable UI panel.

    Attributes:
        x (int): The x-coordinate of the panel's top-left corner
        y (int): The y-coordinate of the panel's top-left corner
        pos (Tuple[int, int]): The position of the panel's top-left corner
        w (int): The width of the panel
        h (int): The height of the panel
        size (Tuple[int, int]): The size of the panel
        rect (Rect): The rect that describes the area occupied by the panel
        label (object): The object that labels the panel
        hovered (bool): A flag indicating if the mouse is over the panel
    '''
    def __init__(self, 
                    label:object, 
                    pos:Tuple[int, int]=(0,0), 
                    size:Tuple[int, int]=(0,0)
                ):
        '''
        Initialize the Panel object.
        
        Attributes:
            label: The object that labels the panel
            pos: The position of the panel's top-left corner (default (0, 0))
            size: The size of the panel (default (0, 0))
        '''
        self._x, self._y = pos
        self._pos = pos
        self._w, self._h = size
        self._size = size
        self._rect = Rect(pos, size)
        self._label = label
        self._hovered = False

    def _get_pos(self) -> Tuple[int, int]:
        '''Get the position of the panel's top-left corner.'''
        return self._pos

    def _set_pos(self, val:Tuple[int, int]) -> None:
        '''Set the position of the panel's top-left corner.'''
        self._x, self._y = val
        self._pos = val
        self._rect = Rect(val, self._size)

    pos = property(_get_pos, _set_pos)

    def center_on(self, center:Tuple[int, int]) -> None:
        '''Center the panel on a position.'''
        x = center[0] - self._w // 2
        y = center[1] - self._h // 2
        self.pos = x, y

    def _get_size(self) -> Tuple[int, int]:
        '''Get the panel's size.'''
        return self._size

    def _set_size(self, val:Tuple[int, int]):
        '''Set the panel's size.'''
        self._w, self._h = val
        self._size = val
        self._rect = Rect(self._pos, val)

    size = property(_get_size, _set_size)

    def collides(self, collision_pos:Tuple[int, int]) -> bool:
        '''Detect if a position collides with the panel.'''
        return self._rect.collidepoint(collision_pos)
        
    def handle_click(self, event:Event) -> None:
        '''Handle a click interaction with the panel.'''
        pass

    def handle_hover(self, mouse_pos:Tuple[int, int]) -> None:
        '''Handle a hover interaction with the panel.'''
        self._hovered = True

    def render(self, 
                buffer:Surface, 
                theme:Theme, 
                active:bool=False,
                render_label:bool=True
            ) -> None:
        '''
        Render panel on to the buffer using the theme.
        
        Parameters:
            buffer: the pygame surface to render on to
            theme: the color and layout scheme to use for rendering
            active: boolean indicating if the active color should be used
            render_label: boolean indicating if the label should be rendered
        '''
        if active:
            bg_col = theme.act_col
        else:
            bg_col = theme.bg_col
        draw.rect(buffer, bg_col, self._rect, border_radius=theme.bord_r)
        draw.rect(buffer, theme.bord_col, self._rect, theme.bord_w, theme.bord_r)
        if render_label:
            label = theme.large_text(self._label)
            label_x = self._rect.centerx - label.get_width() // 2
            label_y = self._rect.centery - label.get_height() // 2
            buffer.blit(label, (label_x, label_y))
        self._hovered = False