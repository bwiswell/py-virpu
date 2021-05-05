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
    '''Initialize Corium assembly and machine code data.'''
    global assembly_codes, control_bits, opcodes
    try:
        with open(PATH_PREFIX + CONTROL_BITS_PATH, 'rb') as file:
            control_bits = load(file)
        with open(PATH_PREFIX + OPCODES_PATH, 'rb') as file:
            opcodes = load(file)
    except:
        raise SystemExit('Error: Unable to load corium language!')

def get_control_bits() -> List[bitarray]:
    '''Get a list of bitarrays of control bits indexed by opcode.'''
    global control_bits
    return control_bits

def get_opcode(opcode_alias:Union[str, int]) -> int:
    '''
    Get opcode information by assembly name or decimal opcode.
    
    Information includes argument types for each opcode.

    Parameters:
        opcode_alias: assembly name (i.e. 'SUB') or opcode number
    '''
    global opcodes
    if isinstance(opcode_alias, int):
        return opcodes[opcode_alias]
    else:
        for opcode in opcodes:
            if opcode['a-code'] == opcode_alias:
                return opcode

def get_a_code(opcode_alias:Union[str, int]) -> str:
    '''Get the assembly name (i.e. 'SUB') of a given opcode.'''
    return get_opcode(opcode_alias)['a-code']

def get_arg_types(opcode_alias:Union[str, int]) -> List[str]:
    '''Get the argument types of a given opcode.'''
    arg_dests = get_opcode(opcode_alias)['arg-types']
    return [arg.split('-')[0] for arg in arg_dests]

def get_arg_dests(opcode:int) -> List[str]:
    '''Get the argument destination ports of a given opcode.'''
    return get_opcode(opcode)['arg-types']        

def get_m_code(opcode_alias:Union[str, int]) -> bitarray:
    '''Get the decimal opcode number of a given opcode.'''
    value = get_opcode(opcode_alias)['m-code']
    return int2ba(value, 8, signed=False)