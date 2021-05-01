from typing import Tuple

from pygame import draw, Rect, Surface

from ..ui.theme import Theme

class Panel:
    def __init__(self, pos:Tuple[int, int]=(0,0), size:Tuple[int, int]=(0,0)):
        self.x, self.y = pos
        self.pos = pos
        self.w, self.h = size
        self.size = size
        self.rect = Rect(self.pos, self.size)
        self.hovered = False

    def repos_resize(self, 
                        new_pos:Tuple[int, int], 
                        new_size:Tuple[int, int]
                    ) -> None:
        self.x, self.y = new_pos
        self.pos = new_pos
        self.w, self.h = new_size
        self.size = new_size
        self.rect = Rect(self.pos, self.size)

    def collides(self, collision_pos:Tuple[int, int]) -> bool:
        return self.rect.collidepoint(collision_pos)

    def handle_hover(self) -> None:
        self.hovered = True

    def render(self, buffer:Surface, theme:Theme, hover_color:bool=False) -> None:
        bg_color = theme.get_hover_color() if hover_color else theme.get_bg_color()
        buffer.fill(bg_color, self.rect)
        draw.rect(
            buffer, 
            theme.get_border_color(), 
            self.rect, 
            theme.get_border_width()
        )
        self.hovered = False