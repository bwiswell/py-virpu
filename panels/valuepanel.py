from typing import Callable, List, Tuple

from pygame import Surface

from .panel import Panel
from ..ui.theme import Theme

class ValuePanel(Panel):
    def __init__(self,
                    label_objs:List[object],
                    value_getters:List[Callable[[], object]],
                    pos:Tuple[int, int]=(0, 0),
                    size:Tuple[int, int]=(0, 0)
                ):
        Panel.__init__(self, label_objs, pos, size)
        self.value_getters = value_getters

    def curr_value_getter(self) -> Callable[[], object]:
        return self.value_getters[self.curr_selection]

    def render(self, buffer:Surface, theme:Theme):
        super().render(buffer, theme, render_label=False)
        label = theme.large_text(self.curr_label())
        label_x = self.rect.centerx - label.get_width() // 2
        label_y = self.y + self.h // 4 - label.get_height() // 2
        buffer.blit(label, (label_x, label_y))
        value_getter = self.curr_value_getter()
        value = theme.medium_text(value_getter())
        value_x = self.rect.centerx - value.get_width() // 2
        value_y = self.rect.centery - value.get_height() // 2
        buffer.blit(value, (value_x, value_y))