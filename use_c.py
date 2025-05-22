#gcc -fPIC -shared -o
import ctypes
from time import perf_counter
clib = ctypes.CDLL('data\\c_lib.so')
def conv(a: int):
    return a ** 2


def run_10M():
    t = perf_counter()
    for i in range(19_000_000):
        conv(i)
    dt = perf_counter() - t
    print(f"finished python code in {dt}")
    return dt
t = perf_counter()
clib.run_10m()
dt_a = perf_counter() - t
print(f"finished c code in {dt_a}")
dt_b = run_10M()
print(f"The calculated delta time between python & C is {(dt_b / dt_a) * 100:.2f}%")