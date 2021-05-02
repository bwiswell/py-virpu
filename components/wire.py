

from pygame import draw, Surface

from .ioport import IOPort
from ..ui.theme import Theme

class Wire:
    def __init__(self, wire_in:IOPort, wire_out:IOPort):
        self.wire_in = wire_in
        self.wire_out = wire_out

    @classmethod
    def compatible(cls, io_a:IOPort, io_b:IOPort) -> bool:
        any_tag = io_a.port_type == 'any' or io_b.port_type == 'any'
        match_tag = io_a.port_type == io_b.port_type
        match_width = io_a.data_width == io_b.data_width
        match_sign = io_a.get_signed() == io_b.get_signed()
        return (any_tag or match_tag) and match_width and match_sign

    def render(self, buffer:Surface, theme:Theme) -> None:
        line_color = theme.get_border_color()
        a_x = self.wire_in.rect.right
        a_y = self.wire_in.rect.centery - self.wire_in.data_width // 2
        b_x = self.wire_out.x
        b_y = self.wire_out.rect.centery - self.wire_out.data_width // 2
        for i in range(self.wire_in.data_width):
            draw.aaline(buffer, line_color, (a_x, a_y), (b_x, b_y))
            a_y += 1
            b_y += 1