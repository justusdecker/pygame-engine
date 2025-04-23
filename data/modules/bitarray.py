from typing import Any, BinaryIO, Dict, Union, overload, Iterable
type initializer = Union[str, Iterable[int], None]
from math import ceil
from sys import getsizeof
class BitArray:
    def __init__(self,
                 initializer: initializer):
        self.parse(initializer)
        
    def parse(self,initializer):
        l = len(initializer)
        self.bit_array = 1 << l - 1

        #elf.first_bit_is_zero = initializer[0] == 0
        self.bit_array |= int(initializer,2)
    def append(self,initializer:initializer):
        _01 = self.to01()
        self.parse(_01 + initializer)
    def insert(self,initializer:initializer):
        _01 = self.to01()
        self.parse(initializer + _01)
    def to01(self) -> str:
        return bin(self.bit_array)[2:]
    def get_size(self):
        return getsizeof(self.bit_array)
    def tofile(self,file_path:str):
        with open(file_path,'wb') as f_out:
            bl = self.bit_array.bit_length()
            f_out.write(
                self.bit_array.to_bytes(ceil(bl/4),'little')
            )
    def fromfile(self,file_path:str):
        with open(file_path,'rb') as f_in:
            byte_array = ''
            for byte in f_in.read():
                byte_array += bin(int(byte))[2:]
            self.parse(byte_array)
            print(byte_array)
            
BA = BitArray("10101010")
print(BA.to01(),BA.bit_array)
BA.append("101")
print(BA.to01(),BA.bit_array)
BA.tofile('test.bin')
#print(BA.bit_array, BA.to01())
BA.fromfile('test.bin')
#print(BA.bit_array, BA.to01())
