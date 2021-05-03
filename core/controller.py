import pygame as pg
from pygame import mouse
from pygame.event import Event

from .coredata import CoreData
from .graphics import Graphics
from .canvas import Canvas
from ..components.ioport import IOPort
from ..components.wire import Wire
from ..ui.ui import UI

class Controller:
    def __init__(self, 
                    core_data:CoreData, 
                    graphics:Graphics, 
                    canvas:Canvas, 
                    ui:UI
                ):
        self.core_data = core_data
        self.graphics = graphics
        self.canvas = canvas
        self.ui = ui

    def handle_mousedown(self, event:Event) -> None:
        ui_target = self.ui.at_pos(event.pos)
        canvas_target = self.canvas.at_pos(event.pos)
        placing = self.core_data.get_data('placing')
        if ui_target is not None:
            was_placing = self.core_data.get_data('placing')
            self.canvas.remove_wires(was_placing)
            self.core_data.set_data('placing', None)
            self.core_data.set_data('wire', None)
            ui_target.handle_click(event)
        elif canvas_target is not None:
            was_placing = self.core_data.get_data('placing')
            self.canvas.remove_wires(was_placing)
            self.core_data.set_data('placing', None)
            config = canvas_target.get_configuration()
            self.ui.register_panel('comp-config', (0, 0), config)
            if isinstance(canvas_target, IOPort):
                if event.button == 1:
                    if canvas_target.port_dir == 'out':
                        wire = Wire(canvas_target)
                        self.core_data.set_data('wire', wire)
                    else:
                        wire = self.core_data.get_data('wire')
                        self.core_data.set_data('wire', None)
                        if wire is not None and wire.compatible(canvas_target):
                            wire.set_wire_out(canvas_target)
                            self.canvas.add_wire(wire)
                elif event.button == 3:
                    self.core_data.set_data('wire', None)
                    self.canvas.remove_wires_from_port(canvas_target)
            else:
                if event.button == 3:
                    self.canvas.remove_component(canvas_target)
                    self.core_data.set_data('placing', canvas_target)
        elif placing is not None:
            placing.set_center(event.pos)
            self.canvas.add_component(placing)
            self.core_data.set_data('placing', None)
        else:
            self.ui.unregister_panel('comp-config')
            wire = self.core_data.get_data('wire')
            if wire is not None:
                wire.add_to_route(event.pos)

    def handle_keydown(self, event:Event) -> None:
        if event.key == pg.K_ESCAPE:
            self.core_data.set_data('running', False)
        elif event.key == pg.K_SPACE:
            self.canvas.tick()
        elif event.key == pg.K_DELETE:
            was_placing = self.core_data.get_data('placing')
            self.canvas.remove_wires(was_placing)
            self.core_data.set_data('placing', None)
            self.ui.unregister_panel('comp-config')

    def handle_hover(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        ui_target = self.ui.at_pos(mouse_pos)
        canvas_target = self.canvas.at_pos(mouse_pos)
        if ui_target is not None:
            ui_target.handle_hover()
        elif canvas_target is not None:
            canvas_target.handle_hover()

    def render_overlay(self) -> None:
        buffer = self.graphics.clear_overlay_buffer()
        theme = self.core_data.get_data('overlay-theme')
        mouse_pos = pg.mouse.get_pos()
        placing = self.core_data.get_data('placing')
        if placing is not None:
            placing.set_center(mouse_pos)
            placing.render(buffer, theme)
        wire = self.core_data.get_data('wire')
        if wire is not None:
            wire.render(buffer, theme, mouse_pos)

    def io_tick(self) -> None:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                self.handle_mousedown(event)
            elif event.type == pg.KEYDOWN:
                self.handle_keydown(event)
        self.handle_hover()
        self.render_overlay()