from typing import Tuple

from pygame import Surface
from pygame.font import Font, SysFont

class Theme:
    def __init__(self,
                    bg_color:Tuple[int, int, int],
                    active_color:Tuple[int, int, int],
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
        self.active_color = active_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.small_font = SysFont(font_name, small_font_size)
        self.small_bold = SysFont(font_name, small_font_size, True)
        self.medium_font = SysFont(font_name, medium_font_size)
        self.medium_bold = SysFont(font_name, medium_font_size, True)
        self.large_font = SysFont(font_name, large_font_size)
        self.large_bold = SysFont(font_name, large_font_size, True)
        self.text_color = text_color

    def get_bg_color(self) -> Tuple[int, int, int]:
        return self.bg_color

    def get_active_color(self) -> Tuple[int, int, int]:
        return self.active_color

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

    def set_active_color(self, active_color:Tuple[int, int, int]) -> None:
        self.active_color = active_color

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

    def small_text(self, text_obj:object, bold:bool=False) -> Surface:
        font = self.small_bold if bold else self.small_font
        return self.render_text(text_obj, font)

    def medium_text(self, text_obj:object, bold:bool=False) -> Surface:
        font = self.medium_bold if bold else self.medium_font
        return self.render_text(text_obj, font)
        
    def large_text(self, text_obj:object, bold:bool=False) -> Surface:
        font = self.large_bold if bold else self.large_font
        return self.render_text(text_obj, font)