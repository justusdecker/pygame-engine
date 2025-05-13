from pygame import Surface
from sys import setrecursionlimit
def dfs(surf: Surface,i,j,old_color,new_color):
    "!RECURSIVE FUNCTION!"
    n, m = surf.get_size()
    if i < 0 or i >= n or j < 0 or j >= m or surf.get_at((i,j)) != old_color:
        #?Pixel is out of range or already recolored
        return
    else:
        surf.set_at((i,j),new_color)
        dfs(surf,i+1,j,old_color,new_color)
        dfs(surf,i-1,j,old_color,new_color)
        dfs(surf,i,j+1,old_color,new_color)
        dfs(surf,i,j-1,old_color,new_color)
def flood_fill(surf,i,j,new_color):
    setrecursionlimit(50000)
    old_color = surf.get_at((i,j))
    if old_color == new_color:
        return
    dfs(surf,i,j,old_color,new_color)
    setrecursionlimit(1000)