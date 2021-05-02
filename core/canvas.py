from typing import Tuple, Union

from .coredata import CoreData
from .graphics import Graphics
from ..components.component import Component
from ..components.ioport import IOPort
from ..components.wire import Wire

class Canvas:
    def __init__(self, core_data:CoreData, graphics:Graphics):
        self.core_data = core_data
        self.graphics = graphics

        self.components = []
        self.wires = []

    def add_component(self, component:Component) -> None:
        self.components.append(component)

    def remove_component(self, component:Component) -> None:
        self.components.remove(component)

    def add_wire(self, wire:Wire) -> None:
        self.wires.append(wire)

    def remove_wire(self, wire:Wire) -> None:
        self.wires.remove(wire)

    def remove_wires(self, component:Component) -> None:
        if component is not None:
            comp_ios = component.in_ports
            comp_ios.extend(component.out_ports)
            to_remove = []
            for wire in self.wires:
                if wire.wire_in in comp_ios or wire.wire_out in comp_ios:
                    to_remove.append(wire)
            for wire in to_remove:
                self.wires.remove(wire)

    def remove_wires_from_port(self, io_port:IOPort) -> None:
        if io_port is not None:
            to_remove = []
            for wire in self.wires:
                if wire.wire_in is io_port or wire.wire_out is io_port:
                    to_remove.append(wire)
            for wire in to_remove:
                self.wires.remove(wire)

    def at_pos(self, pos:Tuple[int, int]) -> Union[Component, IOPort]:
        for component in self.components:
            if component.collides(pos):
                return component.get_clicked(pos)

    def tick(self) -> None:
        curr_tick = self.core_data.get_data('ticks') + 1
        self.core_data.set_data('ticks', curr_tick)
        for component in self.components:
            component.tick()

    def redraw(self) -> None:
        buffer = self.graphics.clear_canvas_buffer()
        theme = self.core_data.get_data('canvas-theme')
        for component in self.components:
            component.render(buffer, theme)
        for wire in self.wires:
            wire.render(buffer, theme)