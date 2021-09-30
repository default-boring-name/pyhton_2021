import pygame as pg
import math

colors = {
          'black': (0, 0, 0),
          'white': (255, 255, 255),
          'green': (0, 104, 55),
          'peach': (255, 175, 128),
          'None': (255, 230, 255)
         }
FPS = 30

def draw_bamboo():
    body = pg.Surface((780, 480))
    body.set_colorkey(colors['None'])
    body.fill(colors['None'])

    stem = pg.Surface((100, 480))
    stem.set_colorkey(colors['None'])
    stem.fill(colors['None'])

    stem_sect = [pg.Surface((37, 112)),
                 pg.Surface((37, 127)),
                 pg.Surface((25, 78)),
                 pg.Surface((13, 105))]
    
    for i in range(4):
        stem_sect[i].set_colorkey(colors['None'])
        stem_sect[i].fill(colors['None'])
        pg.draw.rect(stem_sect[i], colors['green'],
        pg.Rect((0, 1), stem_sect[i].get_size()))

    stem_sect[2] = pg.transform.rotate(stem_sect[2], -27)
    stem_sect[3] = pg.transform.rotate(stem_sect[3], -27)

    stem.blit(stem_sect[0], (5, 368))
    stem.blit(stem_sect[1], (5, 231))
    stem.blit(stem_sect[2], (0, 133))
    stem.blit(stem_sect[3], (35, 8))

    body.blit(stem, (375, 0))

    return body 

pg.init()

window_size = (1200, 800)
screen = pg.display.set_mode(window_size)

main_surf = pg.display.get_surface()
main_surf.fill(colors['peach'])

main_surf.blit(draw_bamboo(), (280, 230))

pg.display.update()
clock = pg.time.Clock()
running = True

while running:
    clock.tick()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
