from typing import List, Tuple

from pygame import draw, Rect, Surface
from pygame.event import Event

from ..ui.theme import Theme

class Panel:
    def __init__(self, 
                    label_objs:List[object], 
                    pos:Tuple[int, int]=(0,0), 
                    size:Tuple[int, int]=(0,0)
                ):
        self.x, self.y = pos
        self.pos = pos
        self.w, self.h = size
        self.size = size
        self.rect = Rect(self.pos, self.size)
        self.label_objs = label_objs
        self.curr_selection = 0
        self.hovered = False

    def repos(self, new_pos:Tuple[int, int]) -> None:
        self.x, self.y = new_pos
        self.pos = new_pos
        self.rect = Rect(self.pos, self.size)

    def repos_resize(self, 
                        new_pos:Tuple[int, int], 
                        new_size:Tuple[int, int]
                    ) -> None:
        self.x, self.y = new_pos
        self.pos = new_pos
        self.w, self.h = new_size
        self.size = new_size
        self.rect = Rect(self.pos, self.size)

    def curr_label(self) -> object:
        return self.label_objs[self.curr_selection]

    def cycle_selection(self) -> None:
        self.curr_selection = (self.curr_selection + 1) % len(self.label_objs)

    def collides(self, collision_pos:Tuple[int, int]) -> bool:
        return self.rect.collidepoint(collision_pos)
        
    def handle_click(self, event:Event) -> None:
        if event.button == 3:
            self.cycle_selection()

    def handle_hover(self) -> None:
        self.hovered = True

    def render(self, 
                buffer:Surface, 
                theme:Theme, 
                hover_color:bool=False,
                render_label:bool=True
            ) -> None:
        if hover_color:
            bg_color = theme.get_hover_color()
        else:
            bg_color = theme.get_bg_color()
        buffer.fill(bg_color, self.rect)
        draw.rect(
            buffer, 
            theme.get_border_color(), 
            self.rect, 
            theme.get_border_width()
        )
        if render_label:
            label = theme.large_text(self.curr_label())
            label_x = self.rect.centerx - label.get_width() // 2
            label_y = self.rect.centery - label.get_height() // 2
            buffer.blit(label, (label_x, label_y))
        self.hovered = False