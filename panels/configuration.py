from typing import Callable, List, Tuple

from pygame import Rect, Surface
from pygame.event import Event

from .panel import Panel
from ..ui.theme import Theme

def dummy_fn(obj:object) -> None:
    pass

class Configuration(Panel):
    def __init__(self, 
                    config_labels:List[str]=['N/A'],
                    config_options:List[List[object]]=[[]],
                    config_setters:List[Callable[[object], None]]=[dummy_fn],
                    pos:Tuple[int, int]=(0, 0),
                    size:tuple[int, int]=(0, 0)
                ):
        Panel.__init__(self, config_labels, pos, size)
        self.config_options = config_options
        self.config_setters = config_setters
        self.option_rects = {}

    def curr_options(self) -> List[object]:
        return self.config_options[self.curr_selection]

    def curr_setter(self) -> Callable[[object], None]:
        return self.config_setters[self.curr_selection]

    def create_option_rects(self) -> None:
        self.option_rects.clear()
        curr_ops = self.curr_options()
        n_ops = len(curr_ops)
        op_w = 0 if n_ops == 0 else self.w // len(curr_ops)
        op_h = self.h // 4
        op_x = self.x
        op_y = self.rect.centery - op_h // 2
        for op in curr_ops:
            self.option_rects[op] = Rect(op_x, op_y, op_w, op_h)
            op_x += op_w           

    def repos(self, new_pos:Tuple[int, int]) -> None:
        super().repos(new_pos)
        self.create_option_rects()

    def cycle_selection(self) -> None:
        super().cycle_selection()
        self.create_option_rects()

    def handle_click(self, event:Event) -> None:
        super().handle_click(event)
        for op, rect in self.option_rects.items():
            if rect.collidepoint(event.pos):
                curr_setter = self.curr_setter()
                curr_setter(op)

    def render(self, buffer:Surface, theme:Theme) -> None:
        super().render(buffer, theme, render_label=False)
        label = theme.large_text(self.curr_label())
        label_x = self.rect.centerx - label.get_width() // 2
        label_y = self.y + self.h // 4 - label.get_height() // 2
        buffer.blit(label, (label_x, label_y))
        for op, rect in self.option_rects.items():
            option = theme.medium_text(op)
            option_x = rect.centerx - option.get_width() // 2
            option_y = rect.centery - option.get_height() // 2
            buffer.blit(option, (option_x, option_y))