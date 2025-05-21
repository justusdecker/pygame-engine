#gcc -fPIC -shared -o
import ctypes
clib = ctypes.CDLL('data\\clib.so')
clib.display()