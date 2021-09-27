import pygame as pg
import pygame.draw as pg_draw
import math

pg.init()

FPS = 30
window_size = (400, 400)
screen = pg.display.set_mode(window_size)

colors = {
         'black': (0, 0, 0),
         'orange': (200, 100, 0),
         'white': (255, 255, 255),
         'green': (0, 255, 0)
         }

screen.fill(colors['orange'])
 
s = pg.Surface(100, 100)
pg_draw.circle(s, colors['green'], (50, 50), 10)


pg.display.update()
clock = pg.time.Clock()
running = True

while running:
    clock.tick()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()

