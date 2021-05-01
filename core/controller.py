import pygame as pg
from pygame.event import Event

from .coredata import CoreData
from .graphics import Graphics
from .canvas import Canvas
from ..ui.ui import UI

class Controller:
    def __init__(self, core_data:CoreData, graphics:Graphics, canvas:Canvas, ui:UI):
        self.core_data = core_data
        self.graphics = graphics
        self.canvas = canvas
        self.ui = ui

    def handle_mousedown(self, event:Event) -> None:
        ui_target = self.ui.get_clicked(event.pos)
        if ui_target is not None:
            ui_target.handle_click(event)

    def handle_keydown(self, event:Event) -> None:
        if event.key == pg.K_ESCAPE:
            self.core_data.set_data('running', False)
        elif event.key == pg.K_SPACE:
            curr_tick = self.core_data.get_data('ticks')
            self.core_data.set_data('ticks', curr_tick)
            self.canvas.tick()

    def io_tick(self) -> None:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                self.handle_mousedown(event)
            elif event.type == pg.KEYDOWN:
                self.handle_keydown(event)