from typing import List, Type

import pygame as pg
from pygame.event import Event

from .canvas import Canvas
from .controller import Controller
from .coredata import CoreData
from .graphics import Graphics
from ..components.constant import Constant
from ..components.memory import Memory
from ..corium import corium
from ..panels.button import Button
from ..panels.valuepanel import ValuePanel
from ..ui.ui import UI

class Core:
    def __init__(self):
        corium.init()
        pg.init()
        self.core_data = CoreData()
        self.graphics = Graphics(self.core_data)
        self.canvas = Canvas(self.core_data, self.graphics)
        self.ui = UI(self.core_data, self.graphics)
        self.controller = Controller(self.core_data, 
                                        self.graphics, 
                                        self.canvas, 
                                        self.ui
                                    )
        self.load_ui()
        self.run()

    def load_ui(self) -> None:
        def get_ticks(): return self.core_data.get_data('ticks')
        tick_panel = ValuePanel(['Tick Counter'], [get_ticks])
        self.ui.register_panel('ticks', (-1, 0), tick_panel)

        def create_btn_from_types(types:List[Type]) -> Button:
            add_comp_labels = []
            add_comp_on_clicks = []
            for comp_type in types:
                add_comp_labels.append(comp_type.NAME)
                def add_comp_fn(event:Event) -> None:
                    comp = comp_type()
                    self.core_data.set_data('placing', comp)
                    config = comp.get_configuration()
                    self.ui.register_panel('comp-config', (0, 0), config)
                add_comp_on_clicks.append(add_comp_fn)
            return Button(add_comp_labels, add_comp_on_clicks)

        module_btn = create_btn_from_types([Memory])       
        self.ui.register_panel('add-module', (-1, 1), module_btn)
        io_btn = create_btn_from_types([Constant])
        self.ui.register_panel('add-io', (-1, 2), io_btn)

    def run(self) -> None:
        while self.core_data.get_data('running'):
            self.controller.io_tick()
            self.canvas.redraw()
            self.ui.redraw()
            self.graphics.render()