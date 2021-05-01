from typing import Callable, Tuple

from pygame import Surface

from .panel import Panel
from ..ui.theme import Theme

class HoverPanel(Panel):
    def __init__(self, 
                    label_obj:object,
                    value_getter:Callable[[], None],
                    pos:Tuple[int, int]=(0, 0),
                    size:tuple[int, int]=(0, 0)
                ):
        Panel.__init__(self, pos, size)
        self.label_obj = label_obj
        self.value_getter = value_getter

    def render(self, buffer:Surface, theme:Theme):
        if self.hovered:
            content = theme.medium_text(self.value_getter())
        else:
            content = theme.medium_text(self.label_obj)
        super().render(buffer, theme, hover_color=self.hovered)
        content_x = self.rect.centerx - content.get_width() // 2
        content_y = self.rect.centery - content.get_height() // 2
        buffer.blit(content, (content_x, content_y))