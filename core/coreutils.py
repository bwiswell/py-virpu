from typing import List

from pygame.event import Event

from .canvas import Canvas
from .coredata import CoreData
from ..components.aggregator import Aggregator
from ..components.alu import ALU
from ..components.constant import Constant
from ..components.controlunit import ControlUnit
from ..components.counter import Counter
from ..components.decoder import Decoder
from ..components.immediates import LeftShifter, SignExtender
from ..components.incrementer import Incrementer
from ..components.logicgate import AndGate, NotGate, OrGate
from ..components.memory import Memory
from ..components.multiplexer import Multiplexer
from ..components.pcadder import PCAdder
from ..components.register import Register
from ..components.stageregister import StageRegister
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
    def add_incrementer(event:Event) -> None: core_data.placing = Incrementer()
    def add_memory(event:Event) -> None: core_data.placing = Memory()
    def add_multiplexer(event:Event) -> None: core_data.placing = Multiplexer()
    def add_not(event:Event) -> None: core_data.placing = NotGate()
    def add_or(event:Event) -> None: core_data.placing = OrGate()
    def add_register(event:Event) -> None: core_data.placing = Register()

    aggregator_btn = Button('Aggregator', add_aggregator)
    and_btn = Button('AND Gate', add_and)
    constant_btn = Button('Constant', add_constant)
    controlunit_btn = Button('Control Unit', add_controlunit)
    counter_btn = Button('Counter', add_counter)
    decoder_btn = Button('Decoder', add_decoder)
    memory_btn = Button('Memory', add_memory)
    multiplexer_btn = Button('Multiplexer', add_multiplexer)
    not_btn = Button('NOT Gate', add_not)
    or_btn = Button('OR Gate', add_or)
    register_btn = Button('Register Bank', add_register)

    module_btns = [
                    controlunit_btn,
                    counter_btn,
                    decoder_btn,
                    memory_btn,
                    multiplexer_btn,
                    register_btn
                ]

    logic_btns = [
                    and_btn,
                    not_btn,
                    or_btn
                ]

    utility_btns = [
                    aggregator_btn,
                    constant_btn
                ]
    
    module_panel = CyclePanel('Modules', module_btns)
    ui.register_panel('modules', (-1, 1), module_panel)

    logic_panel = CyclePanel('Logic Gates', logic_btns)
    ui.register_panel('logic-gates', (-1, 2), logic_panel)

    utility_panel = CyclePanel('Utilities', utility_btns)
    ui.register_panel('utilities', (-1, 3), utility_panel)


IF = 2
ID = 2
EX = 3
MEM = 2
WRT = 2


INS_CYCLES = IF + ID + EX + MEM + WRT

