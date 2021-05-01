from typing import Callable, List, Tuple

from pygame import Surface
from pygame.event import Event

from .panel import Panel
from ..ui.theme import Theme

class Button(Panel):
    def __init__(self, 
                    label_objs:List[object],
                    on_clicks:List[Callable[[Event], None]],
                    pos:Tuple[int, int]=(0, 0),
                    size:tuple[int, int]=(0, 0)
                ):
        Panel.__init__(self, label_objs, pos, size)
        self.on_clicks = on_clicks

    def get_curr_on_click(self) -> Callable[[Event], None]:
        return self.on_clicks[self.curr_selection]

    def handle_click(self, event:Event) -> None:
        super().handle_click(event)
        if event.button == 1:
            on_click = self.get_curr_on_click()
            on_click(event)

    def render(self, buffer:Surface, theme:Theme) -> None:
        super().render(buffer, theme, hover_color=self.hovered)