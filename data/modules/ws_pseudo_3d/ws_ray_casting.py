import pygame as pg
import math
from data.modules.constants import WIDTH, HALF_WIDTH, HALF_HEIGHT, HEIGHT
from data.modules.ws_pseudo_3d.ws_object_renderer import TEXTURE_SIZE,H_TEXTURE_SIZE

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
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.app.object_renderer.wall_textures
    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values
            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column,(SCALE,proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), H_TEXTURE_SIZE - texture_height // 2, SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column,(SCALE,HEIGHT))
                wall_pos = (ray * SCALE,0)
            self.objects_to_render.append((depth,wall_column,wall_pos))
            
    def ray_cast(self):
        self.ray_casting_result = []
        px, py = self.app.player.pos
        mx, my = self.app.player.map_pos
        ray_angle = self.app.player.angle - H_FOV + 0.0001 #The small number is here to prevent further ZeroDivision Errors!
        
        texture_vert, texture_hor = 1, 1
        
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
                    texture_hor = self.app.map.world_map[tile_hor]
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
                    texture_vert = self.app.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
            
            # depth, texture offset
            
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor
            
            # debug drawing
            
            #pg.draw.line(self.app.window.surface,'yellow',(100*px,100*py),(100*px+100*depth*cos_a,100*py+100*depth*sin_a),2)
            
            # remove fishbowl effect
            depth *= math.cos(self.app.player.angle - ray_angle)
            
            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)
            
            """# draw walls
            
            color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            
            pg.draw.rect(self.app.window.surface,color,
                         (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))"""
            
            #ray casting result
            
            #distance color change


            self.ray_casting_result.append((depth,proj_height,texture,offset))
            
            ray_angle += DELTA_ANGLE
    def update(self):
        self.ray_cast()
        self.get_objects_to_render()