from typing import Callable, Tuple

from pygame import Surface

from .panel import Panel
from ..ui.theme import Theme

class ValuePanel(Panel):
    def __init__(self,
                    label_obj:object,
                    value_getter:Callable[[], object],
                    pos:Tuple[int, int]=(0, 0),
                    size:Tuple[int, int]=(0, 0)
                ):
        self.label_obj = label_obj
        self.value_getter = value_getter

    def render(self, buffer:Surface, theme:Theme):
        super().render(buffer, theme)
        label = theme.large_text(self.label_obj)
        value = theme.medium_text(self.value_getter())
        label_x = self.rect.centerx - label.get_width() // 2
        label_y = self.y + self.h // 4 - label.get_height() // 2
        value_x = self.rect.centerx - value.get_width() // 2
        value_y = self.rect.centery
        buffer.blit(label, (label_x, label_y))
        buffer.blit(value, (value_x, value_y))