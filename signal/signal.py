from __future__ import annotations

from typing import Tuple

from bitarray import bitarray
from bitarray.util import ba2int, int2ba

class Signal:
    def __init__(self, value:int=0, data_width:int=32, signed:bool=True):
        self.value = value
        self.data_width = data_width
        self.signed = signed
        self.bits = int2ba(value, data_width, signed=signed)

    @classmethod
    def from_bits(cls, 
                    bits:bitarray, 
                    data_width:int=32, 
                    signed:bool=True
                ) -> Signal:
        value = ba2int(bits, signed)
        return Signal(value=value, data_width=data_width, signed=signed)

    @classmethod
    def left_shift(cls, signal:Signal, target_width:int=32) -> Signal:
        zeros = '0' * (target_width - signal.data_width)
        zero_bits = bitarray(zeros)
        bits = signal.bits + zero_bits
        return Signal.from_bits(bits, target_width, signal.signed)

    @classmethod
    def sign_extend(cls, signal:Signal, target_width:int=32) -> Signal:
        return Signal(signal.value, target_width)

    def __str__(self) -> str:
        type_text = f'{"un" if not self.signed else ""}signed '
        type_text += f'{self.data_width}-bit int'
        return f'{self.value} + ({type_text})'

    def is_nonzero(self) -> bool:
        return self.bits.any()

    def __invert__(self) -> Signal:
        return Signal.from_bits(~self.bits, self.data_width, self.signed)

    def __or__(self, other:Signal) -> Signal:
        result = self.bits | other.bits
        result_width = max(self.data_width, other.data_width)
        signed = self.signed or other.signed
        return Signal.from_bits(result, result_width, signed)

    def __and__(self, other:Signal) -> Signal:
        result = self.bits & other.bits
        result_width = max(self.data_width, other.data_width)
        signed = self.signed or other.signed
        return Signal.from_bits(result, result_width, signed)

    def plus(self, other:Signal, carry_in:bool=False) -> Tuple[Signal, bool]:
        result_width = max(self.data_width, other.data_width)
        sum_bits = bitarray(result_width)
        sum_bits.setall(0)
        carry = carry_in
        for i in range(result_width - 1, -1, -1):
            bit_sum = self.bits[i] + other.bits[i] + carry
            sum_bits[i] = bit_sum % 2
            carry = bit_sum > 1
        signed = self.signed or other.signed
        return Signal.from_bits(sum_bits, result_width, signed), carry

    def __add__(self, other:Signal) -> Signal:
        sum_signal, _ = self.plus(other)
        return sum_signal

    def minus(self, other:Signal) -> Tuple[Signal, bool]:
        return self.plus(~other, True)

    def __sub__(self, other:Signal) -> Signal:
        diff_signal, _ = self.minus(other)
        return diff_signal