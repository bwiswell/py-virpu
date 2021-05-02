from typing import List

from bitarray import bitarray

def translate_line(assembly_line:str) -> bitarray:
    args = assembly_line.split(' ')

def translate(assembly_lines:List[str]) -> List[bitarray]:
    return [translate_line(line) for line in assembly_lines]
