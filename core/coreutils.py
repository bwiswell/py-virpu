from typing import List

from pygame.event import Event

from .canvas import Canvas
from .coredata import CoreData
from ..components.aggregator import Aggregator
from ..components.constant import Constant
from ..components.controlunit import ControlUnit
from ..components.counter import Counter
from ..components.decoder import Decoder
from ..components.delayer import Delayer
from ..components.logicgate import AndGate, NotGate, OrGate
from ..components.memory import Memory
from ..components.register import Register
from ..components.wire import Wire
from ..corium import translator
from ..panels.button import Button
from ..panels.cyclepanel import CyclePanel
from ..panels.valuepanel import ValuePanel
from ..ui.ui import UI

def load_ui(core_data:CoreData, ui:UI) -> None:
    '''Load the default PyVirpu UI.'''
    def get_ticks() -> None: return core_data.ticks
    tick_panel = ValuePanel('Tick Counter', get_ticks)
    ui.register_panel('ticks', (-1, 0), tick_panel)

    def add_aggregator(event:Event) -> None: core_data.placing = Aggregator()
    def add_and(event:Event) -> None: core_data.placing = AndGate()
    def add_constant(event:Event) -> None: core_data.placing = Constant()
    def add_controlunit(event:Event) -> None: core_data.placing = ControlUnit()
    def add_counter(event:Event) -> None: core_data.placing = Counter()
    def add_decoder(event:Event) -> None: core_data.placing = Decoder()
    def add_delayer(event:Event) -> None: core_data.placing = Delayer()
    def add_memory(event:Event) -> None: core_data.placing = Memory()
    def add_not(event:Event) -> None: core_data.placing = NotGate()
    def add_or(event:Event) -> None: core_data.placing = OrGate()
    def add_register(event:Event) -> None: core_data.placing = Register()

    aggregator_btn = Button('Aggregator', add_aggregator)
    and_btn = Button('AND Gate', add_and)
    constant_btn = Button('Constant', add_constant)
    controlunit_btn = Button('Control Unit', add_controlunit)
    counter_btn = Button('Counter', add_counter)
    decoder_btn = Button('Decoder', add_decoder)
    delayer_btn = Button('Delayer', add_delayer)
    memory_btn = Button('Memory', add_memory)
    not_btn = Button('NOT Gate', add_not)
    or_btn = Button('OR Gate', add_or)
    register_btn = Button('Register Bank', add_register)

    module_btns = [
                    controlunit_btn,
                    counter_btn,
                    decoder_btn,
                    memory_btn,
                    register_btn
                ]

    logic_btns = [
                    and_btn,
                    not_btn,
                    or_btn
                ]

    utility_btns = [
                    aggregator_btn,
                    constant_btn,
                    delayer_btn
                ]
    
    module_panel = CyclePanel('Modules', module_btns)
    ui.register_panel('modules', (-1, 1), module_panel)

    logic_panel = CyclePanel('Logic Gates', logic_btns)
    ui.register_panel('logic-gates', (-1, 2), logic_panel)

    utility_panel = CyclePanel('Utilities', utility_btns)
    ui.register_panel('utilities', (-1, 3), utility_panel)





    

def load_default_setup(canvas:Canvas, program:List[str]) -> None:
    '''WORK IN PROGRESS'''
    counter = Counter()
    counter.center_on((100, 450))
    canvas.add_component(counter)

    prog_mem = Memory()
    if program is not None:
        translation = translator.translate(program)
        prog_mem.load_program(translation)
    prog_mem.center_on((400, 450))
    canvas.add_component(prog_mem)

    wire = Wire(counter.out_by_id['data'], prog_mem.in_by_id['address'])
    canvas.add_wire(wire)

    decoder = Decoder()
    decoder.center_on((700, 450))
    canvas.add_component(decoder)

    wire = Wire(prog_mem.out_by_id['data'], decoder.in_by_id['ins'])
    canvas.add_wire(wire)

    control = ControlUnit()
    control.center_on((700, 150))
    canvas.add_component(control)

    wire = Wire(decoder.out_by_id['opcode'], control.in_by_id['opcode'])
    wire.add_waypoint((850, 319))
    wire.add_waypoint((550, 319))
    canvas.add_wire(wire)

    registers = Register()
    registers.center_on((1400, 450))
    canvas.add_component(registers)

    wire = Wire(decoder.out_by_id['reg-a'], registers.in_by_id['reg-a'])
    canvas.add_wire(wire)

    wire = Wire(decoder.out_by_id['reg-b'], registers.in_by_id['reg-b'])
    canvas.add_wire(wire)

    wire = Wire(decoder.out_by_id['reg-w'], registers.in_by_id['reg-w'])
    canvas.add_wire(wire)