def load_default_setup(canvas:Canvas, program:List[str]) -> None:
    '''WORK IN PROGRESS'''
    ins_mult = Multiplexer()
    ins_mult.width = 16
    ins_mult.signed = False
    ins_mult.center_on((400, 320))
    canvas.add_component(ins_mult)

    ins_reg = StageRegister()
    ins_reg._cycles = INS_CYCLES
    ins_reg._counter = INS_CYCLES - 1
    ins_reg.add_interstage_port('next-ins', 16, False)
    ins_reg.center_on((850, 320))
    canvas.add_component(ins_reg)

    wire = Wire(ins_mult.out_by_id['data'], ins_reg.in_by_id['next-ins'])
    canvas.add_wire(wire)

    ins_inc = Incrementer()
    ins_inc.center_on((1350, 260))
    canvas.add_component(ins_inc)

    wire = Wire(ins_reg.out_by_id['next-ins'], ins_inc.in_by_id['data'])
    wire.add_waypoint((1100, 320))
    wire.add_waypoint((1100, 260))
    canvas.add_wire(wire)

    wire = Wire(ins_inc.out_by_id['data'], ins_mult.in_by_id['input-0'])
    wire.add_waypoint((1600, 260))
    wire.add_waypoint((1600, 150))
    wire.add_waypoint((100, 150))
    wire.add_waypoint((100, 320))
    canvas.add_wire(wire)

    prog_mem = Memory()
    if program is not None:
        translation = translator.translate(program)
        prog_mem.load_program(translation)
    prog_mem._cycles = INS_CYCLES
    prog_mem._counter = INS_CYCLES
    prog_mem.center_on((1350, 490))
    canvas.add_component(prog_mem)   

    wire = Wire(ins_reg.out_by_id['next-ins'], prog_mem.in_by_id['address'])
    wire.add_waypoint((1100, 320))
    wire.add_waypoint((1100, 410))
    canvas.add_wire(wire)

    dec = Decoder()
    dec.center_on((900, 890))
    canvas.add_component(dec)

    wire = Wire(prog_mem.out_by_id['data'], dec.in_by_id['ins'])
    wire.add_waypoint((1600, 490))
    wire.add_waypoint((1600, 660))
    wire.add_waypoint((650, 660))
    wire.add_waypoint((650, 890))
    wire.tick()
    canvas.add_wire(wire)

    if_reg = StageRegister()
    if_reg._cycles = INS_CYCLES
    if_reg._counter = IF
    if_reg.add_interstage_port('imm', 16, True)
    if_reg.add_interstage_port('reg-w', 4, False)
    if_reg.add_interstage_port('reg-b', 4, False)
    if_reg.add_interstage_port('reg-a', 4, False)
    if_reg.add_interstage_port('opcode', 8, False)
    if_reg.center_on((1350, 890))
    canvas.add_component(if_reg)

    for port_id in ['imm', 'reg-w', 'reg-b', 'reg-a', 'opcode']:
        wire = Wire(dec.out_by_id[port_id], if_reg.in_by_id[port_id])
        canvas.add_wire(wire)

    con = ControlUnit()
    con.center_on((2100, 440))
    canvas.add_component(con)

    wire = Wire(if_reg.out_by_id['opcode'], con.in_by_id['opcode'])
    wire.add_waypoint((1650, 746))
    wire.add_waypoint((1650, 440))
    canvas.add_wire(wire)

    reg = Register()
    reg._cycles = INS_CYCLES
    reg._read_counter = IF + 1
    reg._write_counter = INS_CYCLES
    reg.center_on((2100, 910))
    canvas.add_component(reg)

    wire = Wire(if_reg.out_by_id['reg-a'], reg.in_by_id['reg-a'])
    wire.add_waypoint((1700, 818))
    wire.add_waypoint((1700, 766))
    canvas.add_wire(wire)

    wire = Wire(if_reg.out_by_id['reg-b'], reg.in_by_id['reg-b'])
    wire.add_waypoint((1750, 890))
    wire.add_waypoint((1750, 838))
    canvas.add_wire(wire)

    sign_ex = SignExtender()
    sign_ex.center_on((2100, 1200))
    canvas.add_component(sign_ex)

    wire = Wire(if_reg.out_by_id['imm'], sign_ex.in_by_id['imm'])
    wire.add_waypoint((1650, 1034))
    wire.add_waypoint((1650, 1200))
    canvas.add_wire(wire)

    left_sh = LeftShifter()
    left_sh.center_on((2100, 1370))
    canvas.add_component(left_sh)

    wire = Wire(if_reg.out_by_id['imm'], left_sh.in_by_id['imm'])
    wire.add_waypoint((1650, 1034))
    wire.add_waypoint((1650, 1370))
    canvas.add_wire(wire)

    id_reg_a = StageRegister()
    id_reg_a._cycles = INS_CYCLES
    id_reg_a._counter = IF + ID
    id_reg_a.add_interstage_port('alu-op', 4, False)
    id_reg_a.add_interstage_port('alu-b-src', 2, False)
    id_reg_a.add_interstage_port('alu-a-src', 1, False)
    id_reg_a.add_interstage_port('pc', 16, False)
    id_reg_a.add_interstage_port('mem-w', 1, False)
    id_reg_a.add_interstage_port('branch', 1, False)
    id_reg_a.add_interstage_port('wrt-src', 1, False)
    id_reg_a.add_interstage_port('reg-w-con', 1, False)
    id_reg_a.center_on((2750, 444))
    canvas.add_component(id_reg_a)

    for port_id in ['alu-op', 'alu-b-src', 'alu-a-src', 'mem-w', 'branch', 'wrt-src', 'reg-w-con']:
        wire = Wire(con.out_by_id[port_id], id_reg_a.in_by_id[port_id])
        canvas.add_wire(wire)

    wire = Wire(ins_inc.out_by_id['data'], id_reg_a.in_by_id['pc'])
    wire.add_waypoint((1600, 260))
    wire.add_waypoint((1600, 150))
    wire.add_waypoint((2450, 150))
    wire.add_waypoint((2450, 474))
    canvas.add_wire(wire)

    id_reg_b = StageRegister()
    id_reg_b._cycles = INS_CYCLES
    id_reg_b._counter = IF + ID
    id_reg_b.add_interstage_port('reg-w', 4, False)
    id_reg_b.add_interstage_port('imm', 16, True)
    id_reg_b.add_interstage_port('data-b')
    id_reg_b.add_interstage_port('sign-ext')
    id_reg_b.add_interstage_port('left-shift')
    id_reg_b.add_interstage_port('data-a')
    id_reg_b.center_on((2750, 970))
    canvas.add_component(id_reg_b)

    wire = Wire(reg.out_by_id['data-a'], id_reg_b.in_by_id['data-a'])
    canvas.add_wire(wire)

    wire = Wire(reg.out_by_id['data-b'], id_reg_b.in_by_id['data-b'])
    canvas.add_wire(wire)

    wire = Wire(sign_ex.out_by_id['data'], id_reg_b.in_by_id['sign-ext'])
    wire.add_waypoint((2350, 1200))
    wire.add_waypoint((2350, 940))
    canvas.add_wire(wire)

    wire = Wire(left_sh.out_by_id['data'], id_reg_b.in_by_id['left-shift'])
    wire.add_waypoint((2400, 1370))
    wire.add_waypoint((2400, 880))
    canvas.add_wire(wire)

    wire = Wire(if_reg.out_by_id['imm'], id_reg_b.in_by_id['imm'])
    wire.add_waypoint((1650, 1034))
    wire.add_waypoint((1650, 1480))
    wire.add_waypoint((2450, 1480))
    wire.add_waypoint((2450, 1060))
    canvas.add_wire(wire)

    wire = Wire(if_reg.out_by_id['reg-w'], id_reg_b.in_by_id['reg-w'])
    wire.add_waypoint((1700, 962))
    wire.add_waypoint((1700, 1530))
    wire.add_waypoint((2500, 1530))
    wire.add_waypoint((2500, 1120))
    canvas.add_wire(wire)

    pc_add = PCAdder()
    pc_add.center_on((3550, 504))
    canvas.add_component(pc_add)

    wire = Wire(id_reg_a.out_by_id['pc'], pc_add.in_by_id['data-a'])
    canvas.add_wire(wire)

    wire = Wire(id_reg_b.out_by_id['imm'], pc_add.in_by_id['data-b'])
    wire.add_waypoint((3200, 1060))
    wire.add_waypoint((3200, 534))
    canvas.add_wire(wire)

    alu_a = Multiplexer()
    alu_a.center_on((3550, 734))
    canvas.add_component(alu_a)

    wire = Wire(id_reg_a.out_by_id['alu-a-src'], alu_a.in_by_id['src'])
    wire.add_waypoint((3150, 534))
    wire.add_waypoint((3150, 814))
    canvas.add_wire(wire)

    wire = Wire(id_reg_b.out_by_id['data-a'], alu_a.in_by_id['input-0'])
    wire.add_waypoint((3000, 820))
    wire.add_waypoint((3000, 734))
    canvas.add_wire(wire)

    alu_b = Multiplexer()
    alu_b.n_inputs = 4
    alu_b.center_on((3550, 1084))
    canvas.add_component(alu_b)

    wire = Wire(id_reg_a.out_by_id['alu-b-src'], alu_b.in_by_id['src'])
    wire.add_waypoint((3100, 594))
    wire.add_waypoint((3100, 1228))
    canvas.add_wire(wire)

    wire = Wire(id_reg_b.out_by_id['data-b'], alu_b.in_by_id['input-0'])
    wire.add_waypoint((3150, 1000))
    wire.add_waypoint((3150, 1156))
    canvas.add_wire(wire)

    wire = Wire(id_reg_b.out_by_id['sign-ext'], alu_b.in_by_id['input-1'])
    wire.add_waypoint((3250, 940))
    wire.add_waypoint((3250, 1084))
    canvas.add_wire(wire)

    wire = Wire(id_reg_b.out_by_id['left-shift'], alu_b.in_by_id['input-2'])
    wire.add_waypoint((3300, 880))
    wire.add_waypoint((3300, 1012))
    canvas.add_wire(wire)

    alu = ALU()
    alu.center_on((4150, 734))
    canvas.add_component(alu)

    wire = Wire(alu_a.out_by_id['data'], alu.in_by_id['data-a'])
    wire.add_waypoint((3800, 734))
    wire.add_waypoint((3800, 654))
    canvas.add_wire(wire)

    wire = Wire(alu_b.out_by_id['data'], alu.in_by_id['data-b'])
    wire.add_waypoint((3850, 1084))
    wire.add_waypoint((3850, 734))
    canvas.add_wire(wire)

    wire = Wire(id_reg_a.out_by_id['alu-op'], alu.in_by_id['alu-op'])
    wire.add_waypoint((3050, 654))
    wire.add_waypoint((3050, 1300))
    wire.add_waypoint((3900, 1300))
    wire.add_waypoint((3900, 814))
    canvas.add_wire(wire)

    ex_reg = StageRegister()
    ex_reg._cycles = INS_CYCLES
    ex_reg._counter = IF + ID + EX
    ex_reg.add_interstage_port('reg-w', 4, False)
    ex_reg.add_interstage_port('data-b')
    ex_reg.add_interstage_port('result')
    ex_reg.add_interstage_port('flow-flag', 1, False)
    ex_reg.add_interstage_port('zero-flag', 1, False)
    ex_reg.add_interstage_port('pc', 16, False)
    ex_reg.add_interstage_port('mem-w', 1, False)
    ex_reg.add_interstage_port('branch', 1, False)
    ex_reg.add_interstage_port('wrt-src', 1, False)
    ex_reg.add_interstage_port('reg-w-con', 1, False)
    ex_reg.center_on((4850, 504))
    canvas.add_component(ex_reg)

    for port_id in ['mem-w', 'branch', 'wrt-src', 'reg-w-con']:
        wire = Wire(id_reg_a.out_by_id[port_id], ex_reg.in_by_id[port_id])
        canvas.add_wire(wire)

    wire = Wire(pc_add.out_by_id['data'], ex_reg.in_by_id['pc'])
    wire.add_waypoint((3800, 504))
    wire.add_waypoint((3800, 474))
    canvas.add_wire(wire)

    wire = Wire(alu.out_by_id['zero-flag'], ex_reg.in_by_id['zero-flag'])
    wire.add_waypoint((4400, 654))
    wire.add_waypoint((4400, 534))
    canvas.add_wire(wire)

    wire = Wire(alu.out_by_id['flow-flag'], ex_reg.in_by_id['flow-flag'])
    wire.add_waypoint((4450, 734))
    wire.add_waypoint((4450, 594))
    canvas.add_wire(wire)

    wire = Wire(id_reg_b.out_by_id['data-b'], ex_reg.in_by_id['data-b'])
    wire.add_waypoint((3150, 1000))
    wire.add_waypoint((3150, 1156))
    wire.add_waypoint((3300, 1156))
    wire.add_waypoint((3300, 1350))
    wire.add_waypoint((4550, 1350))
    wire.add_waypoint((4550, 714))
    canvas.add_wire(wire)

    wire = Wire(alu.out_by_id['data'], ex_reg.in_by_id['result'])
    wire.add_waypoint((4500, 814))
    wire.add_waypoint((4500, 654))
    canvas.add_wire(wire)

    wire = Wire(id_reg_b.out_by_id['reg-w'], ex_reg.in_by_id['reg-w'])
    wire.add_waypoint((3000, 1120))
    wire.add_waypoint((3000, 1400))
    wire.add_waypoint((4600, 1400))
    wire.add_waypoint((4600, 774))
    canvas.add_wire(wire)

    wire = Wire(ex_reg.out_by_id['pc'], ins_mult.in_by_id['input-1'])
    wire.add_waypoint((5100, 474))
    wire.add_waypoint((5100, 100))
    wire.add_waypoint((150, 100))
    wire.add_waypoint((150, 240))
    canvas.add_wire(wire)

    br_and = AndGate()
    br_and.center_on((5550, 384))
    canvas.add_component(br_and)

    wire = Wire(ex_reg.out_by_id['branch'], br_and.in_by_id['data-a'])
    canvas.add_wire(wire)

    wire = Wire(ex_reg.out_by_id['zero-flag'], br_and.in_by_id['data-b'])
    wire.add_waypoint((5200, 534))
    wire.add_waypoint((5200, 414))
    canvas.add_wire(wire)

    wire = Wire(br_and.out_by_id['data'], ins_mult.in_by_id['src'])
    wire.add_waypoint((5800, 384))
    wire.add_waypoint((5800, 50))
    wire.add_waypoint((50, 50))
    wire.add_waypoint((50, 400))
    canvas.add_wire(wire)

    data_mem = Memory()
    data_mem._cycles = INS_CYCLES
    data_mem._counter = IF + ID + EX + 1
    data_mem.center_on((5550, 734))
    canvas.add_component(data_mem)

    wire = Wire(ex_reg.out_by_id['result'], data_mem.in_by_id['address'])
    canvas.add_wire(wire)

    wire = Wire(ex_reg.out_by_id['data-b'], data_mem.in_by_id['data'])
    wire.add_waypoint((5200, 714))
    wire.add_waypoint((5200, 734))
    canvas.add_wire(wire)

    wire = Wire(ex_reg.out_by_id['mem-w'], data_mem.in_by_id['mem-w'])
    wire.add_waypoint((5150, 414))
    wire.add_waypoint((5150, 814))
    canvas.add_wire(wire)

    mem_reg = StageRegister()
    mem_reg._cycles = INS_CYCLES
    mem_reg._counter = IF + ID + EX + MEM
    mem_reg.add_interstage_port('wrt-src', 1, False)
    mem_reg.add_interstage_port('alu-data')
    mem_reg.add_interstage_port('mem-data')
    mem_reg.add_interstage_port('reg-w', 4, False)
    mem_reg.add_interstage_port('reg-w-con', 1, False)
    mem_reg.center_on((6100, 734))
    canvas.add_component(mem_reg)

    wire = Wire(ex_reg.out_by_id['reg-w-con'], mem_reg.in_by_id['reg-w-con'])
    wire.add_waypoint((5850, 234))
    wire.add_waypoint((5850, 590))
    canvas.add_wire(wire)

    wire = Wire(ex_reg.out_by_id['reg-w'], mem_reg.in_by_id['reg-w'])
    wire.add_waypoint((5100, 774))
    wire.add_waypoint((5100, 594))
    wire.add_waypoint((5800, 594))
    wire.add_waypoint((5800, 662))
    canvas.add_wire(wire)

    wire = Wire(data_mem.out_by_id['data'], mem_reg.in_by_id['mem-data'])
    canvas.add_wire(wire)

    wire = Wire(ex_reg.out_by_id['result'], mem_reg.in_by_id['alu-data'])
    wire.add_waypoint((5300, 654))
    wire.add_waypoint((5300, 900))
    wire.add_waypoint((5800, 900))
    wire.add_waypoint((5800, 806))
    canvas.add_wire(wire)

    wire = Wire(ex_reg.out_by_id['wrt-src'], mem_reg.in_by_id['wrt-src'])
    wire.add_waypoint((5250, 294))
    wire.add_waypoint((5250, 950))
    wire.add_waypoint((5850, 950))
    wire.add_waypoint((5850, 878))
    canvas.add_wire(wire)

    wrt_mult = Multiplexer()
    wrt_mult.center_on((6600, 806))
    canvas.add_component(wrt_mult)

    wire = Wire(mem_reg.out_by_id['mem-data'], wrt_mult.in_by_id['input-1'])
    wire.add_waypoint((6350, 734))
    wire.add_waypoint((6350, 726))
    canvas.add_wire(wire)

    wire = Wire(mem_reg.out_by_id['alu-data'], wrt_mult.in_by_id['input-0'])
    canvas.add_wire(wire)

    wire = Wire(mem_reg.out_by_id['wrt-src'], wrt_mult.in_by_id['src'])
    wire.add_waypoint((6350, 878))
    wire.add_waypoint((6350, 886))
    canvas.add_wire(wire)

    wire = Wire(mem_reg.out_by_id['reg-w-con'], reg.in_by_id['reg-w-con'])
    wire.add_waypoint((6950, 590))
    wire.add_waypoint((6950, 1680))
    wire.add_waypoint((1850, 1680))
    wire.add_waypoint((1850, 910))
    canvas.add_wire(wire)

    wire = Wire(mem_reg.out_by_id['reg-w'], reg.in_by_id['reg-w'])
    wire.add_waypoint((6900, 662))
    wire.add_waypoint((6900, 1630))
    wire.add_waypoint((1800, 1630))
    wire.add_waypoint((1800, 982))
    canvas.add_wire(wire)

    wire = Wire(wrt_mult.out_by_id['data'], reg.in_by_id['data-w'])
    wire.add_waypoint((6850, 806))
    wire.add_waypoint((6850, 1580))
    wire.add_waypoint((1750, 1580))
    wire.add_waypoint((1750, 1054))
    canvas.add_wire(wire)