from pygame import Surface
from queue import Queue
def flood_fill(surf: Surface,i,j,new_color):
    n, m = surf.get_size()
    old_color = surf.get_at((i,j))
    if old_color == new_color:
        return
    queue = Queue()
    queue.put((i,j))
    while not queue.empty():
        i,j = queue.get()
        if i < 0 or i >= n or j < 0 or j >= m or surf.get_at((i,j)) != old_color:
            continue
        else:
            surf.set_at((i,j),new_color)
            queue.put((i+1,j))
            queue.put((i-1,j))
            queue.put((i,j+1))
            queue.put((i,j-1))