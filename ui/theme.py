from typing import Tuple

from pygame import Surface
from pygame.font import Font, SysFont

class Theme:
    def __init__(self,
                    bg_color:Tuple[int, int, int],
                    hover_color:Tuple[int, int, int],
                    border_color:Tuple[int, int, int],
                    border_width:Tuple[int, int, int],
                    border_radius:int=10,
                    font_name:str=None,
                    small_font_size:int=12,
                    medium_font_size:int=18,
                    large_font_size:int=24,
                    text_color:Tuple[int, int, int]=(0, 0, 0)
                ):
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.small_font = SysFont(font_name, small_font_size)
        self.medium_font = SysFont(font_name, medium_font_size)
        self.large_font = SysFont(font_name, large_font_size)
        self.text_color = text_color

    def get_bg_color(self) -> Tuple[int, int, int]:
        return self.bg_color

    def get_hover_color(self) -> Tuple[int, int, int]:
        return self.hover_color

    def get_border_color(self) -> Tuple[int, int, int]:
        return self.border_color

    def get_border_width(self) -> int:
        return self.border_width

    def get_border_radius(self) -> int:
        return self.border_radius

    def get_text_color(self) -> Tuple[int, int, int]:
        return self.text_color

    def set_bg_color(self, bg_color:Tuple[int, int, int]) -> None:
        self.bg_color = bg_color

    def set_hover_color(self, hover_color:Tuple[int, int, int]) -> None:
        self.hover_color = hover_color

    def set_border_color(self, border_color:Tuple[int, int, int]) -> None:
        self.border_color = border_color

    def set_border_width(self, border_width:int) -> None:
        self.border_width = border_width

    def set_border_radius(self, border_radius:int) -> None:
        self.border_radius = border_radius

    def set_text_color(self, text_color:Tuple[int, int, int]) -> None:
        self.text_color = text_color

    def render_text(self, text_obj:object, font:Font) -> Surface:
        return font.render(str(text_obj), True, self.text_color)

    def small_text(self, text_obj:object) -> Surface:
        return self.render_text(text_obj, self.small_font)

    def medium_text(self, text_obj:object) -> Surface:
        return self.render_text(text_obj, self.medium_font)
        
    def large_text(self, text_obj:object) -> Surface:
        return self.render_text(text_obj, self.large_font)