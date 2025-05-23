#gcc -fPIC -shared -o

from data.modules.graphics_rendering import color_line
from pygame import surfarray,image

image.save(surfarray.make_surface(color_line()),'test.png')