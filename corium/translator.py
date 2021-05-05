from math import pow
from typing import List

from bitarray import bitarray
from bitarray.util import int2ba

from . import corium

MIN_IMM = int(-pow(2, 8))
MAX_IMM = int(pow(2, 8)) - 1
MIN_REG = 0
MAX_REG = 15

def translate_line(assembly_line:str) -> bitarray:
    '''Translate a line of assembly code to bit instructions.'''
    symbols = assembly_line.split(' ')
    a_code = symbols[0]
    exp_args = corium.get_arg_types(a_code)
    act_args = symbols[1:]
    bits = bitarray(0)
    bit_count = 0

    if len(exp_args) < len(act_args):
        raise SyntaxError(f'Too many args for command {a_code}!')
    elif len(exp_args) > len(act_args):
        raise SyntaxError(f'Not enough args for command {a_code}!')
    else:
        bits = corium.get_m_code(a_code)
        bit_count += 8

    for i in range(len(act_args)):
        arg = int(act_args[i])
        arg_type = exp_args[i]
        if arg_type == 'imm' and arg < MIN_IMM:
            raise ValueError(f'Min value for an immediate is {MIN_IMM}!')
        elif arg_type == 'imm' and arg > MAX_IMM:
            raise ValueError(f'Max value for an immediate is {MAX_IMM}!')
        elif arg_type == 'imm':
            imm = int2ba(arg, 16, signed=True)
            bits += imm
            bit_count += 16
        elif arg < MIN_REG:
            raise ValueError(f'Min value for a register is {MIN_REG}!')
        elif arg > MAX_REG:
            raise ValueError(f'Max value for a register is {MAX_REG}!')
        else:
            reg = int2ba(arg, 4, signed=False)
            bits += reg
            bit_count += 4

    zeros = '0' * (32 - bit_count)
    zero_bits = bitarray(zeros)
    bits += zero_bits

    return bits

def translate(assembly_lines:List[str]) -> List[bitarray]:
    '''Translate a list of assembly code lines to a list of bit instructions.'''
    return [translate_line(line) for line in assembly_lines]