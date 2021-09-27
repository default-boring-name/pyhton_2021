import pygame as pg
import pygame.draw as pg_draw
import math

class Circle:
    
    def __init__(self, parent_scr, coor, rad, color):
        self.parent_scr = parent_scr
        self.coor = list(coor)
        self.rad = rad
        self.color = color

        pg_draw.circle(self.parent_scr, self.color,
                       self.coor, self.rad) 


class Polygon:
    
    def __init__(self, parent_scr, points, color):
        self.parent_scr = parent_scr
        self.points = list(points)
        self.color = color
        pg_draw.polygon(self.parent_scr, self.color,
                       self.points) 


def rotate_rect(coor, size, alpha):
    p = [(0, 0), (0, 0), (0, 0), (0, 0)]

    sin_alpha = math.sin(alpha / 180.0 * math.pi)
    cos_alpha = math.cos(alpha / 180.0 * math.pi)

    for i in range(4):
        p[i] = (math.copysign(size[0] / 2, math.cos(math.pi / 4 + math.pi * i / 2)),
                math.copysign(size[1] / 2, math.sin(math.pi / 4 + math.pi * i / 2)))
        
        p[i] = (p[i][0] * cos_alpha + p[i][1] * sin_alpha, -p[i][0] * sin_alpha + p[i][1] * cos_alpha)
        p[i] = (p[i][0] + coor[0], p[i][1] + coor[1])

    return p
    

pg.init()

FPS = 30
window_size = (400, 400)
screen = pg.display.set_mode(window_size)

colors = {
          'black': (0, 0, 0),
          'red': (255, 0, 0),
          'yellow': (255, 255, 0),
          'grey': (100, 100, 100)
          }

screen.fill(colors['grey'])

face = Circle(screen, (window_size[0] / 2, window_size[1] / 2),
              100, colors['yellow'])

left_eye = Circle(screen, (face.coor[0] - 50, face.coor[1] - 30),
              25, colors['red'])
left_pupil = Circle(screen, (face.coor[0] - 50, face.coor[1] - 30),
              10, colors['black'])

right_eye = Circle(screen, (face.coor[0] + 50, face.coor[1] - 30),
              20, colors['red'])
right_pupil = Circle(screen, (face.coor[0] + 50, face.coor[1] - 30),
              10, colors['black'])

left_eyebrow = Polygon(screen,
                        rotate_rect((left_eye.coor[0] - 5, left_eye.coor[1] - 35), (100, 10), -40),
                        colors['black'])
right_eyebrow = Polygon(screen,
                        rotate_rect((right_eye.coor[0] + 5, right_eye.coor[1] - 25), (80, 10), 20),
                        colors['black'])
mouth = Polygon(screen, rotate_rect((face.coor[0], face.coor[1] + 50), (90, 20), 0), colors['black'])

pg.display.update()
clock = pg.time.Clock()
running = True

while running:
    clock.tick()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()

