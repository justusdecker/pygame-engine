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






a.fill([255,255,255])

c = Surfarray([1,1],True).load_from_file('data\\bin\\img\\stone.png')
print(c.blit(b,[5,5]))
c.array = ocv.resize(c.get_array(),dsize=(128,128))

#b.fill([255,255,255],(32,32,32,32))
#print(b.get_array())
image.save(surfarray.make_surface(c.get_array()),'test.png',)

#img = surfarray.array3d(image.load("data\\bin\\img\\stone.png")).reshape((32*32*3)).tolist()



#image.save(blending_mul(image.load("data\\bin\\img\\stone.png"),image.load("data\\bin\\img\\stone_with_window.png")),'test.png') # surfarray.make_surface(color_correction(img,0.7,32,32))