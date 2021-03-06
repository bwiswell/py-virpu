from typing import Tuple

from pygame import draw, Surface

from .ioport import IOPort
from ..ui.theme import Theme

class Wire:
    '''
    A class to represent a wire connecting two IO ports.

    Attributes:
        wire_in (IOPort): the outbound IOPort that serves as the wire's input
        wire_out (IOPort): the inbound IOPort that serves as the wire's output
        route (List[Tuple[int, int]]): the wire's path (excluding endpoints)
    '''

    def __init__(self, wire_in:IOPort, wire_out:IOPort=None):
        '''
        Initialize the Wire object.

        Parameters:
            wire_in: the IOPort that serves as the wire's input
            wire_out: the IOPort that serves as the wire's output (default None)
        '''
        self.wire_in = wire_in
        self.wire_out = wire_out
        self._route = []

    def __str__(self) -> str:
        '''Return a string representing the wire.'''
        return str(self.wire_in.value)

    def compatible(self, io:IOPort) -> bool:
        '''
        Return if the given IOPort is compatible with the wire.

        This method checks port type, bit-width, and signage.

        Parameters:
            io: the IO port to test for compatibility

        Returns:
            compatible: boolean indicating f the IO port is compatible
        '''
        any_tag = self.wire_in.type == 'any' or io.type == 'any'
        match_tag = self.wire_in.type == io.type
        match_width = self.wire_in.width == io.width
        match_sign = self.wire_in.signed == io.signed
        return (any_tag or match_tag) and match_width and match_sign

    def add_waypoint(self, pos:Tuple[int, int]) -> None:
        '''Add a waypoint position to the wire's route.'''
        self._route.append(pos)

    def tick(self) -> None:
        '''Transfer the wire's input value to the wire's output port.'''
        if self.wire_out is not None:
            self.wire_out.value = self.wire_in.value

    def _render_segment(self, 
                        buffer:Surface, 
                        theme:Theme,
                        pos_a:Tuple[int, int],
                        pos_b:Tuple[int, int]
                    ) -> None:
        '''
        Render a segment of a wire between two route waypoints.

        The width of the segment is dependent on the wire's bit-width.

        Parameters:
            buffer: the pygame surface to render on to
            theme: the color and layout scheme to use for rendering
            pos_a: the start position of the line segment
            pos_b: the end position of the line segment
        '''
        y_off = self.wire_in.width // 2
        a_x = pos_a[0]
        a_y = pos_a[1] - y_off
        b_x = pos_b[0]
        b_y = pos_b[1] - y_off
        for i in range(self.wire_in.width):
            draw.aaline(buffer, theme.wire_col, (a_x, a_y), (b_x, b_y))
            a_y += 1
            b_y += 1

    def render(self, 
                buffer:Surface, 
                theme:Theme, 
                mouse_pos:Tuple[int, int]=None
            ) -> None:
        '''
        Render wire according to route and bit-width.
        
        Parameters:
            buffer: the pygame surface to render on to
            theme: the color and layout scheme to use for rendering
            mouse_pos: position for drawing a wire to the mouse (default None)
        '''
        route = [(self.wire_in._rect.right, self.wire_in._rect.centery)]
        route += self._route
        if self.wire_out is not None:
            route += [(self.wire_out._rect.left, self.wire_out._rect.centery)]
        elif mouse_pos is not None:
            route += [mouse_pos]

        max_x_seg = 0
        max_x_dist = 0
        for i in range(len(route) - 1):
            a = route[i]
            b = route[i + 1]
            x_dist = abs(b[0] - a[0])
            if x_dist > max_x_dist:
                max_x_seg = i
                max_x_dist = x_dist
            self._render_segment(buffer, theme, a, b)
        
        max_a = route[max_x_seg]
        max_b = route[max_x_seg + 1]
        mid_x = (max_a[0] + max_b[0]) // 2
        mid_y = (max_a[1] + max_b[1]) // 2
        label = theme.small_text(self, inv_col=True)
        label_x = mid_x - label.get_width() // 2
        label_y = mid_y - label.get_height() // 2
        buffer.blit(label, (label_x, label_y))