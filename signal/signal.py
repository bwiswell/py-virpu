from __future__ import annotations

from math import pow
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

    @classmethod
    def zero_extend(cls, signal:Signal, target_width:int=32) -> Signal:
        n_zeros = target_width - signal.data_width
        if n_zeros > 0:
            zeros = bitarray(''.join(['0' for _ in range(n_zeros)]))
            value = ba2int(zeros + signal.bits, signal.signed)
            return Signal(value, target_width, signal.signed)
        else:
            return signal

    def min_val(self) -> int:
        return int(-pow(2, self.data_width / 2)) if self.signed else 0

    def max_val(self) -> int:
        power = self.data_width / 2 if self.signed else self.data_width
        return int(pow(2, power) - 1)

    def get_signed(self) -> bool:
        return self.signed

    def __str__(self) -> str:
        type_text = f'{"s" if self.signed else "u"}'
        type_text += f'{self.data_width}'
        return f'{self.value} ({type_text})'

    def __getitem__(self, key:object) -> bitarray:
        return self.bits[key]

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

    def incr_val(self, dir:str) -> None:
        if dir == '+':
            new_val = self.value + 1
            if new_val > self.max_val():
                new_val = self.min_val()
        else:
            new_val = self.value - 1
            if new_val < self.min_val():
                new_val = self.max_val()
        self.value = new_val
        self.bits = int2ba(new_val, self.data_width, signed=self.signed)