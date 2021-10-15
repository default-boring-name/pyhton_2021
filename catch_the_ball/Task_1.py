import pygame as pg
import random
import enum

FPS = 30
WIN_SIZE = {"w": 400, "h": 400}
COLORS = {
          "TRANSPARENT": (255, 255, 255, 0),
          "BLACK": (0, 0, 0),
          "WHITE": (255, 255, 255),
          "RED": (255, 0, 0),
          "GREEN": (0, 255, 0),
          "BLUE": (0, 0, 255),
          "YELLOW": (255, 255, 0),
          "CYAN": (0, 255, 255),
          "MAGENTA": (255, 0, 255)
         }


class OnScreenObj:

    '''
    Класс игровых объектов, которые могут быть
    отрисованы на экране
    '''

    def __init__(self, pos, size, ref_pos):
        '''
        Функци инициализации игрового объекта
        :param pos: словарь {x, y} с позицией игрового объекта
                    (абсолютная позиция опорной точки)
        :param size: словарь {w, h} с размерами игрового
                     объекта (по ним будет создан спрайт)
        :param ref_pos: словарь {x, y} с координатами опорной
                        точки относительно левого вехнего угла
                        спрайта
        '''

        self.screen = screen
        self.pos = dict(pos)
        self.size = dict(size)
        self.ref_pos = ref_pos
        self.sprite = pg.Surface((self.size["w"], self.size["h"]),
                                  pg.SRCALPHA)
        self.rect = pg.Rect((pos["x"] - ref_pos["x"],
                             pos["y"] - ref_pos["y"]),
                             (size["w"], size["h"]))
        self.manager = None
        self.screen = None

    def idle(self):
        '''
        Фунция описывающая дефолтное поведение объекта
        '''

        pass

    def call(self, event):
        '''
        Функция, принимающая события от обработчика событий
        :param event: объект события, которое необходимо
                      обработать
        '''

        return None

    def set_screen(self, screen):
        '''
        Функция, устанавливающая связь с экраном для
        отрисовки
        :param screen: объект Screen, с которым
                              нужно установить связь
        '''

        self.screen = screen

    def set_manager(self, event_manager):
        '''
        Функция, устанавливающая связь с обработчиком
        событий
        :param event_manager: объект EventManager, с которым
                              нужно установить связь
        '''

        self.manager = event_manager

    def move(self, pos):
        '''
        Функция предвигающая объект в указанные координаты
        (необходимо указыать новые координаты опорной точки)
        :param pos: словарь {x, y} с координатами точки, в
                    которую необходимо переместить объект
        '''

        self.pos = dict(pos)
        self.rect = pg.Rect((pos["x"] - ref_pos["x"],
                             pos["y"] - ref_pos["y"]),
                             (size["w"], size["h"]))


    def draw(self):
        '''
        Функция рисующая объект на предустановленном экране
        '''

        self.screen.get_surface().blit(self.sprite, self.rect)

    def collide_point(self, pos):
        '''
        Функция, проверяющая пересекается ли объект с данной
        точкой пространства
        :param pos: словарь {x, y} с координатами точки, для
                    которой нужно проверить пересечение
                    с объектом
        '''

        result =  self.rect.collidepoint((pos["x"], pos["y"]))
        return result

    def collide_obj(self, another):
        '''
        Функция проверяющая сталкиваются ли два объекта
        (если объекты на разных экранах, функция вернет False)
        :param another: объект OnScreeObj, для которого нужно
                        проверить факт столкновения
        '''

        result = (self.rect.colliderect(another.rect)
                  and self.screen is another.screen)
        return result

    def collide_x(self, x):
        '''
        Функция, проверярющая пресекается ли объект с вертикальной
        прямой с абсциссой равной х
        :param x: абсцисса прямой, с которой надо проверить
                  пересечение
        '''

        result = self.rect.left < x and x < self.rect.right
        return result

    def collide_y(self, y):
        '''
        Функция, проверярющая пресекается ли объект с горизонтальной
        прямой с ординатой равной y
        :param y: ордината прямой, с которой надо проверить
                  пересечение
        '''

        result = self.rect.top < y and y < self.rect.bottom
        return result


