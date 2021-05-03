from typing import Tuple

from pygame import draw, Surface, mouse

from .ioport import IOPort
from ..ui.theme import Theme

class Wire:
    def __init__(self, wire_in:IOPort, wire_out:IOPort=None):
        self.wire_in = wire_in
        self.wire_out = wire_out
        self.route = []

    def compatible(self, io_b:IOPort) -> bool:
        any_tag = self.wire_in.port_type == 'any' or io_b.port_type == 'any'
        match_tag = self.wire_in.port_type == io_b.port_type
        match_width = self.wire_in.data_width == io_b.data_width
        match_sign = self.wire_in.get_signed() == io_b.get_signed()
        return (any_tag or match_tag) and match_width and match_sign

    def set_wire_out(self, out_port:IOPort) -> None:
        self.wire_out = out_port

    def add_to_route(self, pos:Tuple[int, int]) -> None:
        self.route.append(pos)

    def tick(self) -> None:
        if self.wire_out is not None:
            value = self.wire_in.get_value()
            self.wire_out.set_value(value)

    def render_segment(self, 
                        buffer:Surface, 
                        line_color:Tuple[int, int, int],
                        pos_a:Tuple[int, int],
                        pos_b:Tuple[int, int]
                    ) -> None:
        data_w = self.wire_in.data_width
        y_off = data_w // 2
        a_x = pos_a[0]
        a_y = pos_a[1] - y_off
        b_x = pos_b[0]
        b_y = pos_b[1] - y_off
        for i in range(data_w):
            draw.aaline(buffer, line_color, (a_x, a_y), (b_x, b_y))
            a_y += 1
            b_y += 1

    def render(self, buffer:Surface, theme:Theme, mouse_pos:Tuple[int, int]=None) -> None:
        line_color = theme.get_border_color()
        route = [(self.wire_in.rect.right, self.wire_in.rect.centery)]
        route += self.route
        if self.wire_out is not None:
            route += [(self.wire_out.rect.left, self.wire_out.rect.centery)]
        elif mouse_pos is not None:
            route += [mouse_pos]
        for i in range(len(route) - 1):
            self.render_segment(buffer, line_color, route[i], route[i + 1])