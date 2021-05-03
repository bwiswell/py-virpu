from typing import List, Tuple, Union
from pickle import load
from os.path import dirname, realpath

from bitarray import bitarray
from bitarray.util import int2ba

PATH_PREFIX = dirname(realpath(__file__)) + '\\data\\'
CONTROL_BITS_PATH = 'control-bits.pkl'
OPCODES_PATH = 'opcodes.pkl'

control_bits = None
opcodes = None

def init() -> None:
    global assembly_codes, control_bits, opcodes
    try:
        with open(PATH_PREFIX + CONTROL_BITS_PATH, 'rb') as file:
            control_bits = load(file)
        with open(PATH_PREFIX + OPCODES_PATH, 'rb') as file:
            opcodes = load(file)
    except:
        raise SystemExit('Error: Unable to load corium language!')

def get_control_bits() -> List[bitarray]:
    global control_bits
    return control_bits

def get_opcode(opcode_alias:Union[str, int]) -> int:
    global opcodes
    if isinstance(opcode_alias, int):
        return opcodes[opcode_alias]
    else:
        for opcode in opcodes:
            if opcode['a-code'] == opcode_alias:
                return opcode

def get_a_code(opcode_alias:Union[str, int]) -> str:
    return get_opcode(opcode_alias)['a-code']

def get_arg_types(opcode_alias:Union[str, int]) -> List[str]:
    arg_dests = get_opcode(opcode_alias)['arg-types']
    return [arg.split('-')[0] for arg in arg_dests]

def get_arg_dests(opcode:int) -> List[str]:
    return get_opcode(opcode)['arg-types']        

def get_m_code(opcode_alias:Union[str, int]) -> bitarray:
    value = get_opcode(opcode_alias)['m-code']
    return int2ba(value, 8, signed=False)