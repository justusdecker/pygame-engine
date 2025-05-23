#gcc -fPIC -shared -o

from data.modules.graphics_rendering import color_line,line_test
from pygame import surfarray,image

image.save(surfarray.make_surface(line_test()),'test.png')