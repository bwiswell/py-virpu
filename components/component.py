from __future__ import annotations
from typing import List, Tuple, Union

from pygame import Rect, Surface

from .ioport import IOPort
from ..panels.panel import Panel
from ..signal.signal import Signal
from ..ui.theme import Theme

class Component(Panel):
    def __init__(self, 
                    comp_name:str, 
                    in_ports:List[IOPort],
                    out_ports:List[IOPort],
                    cycles:int, 
                    pos:Tuple[int, int], 
                    size:Tuple[int, int]
                ):
        Panel.__init__(self, [comp_name], pos, size)
        bb_x = pos[0] - IOPort.SIZE[0] // 2
        bb_w = self.w + IOPort.SIZE[0]
        self.bounding_box = Rect(bb_x, self.y, bb_w, self.h)
        
        in_x = self.x - IOPort.SIZE[0] // 2
        in_y = self.y
        in_y_off = self.h // len(in_ports)
        for in_port in self.in_ports:
            in_port.repos((in_x, in_y))
            in_y += in_y_off
        self.in_ports = {in_port.port_id: in_port for in_port in in_ports}

        out_x = self.x + self.w - IOPort.SIZE[0] // 2
        out_y = self.y
        out_y_off = self.h // len(out_ports)
        for out_port in self.out_ports:
            out_port.repos((out_x, out_y))
            out_y += out_y_off
        self.out_ports = {out_port.port_id: out_port for out_port in out_ports}

        self.cycles = cycles
        self.cycle_counter = cycles

    def get_input_value(self, in_port_id:str) -> Signal:
        return self.in_ports[in_port_id].get_value()

    def set_output_value(self, out_port_id:str, value:Signal) -> None:
        self.out_ports[out_port_id].set_value(value)

    def collides(self, collision_pos:Tuple[int, int]) -> bool:
        if self.bounding_box.collidepoint(collision_pos):
            if collision_pos[0] < self.x:
                for in_port in self.in_ports.values():
                    if in_port.collides(collision_pos):
                        return True
            elif collision_pos[0] > self.x + self.w:
                for out_port in self.out_ports.values():
                    if out_port.collides(collision_pos):
                        return True
            else:
                return True
        return False

    def get_clicked(self, pos:Tuple[int, int]) -> Union[Component, IOPort]:
        io_in = pos[0] < self.x + IOPort.SIZE[0] // 2
        io_out = pos[0] > self.x + self.w - IOPort.SIZE[0] // 2
        if io_in:
            for in_port in self.in_ports.values():
                if in_port.collides(pos):
                    return in_port
        elif io_out:
            for out_port in self.out_ports.values():
                if out_port.collides(pos):
                    return out_port
        return self

    def execute(self) -> None:
        pass

    def tick(self) -> None:
        self.cycle_counter -= 1
        if self.cycle_counter == 0:
            self.execute()
            self.cycle_counter = self.cycles

    def render(self, buffer:Surface, theme:Theme) -> None:
        super().render(buffer, theme)
        for in_port in self.in_ports.values():
            in_port.render(buffer, theme)
        for out_port in self.out_ports.values():
            out_port.render(buffer, theme)