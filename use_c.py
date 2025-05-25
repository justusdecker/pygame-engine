#gcc -fPIC -shared -o

from data.modules.graphics_rendering import color_line,surf_to_1d,invert_rgb,color_correction
from pygame import surfarray,image
from time import perf_counter
from data.modules.data_management import DM


img = surfarray.array3d(image.load("data\\bin\\img\\stone.png")).reshape((32*32*3)).tolist()



image.save(surfarray.make_surface(color_correction(img,0.7)),'test.png')