from __future__ import annotations
from math import ceil
from typing import List, Tuple, Union

from pygame import Rect, Surface

from .ioport import IOPort
from ..panels.panel import Panel
from ..ui.theme import Theme

class Component(Panel):
    '''
    A class to represent functional logic components that extends Panel. 
    
    This is the base class for all functional logic components, and should not
    be directly instantiated.

    Attributes:
        ins (int): the number of incoming IO ports (input ports)
        outs (int): the number of outgoing IO ports (output ports)
        in_ports (List[IOPort]): ordered list of the component's input ports
        in_by_id (Dict[str, IOPort]): dict of the component's input ports by port ID
        out_ports (List[IOPort]): ordered list of the component's output ports
        out_by_id (Dict[str, IOPort]): dict of the component's output ports by port ID
        cycles (int): the number of cycles between component executions
        counter (int): the number of cycles until the component's next execution
        config_options (str): the component's available configuration options
        bounding_box (Rect): the minimum rectangle that contains the component and its IO ports
    '''        

    MAX_CYCLES = 10
    WIDTH = 200

    def __init__(self, 
                    comp_name:str, 
                    in_ports:List[IOPort]=[],
                    out_ports:List[IOPort]=[],
                    cycles:int=1,
                    config_options:str=''
                ):
        '''
        Initialize Component object and extend Panel.

        Parameters:
            comp_name: the name of the component
            in_ports: ordered list of the component's input ports
            out_ports: ordered list of the component's output ports
            cycles: the number of cycles between component executions
            config_options: the component's available configuration options
        '''
        self._ins = len(in_ports)
        self._outs = len(out_ports)
        Panel.__init__(self, [comp_name], (0, 0), self.get_size())

        self.in_ports = in_ports
        self.in_by_id = {in_port.id: in_port for in_port in in_ports}
        self.out_ports = out_ports
        self.out_by_id = {out_port.id: out_port for out_port in out_ports}

        self._cycles = cycles
        self._counter = cycles

        self.config_options = config_options
        
        self._bounding_box = None

    def reposition_ports(self) -> None:
        '''Reposition the component's IO ports.'''
        bb_x = self._x - IOPort.SIZE[0] // 2
        bb_w = self._w + IOPort.SIZE[0]
        self._bounding_box = Rect(bb_x, self._y, bb_w, self._h)
        in_x = self._x - IOPort.SIZE[0] // 2
        in_y_off = 0 if self._ins == 0 else self._h // self._ins
        in_y = self._y + in_y_off // 2 - IOPort.SIZE[1] // 2
        for in_port in self.in_ports:
            in_port.repos((in_x, in_y))
            in_y += in_y_off
        out_x = self._x + self._w - IOPort.SIZE[0] // 2
        out_y_off = 0 if self.outs == 0 else self._h // self.outs
        out_y = self._y + out_y_off // 2 - IOPort.SIZE[1] // 2
        for out_port in self.out_ports:
            out_port.repos((out_x, out_y))
            out_y += out_y_off

    def _get_pos(self) -> Tuple[int, int]:
        '''Get the position of the component's top-left corner.'''
        return self._pos

    def _set_pos(self, val:Tuple[int, int]) -> None:
        '''Set the position of the component's top-left corner.'''
        super()._set_pos(val)
        self.reposition_ports()

    pos = property(_get_pos, _set_pos)

    def _get_size(self) -> Tuple[int, int]:
        '''Get the size of the component.'''
        return self._size

    def _set_size(self, val:Tuple[int, int]) -> None:
        '''Set the size of the component.'''
        super()._set_size(val)
        self.reposition_ports()

    pos = property(_get_size, _set_size)

    def comp_size(self) -> Tuple[int, int]:
        '''Get the best size of the component for the number of IO ports.'''
        return Component.WIDTH, ceil(max((1, self._ins, self._outs)) / 2.0) * 75

    def add_port(self, port:IOPort) -> None:
        '''Add an IO port to the component.'''
        if port.dir == 'in' and self._ins + 1 <= 32:
            self.in_ports.insert(0, port)
            self.in_by_id[port.id] = port
            self.ins += 1
        elif port.dir == 'out' and self._outs + 1 <= 32:
            self.out_ports.insert(0, port)
            self.out_by_id[port.id] = port
            self.outs += 1
        self.size = self.comp_size()

    def remove_port(self, port:IOPort) -> None:
        '''Remove an IO port from the component.'''
        if port.port_dir == 'in':
            self.in_ports.remove(port)
            self.in_by_id.pop(port.port_id)
            self.ins -= 1
        else:
            self.out_ports.remove(port)
            self.out_by_id.pop(port.port_id)
            self.outs -= 1
        self.size = self.comp_size()

    @property
    def cycles(self) -> int:
        '''Get or set the number of cycles between component executions'''
        return self._cycles

    @cycles.setter
    def cycles(self, val:int) -> None:
        self._cycles = max(1, min(Component.MAX_CYCLES, val))

    def set_width(self, width:int) -> None:
        '''
        Set the bit width of the component.
        
        Set a new bit width for the component. Not all components support this
        configuration option, and implementation is left to the descendants of
        Component.

        Parameters:
            width: the new bit width of the component
        '''
        pass

    def set_signed(self, signed:bool) -> None:
        '''
        Set the signage of the component.
        
        Set a new signage for the component. Not all components support this
        configuration option, and implementation is left to the descendants of
        Component.

        Parameters:
            signed: the new signage of the component
        '''
        pass

    def at_pos(self, pos:Tuple[int, int]) -> Union[Component, IOPort]:
        '''
        Return the component or IO port at a given position.

        Return any IO port at the position. If none are, return the component
        if it collides with the position. Otherwise, return None.

        Parameters:
                pos: the position to check for a collision
        '''
        if self._bounding_box.collidepoint(pos):
            if pos[0] < self._x:
                for in_port in self.in_ports:
                    if in_port.collides(pos):
                        return in_port
            elif pos[0] > self._x + self._w:
                for out_port in self.out_ports:
                    if out_port.collides(pos):
                        return out_port
            else:
                return self
        return None

    def execute(self) -> None:
        '''Execute the component's functional logic.'''
        pass

    def tick(self) -> None:
        '''
        Decrement the cycle counter and execute the component's logic.

        Decrement the counter that tracks the number of cycles before the
        component executes. When the counter reaches zero, execute the
        component and reset the cycle counter.
        '''
        self.cycle_counter -= 1
        if self.cycle_counter == 0:
            self.execute()
            self.cycle_counter = self.cycles

    def render(self, buffer:Surface, theme:Theme) -> None:
        '''
        Extend Panel render method to show IO ports.
        
        Parameters:
            buffer: the pygame surface to render on to
            theme: the color and layout scheme to use for rendering
        '''
        super().render(buffer, theme)
        for in_port in self.in_ports:
            in_port.render(buffer, theme)
        for out_port in self.out_ports:
            out_port.render(buffer, theme)