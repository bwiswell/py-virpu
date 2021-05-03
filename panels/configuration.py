from typing import Callable, List, Tuple

from pygame import mouse, Surface
from pygame.event import Event

from .button import Button
from .panel import Panel
from ..ui.theme import Theme

def dummy_getter() -> object:
    return 'N/A'

def dummy_setter(obj:object) -> None:
    pass

def dummy_on_click(event:Event) -> None:
    pass

class Configuration(Panel):

    DEF_SPACING = 5

    def __init__(self, 
                    config_labels:List[str]=['N/A'],
                    config_options:List[List[object]]=[[]],
                    config_getters:List[Callable[[], object]]=[dummy_getter],
                    config_setters:List[Callable[[object], None]]=[dummy_setter],
                ):
        Panel.__init__(self, config_labels)
        self.config_options = config_options
        self.config_getters = config_getters
        self.config_setters = config_setters
        self.buttons = []

    def curr_options(self) -> List[object]:
        return self.config_options[self.curr_selection]

    def curr_getter(self) -> Callable[[], object]:
        return self.config_getters[self.curr_selection]

    def curr_setter(self) -> Callable[[object], None]:
        return self.config_setters[self.curr_selection]

    def create_buttons(self) -> None:
        self.buttons.clear()
        curr_ops = self.curr_options()
        n_ops = len(curr_ops)
        if n_ops > 0:
            x_off = Configuration.DEF_SPACING
            y_off = self.h // 3
            op_w = (self.w - x_off * (n_ops + 1)) // n_ops
            op_h = y_off
            op_x = self.x + x_off
            op_y = self.y + self.h - y_off - op_h // 2
            for op in curr_ops:
                op_btn = Button(
                                    [op], 
                                    [dummy_on_click], 
                                    (op_x, op_y), 
                                    (op_w, op_h)
                                )
                self.buttons.append(op_btn)
                op_x += op_w + x_off     

    def repos(self, new_pos:Tuple[int, int]) -> None:
        super().repos(new_pos)
        self.create_buttons()

    def add_config(self,
                    config_label:str,
                    config_options:List[object]=[],
                    config_getter:Callable[[], object]=dummy_getter,
                    config_setter:Callable[[object], None]=dummy_setter
                ) -> None:
        self.label_objs.append(config_label)
        self.config_options.append(config_options)
        self.config_getters.append(config_getter)
        self.config_setters.append(config_setter)

    def cycle_selection(self) -> None:
        super().cycle_selection()
        self.create_buttons()

    def handle_click(self, event:Event) -> None:
        super().handle_click(event)
        if event.button == 1:
            for op_btn in self.buttons:
                if op_btn.collides(event.pos):
                    setter = self.curr_setter()
                    value = op_btn.curr_label()
                    setter(value)

    def handle_hover(self) -> None:
        super().handle_hover()
        mouse_pos = mouse.get_pos()
        for op_btn in self.buttons:
            if op_btn.collides(mouse_pos):
                op_btn.handle_hover()

    def render(self, buffer:Surface, theme:Theme) -> None:
        super().render(buffer, theme, render_label=False)
        getter = self.curr_getter()
        curr_val = getter()
        label = f'{self.curr_label()}: {curr_val}'
        label = theme.large_text(label)
        label_x = self.rect.centerx - label.get_width() // 2
        y_off = self.h // 3
        label_y = self.y + y_off - label.get_height() // 2
        buffer.blit(label, (label_x, label_y))
        if len(self.buttons) > 0:
            for op_btn in self.buttons:
                op_btn.render(buffer, theme, curr_val == op_btn.curr_label())