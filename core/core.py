from typing import List, Type

import pygame as pg
from pygame.event import Event

from .canvas import Canvas
from .controller import Controller
from .coredata import CoreData
from .graphics import Graphics
from ..components.constant import Constant
from ..components.memory import Memory
from ..components.opdecoder import Opdecoder
from ..corium import corium, translator
from ..panels.button import Button
from ..panels.valuepanel import ValuePanel
from ..ui.ui import UI

class Core:
    def __init__(self, program:List[str]=None):
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

        if program is not None:
            translation = translator.translate(program)
            prog_mem = Memory()
            prog_mem.load_program(translation)
            prog_mem.set_center((400, 400))
            self.canvas.add_component(prog_mem)

        self.run()

    def new_component(self, component_type:Type) -> None:
        comp = component_type()
        self.core_data.set_data('placing', comp)
        config = comp.get_configuration()
        self.ui.register_panel('comp-config', (0, 0), config)

    def load_ui(self) -> None:
        def get_ticks(): return self.core_data.get_data('ticks')
        tick_panel = ValuePanel(['Tick Counter'], [get_ticks])
        self.ui.register_panel('ticks', (-1, 0), tick_panel)

        module_labels = ['Memory', 'Opdecoder']
        def add_memory(event:Event) -> None:
            self.new_component(Memory)
        def add_opdecoder(event:Event) -> None:
            self.new_component(Opdecoder)
        module_on_clicks = [add_memory, add_opdecoder]
        module_btn = Button(module_labels, module_on_clicks)
        self.ui.register_panel('add-module', (-1, 1), module_btn)

        io_labels = ['Constant']
        def add_constant(event:Event) -> None:
            self.new_component(Constant)
        io_on_clicks = [add_constant]
        io_btn = Button(io_labels, io_on_clicks)
        self.ui.register_panel('add-io', (-1, 2), io_btn)

    def run(self) -> None:
        while self.core_data.get_data('running'):
            self.controller.io_tick()
            self.canvas.redraw()
            self.ui.redraw()
            self.graphics.render()