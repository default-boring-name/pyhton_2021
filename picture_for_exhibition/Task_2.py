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

    big_branch = pg.Surface((400, 200))
    big_branch.set_colorkey(colors['None'])
    big_branch.fill(colors['None'])
                
    big_branch_stem = pg.Surface((350, 50))
    big_branch_stem.set_colorkey(colors['None'])
    big_branch_stem.fill(colors['None'])
                                    
    pg.draw.ellipse(big_branch_stem, colors['green'], pg.Rect((-50, 0), (450, 200)), 5)
    big_branch_stem = pg.transform.rotate(big_branch_stem, 25)
    
    big_branch.blit(big_branch_stem, (0, 0))
                                                                
    branch_leaf = pg.Surface((90, 15))
    branch_leaf.set_colorkey(colors['None'])
    branch_leaf.fill(colors['None'])
    
    pg.draw.ellipse(branch_leaf, colors['green'], branch_leaf.get_rect())
    branch_leaf = pg.transform.rotate(branch_leaf, -70)
    
    big_branch.blit(branch_leaf, (135, 90))
    big_branch.blit(branch_leaf, (190, 80))
    big_branch.blit(branch_leaf, (225, 65))
    big_branch.blit(branch_leaf, (250, 40))
    big_branch.blit(branch_leaf, (280, 40))

    big_branch = pg.transform.scale(big_branch, (big_branch.get_width(), int(big_branch.get_height() * 0.8)))

    small_branch = pg.Surface((200, 175))
    small_branch.set_colorkey(colors['None'])
    small_branch.fill(colors['None'])
                
    small_branch_stem = pg.Surface((150, 100))
    small_branch_stem.set_colorkey(colors['None'])
    small_branch_stem.fill(colors['None'])
                                    
    pg.draw.ellipse(small_branch_stem, colors['green'], pg.Rect((-150, 0), (300, 250)), 5)
    small_branch_stem = pg.transform.rotate(small_branch_stem, 60)
                                                    
    small_branch.blit(small_branch_stem, (0, 0))
    small_branch.blit(branch_leaf, (75, 55))
    small_branch.blit(branch_leaf, (110, 55))
    small_branch.blit(branch_leaf, (140, 55))

    left_big_branch = pg.transform.flip(big_branch, True, False)
    left_big_branch = pg.transform.scale(left_big_branch, (460, 200))

    left_small_branch = pg.transform.flip(small_branch, True, False)
    left_small_branch = pg.transform.scale(left_small_branch, (230, 175))

    body.blit(stem, (375, 0))
    body.blit(big_branch, (425, -20))
    body.blit(left_big_branch, (-70, -10))
    body.blit(small_branch, (425, 150))
    body.blit(left_small_branch, (137, 180))

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
