from typing import Tuple, Union

from .coredata import CoreData
from .graphics import Graphics
from ..components.component import Component
from ..components.ioport import IOPort
from ..components.wire import Wire

class Canvas:
    '''
    A class to track and manage functional logic components.

    Attributes:
        core_data (CoreData): The current core state object
        graphics (Graphics): The current graphics object
        components (List[Component]): The components currently on the canvas
        wires (List[Wire]): The wires currently on the canvas
    '''
    def __init__(self, core_data:CoreData, graphics:Graphics):
        '''
        Initialize the Canvas object.

        Parameters:
            core_data: The current core state object
            graphics: The current graphics object
        '''
        self._core_data = core_data
        self._graphics = graphics

        self._components = []
        self._wires = []

    def add_component(self, component:Component) -> None:
        '''Add a component to the canvas.'''
        self._components.append(component)

    def remove_component(self, component:Component) -> None:
        '''Remove a component from the canvas.'''
        self._components.remove(component)

    def add_wire(self, wire:Wire) -> None:
        '''Add a wire to the canvas.'''
        self._wires.append(wire)

    def remove_wire(self, wire:Wire) -> None:
        '''Remove a wire from the canvas.'''
        self._wires.remove(wire)

    def remove_wires(self, component:Component) -> None:
        '''Remove all wires connected to component from the canvas.'''
        if component is not None:
            comp_ios = component.in_ports
            comp_ios.extend(component.out_ports)
            to_remove = []
            for wire in self._wires:
                if wire.wire_in in comp_ios or wire.wire_out in comp_ios:
                    to_remove.append(wire)
            for wire in to_remove:
                self._wires.remove(wire)

    def remove_wires_from_port(self, io_port:IOPort) -> None:
        '''Remove all wires connected to io_port from the canvas.'''
        if io_port is not None:
            to_remove = []
            for wire in self._wires:
                if wire.wire_in is io_port or wire.wire_out is io_port:
                    to_remove.append(wire)
            for wire in to_remove:
                self._wires.remove(wire)

    def at_pos(self, pos:Tuple[int, int]) -> Union[Component, IOPort]:
        '''Return the component or IO port at the given position.'''
        for component in self._components:
            if component.collides(pos):
                return component.at_pos(pos)

    def tick(self) -> None:
        '''Perform a single clock cycle on all components and wires.'''
        self._core_data.ticks += 1
        for component in self._components:
            component.tick()
        for wire in self._wires:
            wire.tick()

    def redraw(self) -> None:
        '''Redraw components and wires to the canvas buffer.'''
        buffer = self._graphics.canvas_buffer
        theme = self._core_data.canvas_theme
        for component in self._components:
            component.render(buffer, theme)
        for wire in self._wires:
            wire.render(buffer, theme)