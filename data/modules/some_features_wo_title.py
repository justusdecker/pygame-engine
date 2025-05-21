from math import sqrt, degrees, atan2,radians,cos,sin
from time import perf_counter


import struct

def inverse_rsqrt(number): #Faster SQRT FUNCTION
    threehalfs = 1.5
    x2 = number * 0.5
    y = number

    # evil floating point bit level hacking
    i = struct.unpack('I', struct.pack('f', y))[0]
    i = 0x5f3759df - (i >> 1)
    y = struct.unpack('f', struct.pack('I', i))[0]

    # 1st iteration
    y = y * (threehalfs - (x2 * y * y))

    # y = y * (threehalfs - (x2 * y * y))
    result_bits = struct.unpack('I', struct.pack('f', y))[0]
    size = struct.calcsize('I')

    if result_bits < 0 or result_bits >= (1 << (size * 8)):
        raise ValueError('result_bits out of range')

    return struct.unpack('f', struct.pack('I', result_bits))[0]
    
def distance_bw_points(x1,y1,x2,y2) -> float:
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)
def distance_bwi_points(x1,y1,x2,y2) -> float:
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Unittesting for sqrt

t = perf_counter()
dbwp1 = f'{distance_bw_points(3,4,4,3):.5f}'
t = perf_counter() - t
print(f'{dbwp1} in {t*1_000:.4f}ms') #should be 1.41421

t = perf_counter()
dbwp1 = f'{distance_bwi_points(3,4,4,3):.5f}'
t = perf_counter() - t
print(f'{dbwp1} in {t*1_000:.4f}ms') #should be 1.41421

#unit: movement



sin
cos
atan2