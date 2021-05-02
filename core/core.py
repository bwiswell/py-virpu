import pygame as pg
from pygame.event import Event

from .canvas import Canvas
from .controller import Controller
from .coredata import CoreData
from .graphics import Graphics
from ..components.component import Component
from ..components.memory import Memory
from ..panels.button import Button
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
        tick_panel = ValuePanel(['Tick Counter'], [get_ticks])
        self.ui.register_panel('ticks', (-1, 0), tick_panel)
        
        add_comp_labels = []
        add_comp_on_clicks = []
        for cls in [Memory]:
            add_comp_labels.append(cls.NAME)
            def add_comp_fn(event:Event) -> None:
                self.core_data.set_data('placing', cls())
            add_comp_on_clicks.append(add_comp_fn)
        add_comp_btn = Button(add_comp_labels, add_comp_on_clicks)
        self.ui.register_button('add-comp', (-1, 1), add_comp_btn)

    def run(self) -> None:
        while self.core_data.get_data('running'):
            self.controller.io_tick()
            self.canvas.redraw()
            self.ui.redraw()
            self.graphics.render()