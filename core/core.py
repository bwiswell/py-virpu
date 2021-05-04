from typing import List, Type

import pygame as pg
from pygame.event import Event

from .canvas import Canvas
from .controller import Controller
from .coredata import CoreData
from .graphics import Graphics
from ..components.aggregator import Aggregator
from ..components.andgate import AndGate
from ..components.constant import Constant
from ..components.counter import Counter
from ..components.decoder import Decoder
from ..components.delayer import Delayer
from ..components.memory import Memory
from ..components.opdecoder import Opdecoder
from ..components.register import Register
from ..components.wire import Wire
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
        self.load_default_setup(program)

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

        module_labels = ['Decoder', 'Memory', 'Opdecoder', 'Register']
        def add_decoder(event:Event) -> None:
            self.new_component(Decoder)
        def add_memory(event:Event) -> None:
            self.new_component(Memory)
        def add_opdecoder(event:Event) -> None:
            self.new_component(Opdecoder)
        def add_register(event:Event) -> None:
            self.new_component(Register)
        module_on_clicks = [
                            add_decoder, 
                            add_memory, 
                            add_opdecoder, 
                            add_register
                        ]
        module_btn = Button(module_labels, module_on_clicks)
        self.ui.register_panel('add-module', (-1, 1), module_btn)

        utility_labels = ['Aggregator', 'Counter', 'Delayer']
        def add_aggregator(event:Event) -> None:
            self.new_component(Aggregator)
        def add_counter(event:Event) -> None:
            self.new_component(Counter)
        def add_delayer(event:Event) -> None:
            self.new_component(Delayer)
        utility_on_clicks = [add_aggregator, add_counter, add_delayer]
        utility_btn = Button(utility_labels, utility_on_clicks)
        self.ui.register_panel('add-utility', (-1, 2), utility_btn)

        logic_labels = ['AND Gate']
        def add_andgate(event:Event) -> None:
            self.new_component(AndGate)
        logic_on_clicks = [add_andgate]
        logic_btn = Button(logic_labels, logic_on_clicks)
        self.ui.register_panel('add-logic', (-1, 3), logic_btn)

        io_labels = ['Constant']
        def add_constant(event:Event) -> None:
            self.new_component(Constant)
        io_on_clicks = [add_constant]
        io_btn = Button(io_labels, io_on_clicks)
        self.ui.register_panel('add-io', (-1, 4), io_btn)

    def load_default_setup(self, program:List[str]) -> None:
        counter = Counter()
        counter.set_center((100, 450))
        self.canvas.add_component(counter)

        prog_mem = Memory()
        if program is not None:
            translation = translator.translate(program)
            prog_mem.load_program(translation)
            prog_mem.execute()
        prog_mem.set_center((400, 450))
        self.canvas.add_component(prog_mem)

        wire = Wire(counter.out_by_id['data'], prog_mem.in_by_id['address'])
        self.canvas.add_wire(wire)

        decoder = Decoder()
        decoder.set_center((700, 450))
        self.canvas.add_component(decoder)

        wire = Wire(prog_mem.out_by_id['data'], decoder.in_by_id['ins'])
        self.canvas.add_wire(wire)

        op_decoder = Opdecoder()
        op_decoder.set_center((700, 150))
        self.canvas.add_component(op_decoder)

        wire = Wire(decoder.out_by_id['opcode'], op_decoder.in_by_id['opcode'])
        wire.add_to_route((850, 319))
        wire.add_to_route((550, 319))
        self.canvas.add_wire(wire)

        registers = Register()
        registers.set_center((1400, 450))
        self.canvas.add_component(registers)

        wire = Wire(decoder.out_by_id['reg-a'], registers.in_by_id['reg-a'])
        self.canvas.add_wire(wire)

        wire = Wire(decoder.out_by_id['reg-b'], registers.in_by_id['reg-b'])
        self.canvas.add_wire(wire)

        wire = Wire(decoder.out_by_id['reg-w'], registers.in_by_id['reg-w'])
        self.canvas.add_wire(wire)

    def run(self) -> None:
        while self.core_data.get_data('running'):
            self.controller.io_tick()
            self.canvas.redraw()
            self.ui.redraw()
            self.graphics.render()