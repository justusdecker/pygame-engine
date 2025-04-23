from typing import Any, BinaryIO, Dict, Union, overload, Iterable
type initializer = Union[str, Iterable[int], None]
from sys import getsizeof
class BitArray:
    def __init__(self,
                 initializer: initializer):
        self.parse(initializer)
    def parse(self,initializer):
        l = len(initializer)
        self.bit_array = 1 << l - 1
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
            f_out.write(
                self.bit_array.to_bytes(4,'big')
            )
    def fromfile(self,file_path:str):
        with open(file_path,'rb') as f_in:
            
            self.parse(bin(int(f_in.read(),2))[2:])
BA = BitArray("10101010")
print(BA.to01())
BA.append("101")
print(BA.to01())

print(BA.get_size())
BA.tofile('test.bin')
#BA.fromfile('test.bin')