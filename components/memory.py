from typing import List, Union

from bitarray import bitarray

from .component import Component
from .ioport import IOPort
from ..core import logger
from ..signal.signal import Signal

class Memory(Component):
    '''
    A class to represent a memory cell that extends Component.
    
    This class is a functional logic component that retrieves or stores data 
    at a given memory address.

    Attributes:
        data (List[Signal]): the memory contents indexed by memory address
    '''

    MAX_MEM = 65536

    def __init__(self):
        '''Initialize the Memory object and extend Component.'''
        add_port = IOPort('address', 'address', 'in', 16, False)
        data_port = IOPort('data', 'data', 'in')
        con_port = IOPort('mem-w', 'control', 'in', 1, False)
        in_ports = [add_port, data_port, con_port]
        out_ports = [IOPort('data', 'data', 'out')]
        Component.__init__(self,
                            comp_name='Memory',
                            in_ports=in_ports,
                            out_ports=out_ports,
                            config_options='t'
                        )
        self._data = [Signal.from_value(i) for i in range(Memory.MAX_MEM)]

    def __getitem__(self, key:object) -> Union[Signal, List[Signal]]:
        '''Return a signal or slice of signals from the memory cell.'''
        return self._data[key]

    def load_program(self, program:List[bitarray]) -> None:
        '''Load a program into memory.'''
        self._label = 'Program'
        self.out_by_id['data'].signed = False
        mem = [Signal(bitarr, signed=False) for bitarr in program]
        rem_mem = Memory.MAX_MEM - len(mem)
        mem_ext = [Signal.from_value(i, signed=False) for i in range(rem_mem)]
        mem.extend(mem_ext)
        self._data = mem
        self._execute()
        
    def _execute(self) -> None:
        '''
        Execute the memory's functional logic.

        The memory retrieves or stores data at a given memory address.
        '''
        address = self.in_by_id['address'].value
        if bool(self.in_by_id['mem-w'].value):
            value = self.in_by_id['data'].value
            self._data[address.value] = value
            logger.log(f'Memory: wrote {value} to address {hex(address.value)}')
        else:
            self.out_by_id['data'].value = self._data[address.value]