import pygame as pg
import random

FPS = 30
WIN_SIZE = {"w": 400, "h": 400}
COLORS = {
          "BLACK": (0, 0, 0),
          "WHITE": (255, 255, 255),
          "RED": (255, 0, 0),
          "GREEN": (0, 255, 0),
          "BLUE": (0, 0, 255),
          "YELLOW": (255, 255, 0),
          "CYAN": (0, 255, 255),
          "MAGENTA": (255, 0, 255)
         }

pg.init()

screen = pg.display.set_mode((WIN_SIZE["w"], WIN_SIZE["h"]))


running = True
clock = pg.time.Clock()

while running:
    clock.tick(FPS)
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
