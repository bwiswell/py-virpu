from __future__ import annotations
from typing import List, Tuple, Union

from pygame import Rect, Surface

from .ioport import IOPort
from ..panels.configuration import Configuration
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
                    size:Tuple[int, int],
                    configuration:Configuration=Configuration()
                ):
        Panel.__init__(self, [comp_name], pos, size)

        self.bounding_box = self.rect

        self.in_ports = in_ports
        self.in_by_id = {in_port.port_id: in_port for in_port in in_ports}
        self.ins = len(in_ports)
        self.out_ports = out_ports
        self.out_by_id = {out_port.port_id: out_port for out_port in out_ports}
        self.outs = len(out_ports)
        
        self.in_y_off = 0 if self.ins == 0 else self.h // self.ins
        self.out_y_off = 0 if self.outs == 0 else self.h // self.outs
        self.repos(pos)

        self.cycles = cycles
        self.cycle_counter = cycles

        self.configuration = configuration

    def repos(self, new_pos:Tuple[int, int]) -> None:
        super().repos(new_pos)
        bb_x = new_pos[0] - IOPort.SIZE[0] // 2
        bb_w = self.w + IOPort.SIZE[0]
        self.bounding_box = Rect(bb_x, self.y, bb_w, self.h)
        in_x = self.x - IOPort.SIZE[0] // 2
        in_y = self.y + self.in_y_off // 2 - IOPort.SIZE[1] // 2
        for in_port in self.in_ports:
            in_port.repos((in_x, in_y))
            in_y += self.in_y_off
        out_x = self.x + self.w - IOPort.SIZE[0] // 2
        out_y = self.y + self.out_y_off // 2 - IOPort.SIZE[1] // 2
        for out_port in self.out_ports:
            out_port.repos((out_x, out_y))
            out_y += self.out_y_off

    def get_configuration(self) -> Configuration:
        return self.configuration

    def get_input_value(self, in_port_id:str) -> Signal:
        return self.in_by_id[in_port_id].get_value()

    def get_in_port(self, in_port_id:str) -> IOPort:
        return self.in_by_id[in_port_id]

    def get_output_value(self, out_port_id:str) -> Signal:
        return self.out_by_id[out_port_id].get_value()

    def get_out_port(self, out_port_id:str) -> IOPort:
        return self.out_by_id[out_port_id]

    def set_input_value(self, in_port_id:str, value:Signal) -> None:
        self.in_by_id[in_port_id].set_value(value)

    def set_output_value(self, out_port_id:str, value:Signal) -> None:
        self.out_by_id[out_port_id].set_value(value)

    def collides(self, collision_pos:Tuple[int, int]) -> bool:
        if self.bounding_box.collidepoint(collision_pos):
            if collision_pos[0] < self.x:
                for in_port in self.in_ports:
                    if in_port.collides(collision_pos):
                        return True
            elif collision_pos[0] > self.x + self.w:
                for out_port in self.out_ports:
                    if out_port.collides(collision_pos):
                        return True
            else:
                return True
        return False

    def get_clicked(self, pos:Tuple[int, int]) -> Union[Component, IOPort]:
        if pos[0] < self.x + IOPort.SIZE[0] // 2:
            for in_port in self.in_ports:
                if in_port.collides(pos):
                    return in_port
        elif pos[0] > self.x + self.w - IOPort.SIZE[0] // 2:
            for out_port in self.out_ports:
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
        for in_port in self.in_ports:
            in_port.render(buffer, theme)
        for out_port in self.out_ports:
            out_port.render(buffer, theme)