class EventManager:
    '''
    Класс менеджра событий, который обрабатывает как
    pygame события, так и пользовательские события
    '''

    #События менеджера событий

    REMOVEOBJ = pg.event.custom_type()
    '''
    Событие данного типа должно иметь
    атрибут target, указывающий на объект,
    который нужно удалить
    '''

    ADDOBJ = pg.event.custom_type()
    '''
    Событие данного типа должно иметь
    атрибут target, указывающий на объект,
    который нужно добавить
    '''

    def __init__(self):
        '''
        Функция для инициализация объекта менеджера событий
        '''
        self.pool = []

    def add_obj(self, obj):
        '''
        Функция, которая добавляет переданный объект в
        список отслеживаемых объектов, если его там уже не было
        :param obj: обЪект, который нужно добавить в
                    список(объект должен иметь метод
                    idle(), описывающий дефолтное поведение
                    объекта, метод call(), принимающий
                    объект события, и метод set_manger() принимающий
                    объект типа EventManager

        '''
        if obj not in self.pool:
            self.pool.append(obj)
            obj.set_manager(self)

    def remove_obj(self, obj):
        '''
        Функция, исключающая переданный объект из списка
        отслеживаемых объектов (если он там был)
        :param obj: объект, который будет исключен из
                    списка отслеживаемых объектов
        '''
        if obj in self.pool:
            self.pool.remove(obj)

    def get_pool(self):
        '''
        Функция, возращающая список отслеживаемых объектов
        '''
        return self.pool

    def run(self):
        '''
        Функция, забирающая события из очереди событий pygame,
        обрабатывающая их, пересылающая часть событий в
        объекты из списка отслеживаемых объектов, вызывающая
        дефолтное поведение объектов из списка отслеживаемых
        объектов и возращающая флаг продолжения работы
        '''
        running = True
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            elif event.type == EventManager.REMOVEOBJ:
                self.remove_obj(event.target)

            elif event.type == EventManager.ADDOBJ:
                self.add_obj(event.target)

            else:
                for obj in self.pool:
                    obj.call(event)

        for obj in self.pool:
            obj.idle()

        return running


class Screen:
    '''
    Класс экрана, на котором будет отрисовываться
    некоторая сцена
    '''

    def __init__(self, size, bg_color=COLORS["TRANSPARENT"]):
        '''
        Функция для инициализации экрана
        :param size: словарь вида {"w", "h"}, размеры экрана
        :param bg_color: цвет из COLORS, цвет заднего фона экрана
                         (заливка), по умолчания он прозрачный
        '''

        self.size = dict(size)
        self.bg_color = bg_color
        self.surf = pg.Surface((self.size["w"],
                                self.size["h"]), pg.SRCALPHA)
        self.to_draw_list = []

    def update(self):
        '''
        Функция, которая перерисовывате экран
        (делает заливку bg_color и поочереди отрисовывает
        все обЪекты, содержащиеся в списке для отрисовки)
        '''

        self.surf.fill(self.bg_color)
        for obj in self.to_draw_list:
            obj.draw()

    def add_obj(self, obj):
        '''
        Функция, добавляющая переданный объект в список
        для отрисовки, если его там еще не было
        :param obj: обЪект, который нужно добавить в
                    список для отрисовки (обязательно должен
                    иметь метод draw() для отрисовки и метод
                    set_screen примающий объект Screen)
        '''

        if obj not in self.to_draw_list:
            self.to_draw_list.append(obj)
            obj.set_screen(self)

    def remove_obj(self, obj):
        '''
        Функция, исключающая переданный объект из списка
        для отрисовки (если он там был)
        :param obj: объект, который будет исключен из
                    списка для отрисовки
        '''

        if obj in self.to_draw_list:
            self.to_draw_list.remove(obj)

    def get_surface(self):
        '''
        Функция, возвращающая основную поверхность для рисования
        '''

        return self.surf


class MainScreen(Screen):
    '''
    Класс главного экрана приложения
    '''

    def __init__(self, size, bg_color=COLORS["WHITE"]):
        '''
        Функция для инициализации главного экрана приложения
        :param size: словарь вида {"w", "h"}, размеры экрана
        :param bg_color: цвет из COLORS, цвет заднего фона экрана
                         (заливка), по умолчания он белый
        '''

        Screen.__init__(self, size, bg_color)
        self.surf = pg.display.set_mode((self.size["w"],
                                         self.size["h"]))

    def update(self):
        '''
        Функция, которая перерисовывате экран
        (делает заливку bg_color и поочереди отрисовывает
        все обЪекты, содержащиеся в списке для отрисовки)
        '''

        Screen.update(self)

        pg.display.update()


