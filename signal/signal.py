from __future__ import annotations

from math import pow
from typing import Tuple, Union

from bitarray import bitarray
from bitarray.util import ba2int, int2ba

class Signal:
    '''
    A class to represent bit signals and their decimal values.

    Signals act as immutable objects (i.e. the bits, width, signage, and value
    are not modifiable.)

    Attributes:
        bits (bitarray): the individual bits that make up the signal
        width (int): the bit-width of the signal
        signed (bool): the signage of the signal
        value (int): the integer value of the signal
    '''
    def __init__(self, bits:bitarray=None, width:int=32, signed:bool=True):
        '''
        Initialize the signal and compute the decimal value.
        
        Parameters:
            bits: the individual bits that make up the signal (default None)
            width: the bit-width of the signal (default 32)
            signed: the signage of the signal (default True)
        '''
        self._bits = bits
        if bits is None:
            self._bits = bitarray(width)
            self._bits.setall(0)
        self._width = width
        self._signed = signed
        self._value = ba2int(self._bits, signed=signed)

    @classmethod
    def from_value(cls, value:int, width:int=32, signed:bool=True) -> Signal:
        '''
        Create a signal from an integer value instead of a bitarray.
        
        Parameters:
            value: the integer value of the signal
            width: the bit-width of the signal (default 32)
            signed: the signage of the signal (default True)
        '''
        if signed:
            if value < 0:
                min_signal_val = -int(pow(2, width // 2))
                value = max(min_signal_val, value)
            else:
                max_signal_val = int(pow(2, width // 2)) - 1
                value = min(max_signal_val, value)
        else:
            if value < 0:
                value = 0
            else:
                max_signal_val = int(pow(2, width))
                value = min(max_signal_val, value)
        bits = int2ba(value, width, signed=signed)
        return Signal(bits)

    @classmethod
    def from_bool(cls, value:bool) -> Signal:
        '''
        Create a signal from an boolean value instead of a bitarray.
        
        Parameters:
            value: the boolean value of the signal
        '''
        return Signal(int(value), 1, False)

    @property
    def bits(self) -> bitarray:
        '''Get the bits that make up the signal. Setting is disallowed.'''
        return self._bits

    @property
    def width(self) -> int:
        '''Get the bit width of the signal. Setting is disallowed.'''
        return self._width

    @property
    def signed(self) -> bool:
        '''Get the signage of the signal. Setting is disallowed.'''
        return self._signed

    @property
    def value(self) -> int:
        '''Get the decimal value of the signal. Setting is disallowed.'''
        return self._value

    def __str__(self) -> str:
        '''Return a string representation of the signal.'''
        text = f'{"s" if self._signed else "u"}'
        text += f'{self._width}'
        return f'{self.value} ({text})'

    def __getitem__(self, key:object) -> bitarray:
        '''Return a bit or slice of bits from the signal.'''
        return self._bits[key]

    def __bool__(self) -> bool:
        '''Return False if the signal's decimal value is 0 else True.'''
        return self._bits.any()

    def __invert__(self) -> Signal:
        '''Return the result of inverting each bit of the signal.'''
        return Signal(~self._bits, self._width, self._signed)

    def __or__(self, other:Signal) -> Signal:
        '''
        Return the result of a bitwise OR over two signals.

        This operation retains the signage of the signal that self refers to.
        '''
        if self._width != other.width:
            raise ValueError('Signal bit-widths must match!')
        bits = self._bits | other.bits
        return Signal(bits, self._width, self._signed)

    def __and__(self, other:Signal) -> Signal:
        '''
        Return the result of a bitwise AND over two signals.

        This operation retains the signage of the signal that self refers to.
        '''
        if self._width != other.width:
            raise ValueError('Signal bit-widths must match!')
        bits = self._bits & other.bits
        return Signal(bits, self._width, self._signed)

    def __add__(self, other:Union[Signal, int]) -> Tuple[Signal, bool]:
        '''
        Return the result and overflow flag of adding two signals or a signal
        and an int.

        This operation retains the signage of the signal that self refers to.
        '''
        if isinstance(other, int):
            other = Signal.from_value(other, self._width, self._signed)
        if self._width != other.width:
            raise ValueError('Signal bit-widths must match!')
        bits = bitarray(self._width)
        carry = False
        for i in range(self._width - 1, -1, -1):
            bit_res = self[i] + other[i] + carry
            bits[i] = bit_res % 2
            carry = bit_res > 1
        return Signal(bits, self._width, self._signed), carry

    def plus(self, other:Signal, carry_in:bool=False) -> Tuple[Signal, bool]:
        
        '''
        Return the result and overflow flag of adding two signals.

        This version of addition allows for a carry in value. This operation
        retains the signage of the signal that self refers to.

        Parameters:
            other: the signal to add to this signal
            carry_in: the carry in to the add operation (default False)
        '''
        carry_sum, carry_overflow = self + int(carry_in)
        val_sum, val_overflow = carry_sum + other
        return val_sum, carry_overflow or val_overflow

    def __sub__(self, other:Signal) -> Tuple[Signal, bool]:
        '''
        Return the result and underflow flag of subtracting a signal.

        This operation retains the signage of the signal that self refers to.
        '''
        return self.plus(~other, True)