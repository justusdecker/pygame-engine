import pygame as pg
import math
from data.modules.constants import WIDTH, HALF_WIDTH, HALF_HEIGHT
FOV = math.pi / 3
H_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
H_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20
SCREEN_DIST = HALF_WIDTH / math.tan(H_FOV)
SCALE = WIDTH // NUM_RAYS
class RayCasting:
    def __init__(self,app):
        self.app = app
    def ray_cast(self):
        px, py = self.app.player.pos
        mx, my = self.app.player.map_pos
        ray_angle = self.app.player.angle - H_FOV + 0.0001 #The small number is here to prevent further ZeroDivision Errors!
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)
            
            #horizontals
            
            y_hor, dy = (my + 1, 1) if sin_a > 0 else (my - 1e-6, -1)
            
            depth_hor = (y_hor - py) / sin_a
            x_hor = px + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a
            
            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.app.map.world_map:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth
            
            #verticals
            
            x_vert, dx = (mx + 1, 1) if cos_a > 0 else (mx - 1e-6, -1)
            
            depth_vert = (x_vert - px) / cos_a
            y_vert = py + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a
            
            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.app.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
            
            # depth
            
            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor
            
            # debug drawing
            
            #pg.draw.line(self.app.window.surface,'yellow',(100*px,100*py),(100*px+100*depth*cos_a,100*py+100*depth*sin_a),2)
            
            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)
            
            # draw walls
            
            pg.draw.rect(self.app.window.surface,'white',
                         (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
            ray_angle += DELTA_ANGLE
    def update(self):
        self.ray_cast()