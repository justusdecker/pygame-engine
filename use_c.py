#gcc -fPIC -shared -o

from data.modules.graphics_rendering import color_line,surf_to_1d
from data.modules.grop import gamma_correction,invert_rgb,blending_mul
from pygame import surfarray,image
from time import perf_counter
from data.modules.data_management import DM


img = surfarray.array3d(image.load("data\\bin\\img\\stone.png")).reshape((32*32*3)).tolist()



image.save(blending_mul(image.load("data\\bin\\img\\stone.png"),image.load("data\\bin\\img\\stone_with_window.png")),'test.png') # surfarray.make_surface(color_correction(img,0.7,32,32))