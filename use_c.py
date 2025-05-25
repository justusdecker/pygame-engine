#gcc -fPIC -shared -o

from data.modules.graphics_rendering import color_line,surf_to_1d
from pygame import surfarray,image
from time import perf_counter
from data.modules.data_management import DM

def testEnvoirment():
    t = perf_counter()
    
    #your test function here
    surf_to_1d(image.load("data\\bin\\img\\stone.png"))
    
    print(perf_counter() - t)
def testEnvoirment1():
    t = perf_counter()
    
    #your test function here
    surfarray.array3d(image.load("data\\bin\\img\\stone.png")).reshape((32*32*3))
    
    print(perf_counter() - t)
testEnvoirment1()
testEnvoirment()


#image.save(surfarray.make_surface(line_test()),'test.png')