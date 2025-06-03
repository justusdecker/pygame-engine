#gcc -fPIC -shared -o

from data.modules.graphics_rendering import color_line,surf_to_1d
from data.modules.grop import gamma_correction,invert_rgb,blending_mul
from pygame import surfarray,image
from time import perf_counter
from data.modules.data_management import DM

from data.modules.kernel.opt_surfarray import Surfarray
a = Surfarray((15,15))
b = Surfarray((16,16))


x, y = -5, 5
w, h = 10,10
"""
Pseudo code:
if x < 0
    x = x+w
    w = w+abs(x)
"""

import cv2 as ocv


# Test Envoirment

A = Surfarray().load_from_file('data\\bin\\img\\stone.png')

B = Surfarray().load_from_file('data\\bin\\img\\stone_with_window.png')

# 1. fill without args [COMP FILL]

#!A.fill((255,255,255,255))

#A.fill((255,255,255))
#A.array
#A.blit(B,(0,0))
#A.blit(B,(-64,-64))
#A.blit(B,(64,64))
#A.blit(B,(-16,16))
#A.blit(B,(16,-16))

A.array

# NO UINT8 --> UINT64 CONVERSION IN THIS PART

#A.resize((64,64))
#180 87 2 83


C = A.resize((256,256))
image.save(C.get_surface(),'test.png')
D = C.subarray((180,87,8,83))
image.save(D.get_surface(),'test1.png')
E = C.subarray((0,0,8,256))
image.save(E.get_surface(),'test2.png')
pass
#b.fill([255,255,255],(32,32,32,32))
#print(b.get_array())
#image.save(surfarray.make_surface(c.get_array()),'test.png',)

#img = surfarray.array3d(image.load("data\\bin\\img\\stone.png")).reshape((32*32*3)).tolist()



#image.save(blending_mul(image.load("data\\bin\\img\\stone.png"),image.load("data\\bin\\img\\stone_with_window.png")),'test.png') # surfarray.make_surface(color_correction(img,0.7,32,32))