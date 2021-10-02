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

def draw_bamboo(size):
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

    return pg.transform.scale(body, size)

def draw_panda(size):
    body = pg.Surface((400, 450))
    body.set_colorkey(colors['None'])
    body.fill(colors['None'])

    pg.draw.ellipse(body, colors['white'], pg.Rect((20, 100), (300, 165)))

    head = pg.Surface((220, 210))
    head.set_colorkey(colors['None'])
    head.fill(colors['None'])
                                    
    pg.draw.rect(head, colors['white'], pg.Rect((30, 85), (175, 60)))
    pg.draw.ellipse(head, colors['white'], pg.Rect((30, 10), (175, 150)))

    chin = pg.Surface((120, 194))
    chin.set_colorkey(colors['None'])
    chin.fill(colors['None'])
    pg.draw.ellipse(chin, colors['white'], pg.Rect((0, 0), (300, 194)))
    chin = pg.transform.rotate(chin, 60)
    head.blit(chin, (-20, 47))

    pg.draw.circle(head, colors['black'], (130, 130), 25)
    pg.draw.ellipse(head, colors['black'], pg.Rect((27, 100), (42, 50)))
    pg.draw.ellipse(head, colors['black'], pg.Rect((50, 175), (50, 35)))

    ear = pg.Surface((80, 45))
    ear.set_colorkey(colors['None'])
    ear.fill(colors['None'])

    upper_ear = pg.Surface((80, 40))
    upper_ear.set_colorkey(colors['None'])
    upper_ear.fill(colors['None'])
    pg.draw.ellipse(upper_ear, colors['black'], pg.Rect((0, 0), (80, 50)))
    ear.blit(upper_ear, (0,0))

    down_ear = pg.Surface((80, 10))
    down_ear.set_colorkey(colors['None'])
    down_ear.fill(colors['None'])
    pg.draw.ellipse(down_ear, colors['black'], pg.Rect((0, -10), (80, 20)))
    ear.blit(down_ear, (0, 25))
    
    head.blit(pg.transform.rotate(ear, 50), (3, -10))
    head.blit(pg.transform.flip(pg.transform.rotate(ear, 45), True, False), (140, -5))

    back_leg = pg.Surface((190, 100))
    back_leg.set_colorkey(colors['None'])
    back_leg.fill(colors['None'])
    pg.draw.circle(back_leg, colors['black'], (150, 45), 45)
    pg.draw.polygon(back_leg, colors['black'], [(0, 20), (0, 30), (30, 65), (100, 90),(150, 90), (160, 0), (0, 20)])

    back_back_leg = pg.Surface((190, 25))
    back_back_leg.set_colorkey(colors['None'])
    back_back_leg.fill(colors['None'])
    pg.draw.ellipse(back_back_leg, colors['black'],
    pg.Rect((-90, 0), (420, 240)))
    back_leg.blit(back_back_leg, (-20, 0))

    front_left_leg = pg.Surface((154, 300))
    front_left_leg.set_colorkey(colors['None'])
    front_left_leg.fill(colors['None'])
    pg.draw.polygon(front_left_leg, colors['black'],[(154, 0), (100, 0), (100, 100), (60, 220), (154, 200)])

    front_left_feet = pg.Surface((100, 140))
    front_left_feet.set_colorkey(colors['None'])
    front_left_feet.fill(colors['None'])
    pg.draw.ellipse(front_left_feet, colors['black'], front_left_feet.get_rect())
    front_left_leg.blit(pg.transform.rotate(front_left_feet, -50), (20, 120))
    
    front_right_leg = pg.Surface((130, 170))
    front_right_leg.set_colorkey(colors['None'])
    front_right_leg.fill(colors['None'])
    pg.draw.polygon(front_right_leg, colors['black'], [(0, 0), (80, 0), (110, 80), (75, 170), (0, 40)])

    back_front_right_leg = pg.transform.scale(back_back_leg, (170, 60))
    front_right_leg.blit(pg.transform.rotate(back_front_right_leg, 110), (-40, 10))
    body.blit(pg.transform.rotate(back_leg, -110), (170, 160))
    body.blit(front_left_leg, (40, 100))
    body.blit(pg.transform.rotate(front_right_leg, -10), (-10, 150))
    body.blit(head, (-15, 30))

    return pg.transform.scale(body, size)

pg.init()

window_size = (1200, 800)
screen = pg.display.set_mode(window_size)

main_surf = pg.display.get_surface()
main_surf.fill(colors['peach'])

main_surf.blit(draw_bamboo((225, 350)), (280, 230))
main_surf.blit(draw_bamboo((500, 500)), (300, 50))
main_surf.blit(draw_bamboo((275, 450)), (800, 75))
main_surf.blit(draw_bamboo((230, 285)), (40, 275))

main_surf.blit(draw_panda((400, 450)), (600, 350))
main_surf.blit(draw_panda((150, 120)), (475, 600))

pg.display.update()
clock = pg.time.Clock()
running = True

while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
