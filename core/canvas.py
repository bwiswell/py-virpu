from typing import Tuple, Union

from .coredata import CoreData
from .graphics import Graphics
from ..components.component import Component
from ..components.ioport import IOPort

class Canvas:
    def __init__(self, core_data:CoreData, graphics:Graphics):
        self.core_data = core_data
        self.graphics = graphics

        self.components = []
        self.wires = []

    def add_component(self, component:Component):
        self.components.append(component)

    def remove_component(self, component:Component):
        self.components.remove(component)
        # TODO: Check for wires to be removed on component deletion

    def add_wire(self, wire): # :Wire):
        self.wires.append(wire)

    def remove_wire(self, wire): # :Wire):
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