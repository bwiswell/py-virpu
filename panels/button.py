from typing import Callable, Tuple

from pygame import Surface
from pygame.event import Event

from .panel import Panel
from ..ui.theme import Theme

class Button(Panel):
    def __init__(self, 
                    label_obj:object,
                    on_click:Callable[[Event], None],
                    pos:Tuple[int, int]=(0, 0),
                    size:tuple[int, int]=(0, 0)
                ):
        Panel.__init__(self, pos, size)
        self.label_obj = label_obj
        self.on_click = on_click

    def handle_click(self, click_event:Event) -> None:
        self.on_click(click_event)

    def render(self, buffer:Surface, theme:Theme):
        super().render(buffer, theme)
        label = theme.large_text(self.label_obj)
        label_x = self.x + self.w // 2 - label.get_width() // 2
        label_y = self.y + self.h // 2 - label.get_height() // 2
        buffer.blit(label, (label_x, label_y))