import pygame as pg
from pygame.event import Event

from .canvas import Canvas
from .controller import Controller
from .coredata import CoreData
from .graphics import Graphics
from ..panels.button import Button
from ..panels.hoverpanel import HoverPanel
from ..panels.valuepanel import ValuePanel
from ..ui.ui import UI

class Core:
    def __init__(self):
        pg.init()
        self.core_data = CoreData()
        self.graphics = Graphics(self.core_data)
        self.canvas = Canvas(self.core_data, self.graphics)
        self.ui = UI(self.core_data, self.graphics)
        self.controller = Controller(self.core_data, self.graphics, self.canvas, self.ui)
        self.load_ui()
        self.run()

    def load_ui(self) -> None:
        def get_ticks(): return self.core_data.get_data('ticks')
        tick_panel = ValuePanel('Tick Counter', get_ticks)
        self.ui.register_panel('ticks', (-1, 0), tick_panel)
        def tick(event:Event): self.canvas.tick()
        tick_button = Button('Tick++', tick)
        self.ui.register_button('incr-tick', (-1, 1), tick_button)
        def test_message(): return 'Test message'
        test_panel = HoverPanel('Test Panel', test_message)
        self.ui.register_panel('test', (-2, 0), test_panel)

    def run(self) -> None:
        while self.core_data.get_data('running'):
            self.controller.io_tick()
            self.canvas.redraw()
            self.ui.redraw()
            self.graphics.render()