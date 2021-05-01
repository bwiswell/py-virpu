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
        ui_button = self.ui.button_at_pos(event.pos)
        if ui_button is not None:
            ui_button.handle_click(event)

    def handle_keydown(self, event:Event) -> None:
        if event.key == pg.K_ESCAPE:
            self.core_data.set_data('running', False)
        elif event.key == pg.K_SPACE:
            self.canvas.tick()

    def handle_hover(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        ui_target = self.ui.at_pos(mouse_pos)
        if ui_target is not None:
            ui_target.handle_hover()

    def io_tick(self) -> None:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                self.handle_mousedown(event)
            elif event.type == pg.KEYDOWN:
                self.handle_keydown(event)
        self.handle_hover()