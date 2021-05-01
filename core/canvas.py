from .coredata import CoreData
from .graphics import Graphics

class Canvas:
    def __init__(self, core_data:CoreData, graphics:Graphics):
        self.core_data = core_data
        self.graphics = graphics

        self.components = []
        self.wires = []

    def add_component(self, component): # :ComponentPanel):
        self.components.append(component)

    def remove_component(self, component): # :ComponentPanel):
        self.components.remove(component)
        # TODO: Check for wires to be removed on component deletion

    def add_wire(self, wire): # :Wire):
        self.wires.append(wire)

    def remove_wire(self, wire): # :Wire):
        self.wires.remove(wire)

    def tick(self) -> None:
        # TODO: Implement tick function for the canvas
        curr_tick = self.core_data.get_data('ticks') + 1
        self.core_data.set_data('ticks', curr_tick)

    def redraw(self) -> None:
        # TODO: Implement redraw function for the canvas
        buffer = self.graphics.clear_canvas_buffer()
        theme = self.core_data.get_data('canvas-theme')
        # Pass to components and wires
        pass