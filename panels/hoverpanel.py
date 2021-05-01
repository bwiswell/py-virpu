from typing import Callable, List, Tuple

from pygame import Surface

from .panel import Panel
from ..ui.theme import Theme

class HoverPanel(Panel):
    def __init__(self, 
                    label_objs:List[object],
                    value_getters:List[Callable[[], None]],
                    pos:Tuple[int, int]=(0, 0),
                    size:tuple[int, int]=(0, 0)
                ):
        Panel.__init__(self, label_objs, pos, size)
        self.value_getters = value_getters

    def curr_value_getter(self) -> Callable[[], None]:
        return self.value_getters[self.curr_selection]

    def render(self, buffer:Surface, theme:Theme):
        if self.hovered:
            value_getter = self.curr_value_getter()
            content = theme.medium_text(value_getter())
        else:
            content = theme.medium_text(self.curr_label())
        super().render(
            buffer, 
            theme, 
            hover_color=self.hovered, 
            render_label=False
        )
        content_x = self.rect.centerx - content.get_width() // 2
        content_y = self.rect.centery - content.get_height() // 2
        buffer.blit(content, (content_x, content_y))