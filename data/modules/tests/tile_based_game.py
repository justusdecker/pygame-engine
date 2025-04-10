from pygame.mouse import get_pos

class Map:
    def __init__(self, app):
        self.app = app
        self.map = [[(i,i,i) for i,x in enumerate(range(36))] for y in range(64)]

    def update(self):
        D = 20
        for i,y in enumerate(self.map):
            for j,tile in enumerate(y):
                c,v = get_pos()
                if c > i * D and v > j * D and c < (i+1) * D and v < (j+1) * D:
                    color = (self.map[i][j][0] + 10)
                    if color > 255: color = 255
                    self.map[i][j] = (color, color, color)
                self.app.window.surface.fill(tile,(i*D,j*D,(i+1)*D,(j+1)*D))
        pass