class SubScreen(Screen):
    '''
    Класс подэкрана для отображения на главном экране сразу
    нескольких сцен
    '''

    def __init__(self, pos, size, bg_color=COLORS["TRANSPARENT"]):
        '''
        Функция для инициализации подэкрана приложения
        :param pos: словарь {x, y} с позицией левого верхнего
                    угла подэкрана
        :param size: словарь вида {"w", "h"}, размеры подэкрана
        :param bg_color: цвет из COLORS, цвет заднего фона подэкрана
                         (заливка), по умолчания он прозрачный
        '''
        self.pos = dict(pos)
        Screen.__init__(self, size, bg_color)
        self.screen = None

    def move(self, pos):
        '''
        Функция предвигающая подэкран в указанные координаты
        :param pos: словарь {x, y} с координатами точки, в
                    которую необходимо переместить левый верхний
                    угл подэкрана
        '''
        self.pos = dict(pos)

    def set_screen(self, screen):
        '''
        Функция, устанавливающая связь с экраном для
        отрисовки
        :param screen: объект Screen, с которым
                              нужно установить связь
        '''
        self.screen = screen

    def draw(self):
        '''
        Функция рисующая подэкран на предустановленном экране
        '''
        Screen.update(self)
        self.screen.get_surface().blit(self.surf,
                                       (self.pos["x"], self.pos["y"]))


class ShootingRange(SubScreen):
    '''
    Класс стрельбища (загон с движущимися мишенями)
    '''

    #События стрельбища

    ADDTARGET = pg.event.custom_type()
    '''
    Событие данного типа должно иметь
    атрибут target_type из TARGET_TYPES, указывающий на тип мишени,
    которую нужно создать
    '''

    REMOVETARGET = pg.event.custom_type()
    '''
    Событие данного типа должно иметь
    атрибут target, указывающий на мишень,
    которую нужно уничтожить
    '''


    class Target(OnScreenObj):
        '''
        Класс мишени для стрельбища
        '''

        class SHAPES(enum.Enum):
            CIRCLE = enum.auto()
            SQUARE = enum.auto()
            TRIANGLE_UP = enum.auto()
            TRIANGLE_DOWN = enum.auto()
            TRIANGLE_LEFT = enum.auto()
            TRIANGLE_RIGHT = enum.auto()


        def __init__(self, pos, velocity, shape, color, size):
            '''
            Функция инициализирующая мишень
            :param pos: словарь {x, y} с позицией центра мишени
            :param velocity: словарь {x, y} со скоростью центра мишени
            :param shape: форма из Target.SHAPES, форма мишени
            :param color: цвет из COLORS, цвет мишени
            :param size: характерный размер мишени
            '''
            pass

        def idle(self):
            '''
            Функция, описывающая дефолтное движение мишени
            '''
            pass

        def call(self, event):
            '''
            Функция, описывающая реакцию мишени на полученное событие
            :param event: полученное событие, на которое мишень
                          должна прореагировать
            '''
            pass


    TARGET_TYPES = {
                    "m_r_o": {
                              "shape": Target.SHAPES.CIRCLE,
                              "color": COLORS["RED"],
                              "size": 20
                             }
                   }

    def __init__(self, pos, size, pool_size):
        '''
        Функция инициализирующая стрельбище
        :param pos: словарь {x, y} с позицией левого верхнего
                    угла стрельбища
        :param size: словарь вида {"w", "h"}, размеры стрельбища
        :param pool_size: количество мишеней, одновременно находящихся
                          на стрельбище
        '''
        pass

    def idle(self):
        '''
        Фунция описывающая дефолтное поведение стрельбища
        (подсчет существующих мишеней)
        '''
        pass

    def call(self, event):
        '''
        Функция, принимающая события от обработчика событий
        :param event: объект события, которое необходимо
                      обработать
        '''
        pass

    def set_manager(self, event_manager):
        '''
        Функция, устанавливающая связь с обработчиком
        событий
        :param event_manager: объект EventManager, с которым
                              нужно установить связь
        '''
        pass

    def generate_target(self, target_type):
        '''
        Функция, создающая мишени разных типов
        :param target_type: тип мишени, которую нужно создать
        '''
        pass


screen = MainScreen(WIN_SIZE)
manager = EventManager()
clock = pg.time.Clock()

while manager.run():
    screen.update()
    clock.tick(FPS)

pg.quit()
