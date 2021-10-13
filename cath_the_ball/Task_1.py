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

class Screen:
    '''
    Класс экрана, на котором будет отрисовываться
    некоторая сцена
    '''

    def __init__(self, size, bg_color=COLORS["WHITE"]):
        '''
        Функция для инициализации окна приложения
        :param size: словарь вида {"w", "h"}, размеры окна
        :param bg_color: цвет из COLORS, цвет заднего фона экрана
                         (заливка), по умолчания он белый
        '''

        self.size = dict(size)
        self.bg_color = bg_color
        self.surf = pg.display.set_mode((self.size["w"],
                                         self.size["h"]))
        self.to_draw_list = []

    def update(self):
        '''
        Функция, которая перерисовывате экран
        (делает заливку bg_color и поочереди отрисовывает
        все обЪекты, содержащиеся в списке для отрисовки)
        '''

        self.surf.fill(self.bg_color)
        for obj in self.to_draw_list:
            obj.draw(self.surf, self.size)

        pg.display.update()
    
    def add_obj(self, obj):
        '''
        Функция, добавляющая переданный объект в список 
        для отрисовки
        :param obj: обЪект, который нужно добавить в
                    список для отрисовки (обязательно должен
                    иметь метод draw(), принимающий холст
                    для отрисовки и его размер)
        '''

        if obj not in self.to_draw_list:
            self.to_draw_list.append(obj)

    def remove_obj(self, obj):
        '''
        Функция, исключающая переданный объект из списка
        для отрисовки (если он там был)
        :param obj: объект, который будет исключен из
                    списка для отрисовки
        '''

        if obj in self.to_draw_list:
            self.to_draw_list.remove(obj)


pg.init()

screen = Screen(WIN_SIZE)
running = True
clock = pg.time.Clock()
while running:
    screen.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    clock.tick(FPS)

pg.quit()
