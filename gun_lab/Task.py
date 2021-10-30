import subprocess as subprcs
import random
import enum
import math
import yaml
import time
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMT"] = "1"
import pygame as pg

pg.init()
FPS = 30
WIN_SIZE = {"w": 800, "h": 600}


class COLORS:
    TRANSPARENT = (255, 255, 255, 0),
    BLACK = (0, 0, 0),
    WHITE = (255, 255, 255),
    GREY = (200, 200, 200),
    RED = (255, 0, 0),
    GREEN = (0, 255, 0),
    BLUE = (0, 0, 255),
    YELLOW = (255, 255, 0),
    CYAN = (0, 255, 255),
    MAGENTA = (255, 0, 255)


class DIRECTION(enum.Flag):
    NONE = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


class Name:
    '''
    Класс, позволяющий давать объектам
    уникальные имена
    '''
    Next = 0

    def __init__(self, owner):
        '''
        Функция, инициализирущая объект имени
        :param owner: ссылка на объект, которому будет
                      принадлежать имя
        '''
        self.id_number = Name.Next
        Name.Next += 1
        self.type_ = str(type(owner))[17:-2]

    def log_name(self):
        '''
        Функция, вовращающая имя объекта в формате
        "<Class name>:<id>"
        '''
        return self.type_ + ":" + str(self.id_number)


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

        self.pos = dict(pos)

        self.raw_size = dict(size)
        self.raw_ref_pos = dict(ref_pos)

        self.scaled_size = dict(size)
        self.scaled_ref_pos = dict(ref_pos)

        self.size = dict(size)
        self.ref_pos = dict(ref_pos)

        self.sprite = pg.Surface((self.size["w"], self.size["h"]),
                                 pg.SRCALPHA)
        self.rect = pg.Rect((self.pos["x"] - self.ref_pos["x"],
                             self.pos["y"] - self.ref_pos["y"]),
                            (self.size["w"], self.size["h"]))
        self.angle = 0
        self.manager = None
        self.screen = None
        self.name = Name(self)

    def idle(self):
        '''
        Фунция описывающая дефолтное поведение объекта
        '''

        pass

    def call(self, event):
        '''
        Функция, принимающая события от обработчика событий
        и возвращающая его лог в формате словаря
        (или None, если событие не было обработано)
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
        self.rect = pg.Rect((self.pos["x"] - self.ref_pos["x"],
                             self.pos["y"] - self.ref_pos["y"]),
                            (self.size["w"], self.size["h"]))

    def resize(self, size, adjust_ref={"x": True, "y": True}):
        '''
        Функция, изменяющая размеры игрового объекта.
        :param size: словарь {w, h} с новыми размерами игрового
                     объекта (спрайт объекта будет отмаштабирован)
        :adjust_ref: словарь {x, y} с флагами, показывающими надо ли
                     отмаштабировать положение опорной точки относительно
                     спрайта, по умолчанияю имеет значение {True, True}.
                     !Если опорная точка окажется за пределами спрайта,
                     то маштабирование будет произведено автоматически!
        '''
        if self.raw_ref_pos["x"] > size["w"] or adjust_ref["x"]:
            self.ref_pos["x"] = (self.raw_ref_pos["x"]
                                 * size["w"] / self.raw_size["w"])
            self.scaled_ref_pos["x"] = self.ref_pos["x"]

        if self.raw_ref_pos["y"] > size["h"] or adjust_ref["y"]:
            self.ref_pos["y"] = (self.raw_ref_pos["y"]
                                 * size["h"] / self.raw_size["h"])
            self.scaled_ref_pos["y"] = self.ref_pos["y"]

        self.size = dict(size)
        self.scaled_size = dict(size)

        self.rect = pg.Rect((self.pos["x"] - self.ref_pos["x"],
                             self.pos["y"] - self.ref_pos["y"]),
                            (self.size["w"], self.size["h"]))

    def rotate(self, angle):
        '''
        Функция, поворачивающая игровой объект на некоторый угол
        :param angle: угол в градусах, на который нужно повернуть объект
                      против часовой стрелки.
        '''
        self.angle += angle

        rad_angle = self.angle / 180 * math.pi
        sin = abs(math.sin(rad_angle))
        cos = abs(math.cos(rad_angle))

        if 0 < self.angle and self.angle <= 90:
            self.ref_pos = {
                            "x": (self.scaled_ref_pos["x"] * cos
                                  + self.scaled_ref_pos["y"] * sin),

                            "y": (self.scaled_size["w"] * sin
                                  + self.scaled_ref_pos["x"] * (-sin)
                                  + self.scaled_ref_pos["y"] * cos)
                           }

        elif 90 < self.angle and self.angle <= 180:
            self.ref_pos = {
                            "x": (self.scaled_size["w"] * cos
                                  + self.scaled_ref_pos["x"] * (-cos)
                                  + self.scaled_ref_pos["y"] * sin),

                            "y": (self.scaled_size["w"] * sin
                                  + self.scaled_size["h"] * cos
                                  + self.scaled_ref_pos["x"] * (-sin)
                                  + self.scaled_ref_pos["y"] * (-cos))
                           }

        elif -90 < self.angle and self.angle <= 0:
            self.ref_pos = {
                            "x": (self.scaled_size["h"] * sin
                                  + self.scaled_ref_pos["x"] * cos
                                  + self.scaled_ref_pos["y"] * (-sin)),

                            "y": (self.scaled_ref_pos["x"] * sin
                                  + self.scaled_ref_pos["y"] * cos)
                           }

        else:
            self.ref_pos = {
                            "x": (self.scaled_size["w"] * cos
                                  + self.scaled_size["h"] * sin
                                  + self.scaled_ref_pos["x"] * (-cos)
                                  + self.scaled_ref_pos["y"] * (-sin)),

                            "y": (self.scaled_size["h"] * cos
                                  + self.scaled_ref_pos["x"] * sin
                                  + self.scaled_ref_pos["y"] * (-cos))
                           }

        self.size = {"w": (self.scaled_size["w"] * cos
                           + self.scaled_size["h"] * abs(sin)),
                     "h": (self.scaled_size["h"] * cos
                           + self.scaled_size["w"] * abs(sin))}

        self.rect = pg.Rect((self.pos["x"] - self.ref_pos["x"],
                             self.pos["y"] - self.ref_pos["y"]),
                            (self.size["w"], self.size["h"]))

    def draw(self):
        '''
        Функция рисующая объект на предустановленном экране
        '''
        self.rotate(0)
        blit_size = {"w": int(self.scaled_size["w"]),
                     "h": int(self.scaled_size["h"])}

        blit_sprite = pg.transform.scale(self.sprite, (blit_size["w"],
                                                       blit_size["h"]))
        blit_sprite = pg.transform.rotate(blit_sprite, self.angle)

        blit_rect = pg.Rect((int(self.rect.x), int(self.rect.y)),
                            (int(self.rect.w), int(self.rect.h)))

        self.screen.get_surface().blit(blit_sprite, blit_rect)

    def collide_point(self, pos):
        '''
        Функция, проверяющая пересекается ли объект с данной
        точкой пространства
        :param pos: словарь {x, y} с координатами точки, для
                    которой нужно проверить пересечение
                    с объектом
        '''

        result = self.rect.collidepoint((pos["x"], pos["y"]))
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

    def __str__(self):
        '''
        Функция, привязывающая __str__ к имени объекта
        '''

        return self.name.log_name()


class Text(OnScreenObj):
    '''
    Класс для отображения текста на экране
    '''

    class JUSTIFICATION(enum.Enum):
        LEFT = enum.auto()
        RIGHT = enum.auto()
        CENTRE = enum.auto()

    def __init__(self, pos, size, font="Times New Roman",
                 justification=JUSTIFICATION.LEFT,
                 color=COLORS.BLACK, bg_color=COLORS.TRANSPARENT):
        '''
        Функция инициализирующая объект текста
        :param pos: словарь {x, y}, с позицией текста
                    (позиция центра левой грани, если текста выравнен
                     по левой стороне;
                     позиция центра правой грани, если текста выравнен
                     по правой стороне;
                     позиция центра текста, если текст центрирован)
        :param size: размер текста (шрифта)
        :param justification: выравнивание из Text.JUSTIFICATION,
                              выравнивание текста, по умолчанию
                              текст выравнен слева
        :param font: шрифт текста, по умолчанию шрифт "Times New Roman"
        :param color: цвет из COLORS, цвет текста, по умолчанию
                      цвет текста черный
        :param bg_color: цвет из COLORS, цвет заднего фона текста
                         по умолчанию цвет заднего фона прозрачный
        '''
        self.font_size = size
        self.justification = justification
        self.font_color = color
        self.bg_color = bg_color
        self.font_name = font

        self.text = ""
        self.font_obj = pg.font.SysFont(self.font_name, self.font_size)

        ref_pos = {"x": 0, "y": self.font_size // 2}
        super().__init__(pos,
                         {"w": 0, "h": self.font_size},
                         ref_pos)

    def write(self, text):
        '''
        Функция, отображающая преданный текст на экране
        :param text: текст, который необходимо отобразить
        '''

        self.text = text
        self.sprite = self.font_obj.render(self.text, True,
                                           self.font_color, self.bg_color)

        self.size["w"] = self.sprite.get_rect().width

        if self.justification == Text.JUSTIFICATION.RIGHT:
            self.ref_pos["x"] = self.size["w"]

        elif self.justification == Text.JUSTIFICATION.CENTRE:
            self.ref_pos["x"] = self.size["w"] // 2

        self.rect = pg.Rect((self.pos["x"] - self.ref_pos["x"],
                             self.pos["y"] - self.ref_pos["y"]),
                            (self.size["w"], self.size["h"]))


class ScoreLine(Text):
    '''
    Класс счетчика очков
    '''

    # События счетчика очков

    INCREASE = pg.event.custom_type()
    '''
    Событие данного типа должно иметь
    атрибут increment, указывающий кол-во очков,
    которое нужно добавить
    '''

    SAVE = pg.event.custom_type()
    '''
    Событие данного типа не дожно иметь какие-либо
    атрибуты
    '''

    def __init__(self, pos, size, digit_number=3):
        '''
        Функция, инициализирующая объект счетчика очков
        :param pos: словарь вида {x, y}, указывающий позицию
                    центра счетчика очков
        :param size: размер шрифта счетчика очков
        :param digit_number: кол-во делений счетчика очков
        '''

        self.digit_number = digit_number
        self.scores = 0
        super().__init__(pos, size,
                         justification=Text.JUSTIFICATION.CENTRE)
        self.write(self.scores_to_text())

    def call(self, event):
        '''
        Функция, описывающая реакцию счетчика очков на полученное событие
        и возвращающая его лог в формате словаря (или None, если событие
        не было обработано)
        :param event: полученное событие, на которое счетчик
                      должен прореагировать
        '''

        log_msg = None

        if event.type == ScoreLine.INCREASE:
            log_msg = {
                       "name": str(self),
                       "status": "Increased score by number",
                       "number": event.increment
                      }

            self.scores += event.increment
            if self.scores > 10 ** self.digit_number:
                self.scores -= 10 ** self.digit_number
            self.write(self.scores_to_text())

        elif event.type == ScoreLine.SAVE:
            log_msg = {
                       "name": str(self),
                       "status": "Updated highscore.yml file"
                      }
            self.save_scores()

        return log_msg

    def scores_to_text(self):
        '''
        Функция, переводящая очки в строку вида Scores: XXXX,
        где XXXX - кол-во очков с учетом лидирующих нулей
        '''

        zero_number = (self.digit_number - 1
                       - int(math.log(self.scores + 1) / math.log(10)))

        score_str = ("Scores: " + "0" * zero_number
                     + str(self.scores))

        return score_str

    def save_scores(self):
        '''
        Функция, сохраняющая счет в таблицу рекордов
        '''

        user_name_raw = subprcs.run(["whoami"], stdout=subprcs.PIPE)
        user_name = user_name_raw.stdout.decode("utf-8")[:-1]

        host_name_raw = subprcs.run(["hostname"], stdout=subprcs.PIPE)
        host_name = host_name_raw.stdout.decode("utf-8")[:-1]

        player_name = "@".join([user_name, host_name])
        record_time = time.strftime("%H:%M %d.%m.%Y")

        player = {
                  "name": player_name,
                  "date": record_time,
                  "scores": self.scores
                 }
        highscores = None

        if os.path.isfile("highscore.yml"):
            with open("highscore.yml", "r") as score_file:
                highscores = yaml.safe_load(score_file)

        if highscores is None:
            highscores = []
        highscores.append(player)

        sort_key = lambda x: x["scores"]
        highscores.sort(key=sort_key)

        with open("highscore.yml", "w") as score_file:
            yaml.dump(highscores, score_file, sort_keys=False)


class EventManager:
    '''
    Класс менеджра событий, который обрабатывает как
    pygame события, так и пользовательские события
    '''

    # События менеджера событий

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
        self.name = Name(self)
        self.end = False
        self.log_hist = []

        if os.path.isfile("log.yml"):
            with open("log.yml", "r") as log_file:
                self.log_hist = yaml.safe_load(log_file)

        if self.log_hist is None:
            self.log_hist = []

    def add_obj(self, obj):
        '''
        Функция, которая добавляет переданный объект в
        список отслеживаемых объектов, если его там уже не было
        :param obj: обЪект, который нужно добавить в
                    список(объект должен иметь метод
                    idle(), описывающий дефолтное поведение
                    объекта, метод call(), принимающий
                    объект события и возвращающий его лог в формате
                    словаря (или None, если событие не было
                    обработано), и метод set_manger() принимающий
                    объект типа EventManager
        '''
        if obj not in self.pool:
            self.pool.append(obj)
            obj.set_manager(self)
            return True
        return False

    def remove_obj(self, obj):
        '''
        Функция, исключающая переданный объект из списка
        отслеживаемых объектов (если он там был)
        :param obj: объект, который будет исключен из
                    списка отслеживаемых объектов
        '''
        if obj in self.pool:
            self.pool.remove(obj)
            return True
        return False

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
            log_msg = None

            if event.type == pg.QUIT:
                log_msg = {
                           "name": str(self),
                           "status": "Preparing to exit"
                          }
                running = False
            elif event.type == EventManager.REMOVEOBJ:
                if self.remove_obj(event.target):
                    log_msg = {
                               "name": str(self),
                               "status": "Removed object from list",
                               "object": str(event.target)
                              }
            elif event.type == EventManager.ADDOBJ:
                if self.add_obj(event.target):
                    log_msg = {
                               "name": str(self),
                               "status": "Added object to list",
                               "object": str(event.target)
                              }
            else:
                for obj in self.pool:
                    self.log(obj.call(event))

            self.log(log_msg)

        for obj in self.pool:
            obj.idle()

        if self.end:
            log_msg = {
                       "name": str(self),
                       "status": "Exiting"
                      }
            self.log(log_msg)
            self.save_log()
            return False

        if not running:
            self.end = True
            save_score_event = pg.event.Event(ScoreLine.SAVE)
            pg.event.post(save_score_event)
            return True

        return running

    def log(self, log_msg):
        if log_msg is not None:
            log_time = time.strftime("%H:%M:%S %d.%m.%Y")
            log_msg.update({"time": log_time})
            self.log_hist.append(log_msg)

    def save_log(self):
        '''
        Функция, сохраняющая логи
        '''

        with open("log.yml", "w") as log_file:
            yaml.dump(self.log_hist, log_file, sort_keys=False)

    def __str__(self):
        '''
        Функция, привязывающая __str__ к имени объекта
        '''

        return self.name.log_name()


class Screen:
    '''
    Класс экрана, на котором будет отрисовываться
    некоторая сцена
    '''

    def __init__(self, size, bg_color=COLORS.TRANSPARENT):
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

    def get_absolute_pos(self):
        '''
        Функция, возвращающая абсолютное положение объекта
        '''

        screen_pos = {"x": 0, "y": 0}
        if self.screen is not None:
            screen_pos = screen.get_absolute_pos()
        pos = {
               "x": self.pos["x"] + screen_pos["x"],
               "y": self.pos["y"] + screen_pos["y"]
              }

        return pos


class MainScreen(Screen):
    '''
    Класс главного экрана приложения
    '''

    def __init__(self, size, bg_color=COLORS.WHITE):
        '''
        Функция для инициализации главного экрана приложения
        :param size: словарь вида {"w", "h"}, размеры экрана
        :param bg_color: цвет из COLORS, цвет заднего фона экрана
                         (заливка), по умолчания он белый
        '''

        super().__init__(size, bg_color)
        self.surf = pg.display.set_mode((self.size["w"],
                                         self.size["h"]))

    def update(self):
        '''
        Функция, которая перерисовывате экран
        (делает заливку bg_color и поочереди отрисовывает
        все обЪекты, содержащиеся в списке для отрисовки)
        '''

        super().update()

        pg.display.update()

    def get_absolute_pos(self):
        '''
        Функция, возвращающая абсолютное положение экрана
        '''

        return {"x": 0, "y": 0}


class SubScreen(Screen):
    '''
    Класс подэкрана для отображения на главном экране сразу
    нескольких сцен
    '''

    def __init__(self, pos, size, bg_color=COLORS.TRANSPARENT):
        '''
        Функция для инициализации подэкрана приложения
        :param pos: словарь {x, y} с позицией левого верхнего
                    угла подэкрана
        :param size: словарь вида {"w", "h"}, размеры подэкрана
        :param bg_color: цвет из COLORS, цвет заднего фона подэкрана
                         (заливка), по умолчания он прозрачный
        '''
        self.pos = dict(pos)
        super().__init__(size, bg_color)
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

    def get_absolute_pos(self):
        '''
        Функция, возвращающая абсолютное положение подэкрана
        '''
        screen_pos = {"x": 0, "y": 0}
        if self.screen is not None:
            screen_pos = screen.get_absolute_pos()
        pos = {
               "x": self.pos["x"] + screen_pos["x"],
               "y": self.pos["y"] + screen_pos["y"]
              }
        return pos


class ShootingRange(SubScreen):
    '''
    Класс активной области, в которой происходит игра
    '''

    class GameObj(OnScreenObj):
        '''
        Класс игрового объекта (объект,
        находящийся в активной игровой области)
        '''

        # Событие игрового объекта
        WALLCOLLISION = pg.event.custom_type()
        '''
        События данного типа должны иметь
        атрибут target, указывающий на объект столкнувшийся
        со стеной, и атрибут направления dir, являющийся
        флагом DIRECTION
        '''

    class Gun(GameObj):
        '''
        Класс пушки
        '''

        def __init__(self, pos):
            '''
            Функция, инициализирующая пушку
            :param pos: словарь {x, y} с позицией основания ствола пушки
            '''
            self.aiming = False
            self.power = 10
            size = {"w": 40, "h": 10}
            ref_pos = {"x": 5, "y": 5}

            super().__init__(pos, size, ref_pos)
            pg.draw.rect(self.sprite, COLORS.BLACK, self.sprite.get_rect())

        def call(self, event):
            '''
            Функция, описывающая реакцию пушки на полученное событие
            и возвращающая его лог в формате словаря (или None, если событие
            не было обработано)
            :param event: полученное событие, на которое пушка
                          должна прореагировать
            '''
            log_msg = None

            if event.type == pg.MOUSEMOTION:
                screen_abs_pos = self.screen.get_absolute_pos()
                rel_mouse_pos = {
                                 "x": event.pos[0] - screen_abs_pos["x"],
                                 "y": event.pos[1] - screen_abs_pos["y"]
                                }

                dist = (abs(self.pos["y"] - rel_mouse_pos["y"])
                        + abs(rel_mouse_pos["x"] - self.pos["x"]))
                abs_angle = math.atan2(self.pos["y"] - rel_mouse_pos["y"],
                                       rel_mouse_pos["x"] - self.pos["x"])

                rel_angle = (abs_angle) * 180 / math.pi - self.angle

                if abs(rel_angle * dist) >= 800:
                    self.rotate(rel_angle)

                    log_msg = {
                               "name": str(self),
                               "status": f"Rotated by {rel_angle}"
                              }

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.aiming:
                        self.aiming = True
                        pg.draw.rect(self.sprite, COLORS.YELLOW,
                                     self.sprite.get_rect())

                        log_msg = {
                                   "name": str(self),
                                   "status": "Started to aim"
                                  }

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.aiming:
                        self.aiming = False
                        self.power = 10
                        pg.draw.rect(self.sprite, COLORS.BLACK,
                                     self.sprite.get_rect())
                        self.resize(self.raw_size)

                        log_msg = {
                                   "name": str(self),
                                   "status": "Fired"
                                  }

            return log_msg

        def idle(self):
            '''
            Функция, описывающая дефолтное поведения пушки
            '''
            if self.aiming and self.power <= 100:
                self.power += 0.5
                new_size = {"w": self.raw_size["w"] + self.power - 10,
                            "h": self.raw_size["h"]}
                adjust = {"x": False, "y": True}
                self.resize(new_size, adjust)

    def __init__(self, pos, size):
        '''
        Функция инициализирующая активную игровую область
        :param pos: словарь {x, y} с позицией левого верхнего
                    угла стрельбища
        :param size: словарь вида {"w", "h"}, размеры стрельбища
        '''
        self.manager = None
        self.name = Name(self)
        self.pool = []
        super().__init__(pos, size, COLORS.GREY)

        gun = ShootingRange.Gun({"x": 50, "y": self.size["h"] - 50})
        self.pool.append(gun)
        self.add_obj(gun)

    def idle(self):
        '''
        Фунция описывающая дефолтное поведение активной области
        (проверка того, что все игровые оъекты находятся в пределах
         области)
        '''

        for obj in self.pool:
            coll_flag = DIRECTION.NONE

            if obj.collide_x(0):
                coll_flag |= DIRECTION.LEFT

            if obj.collide_x(self.size["w"]):
                coll_flag |= DIRECTION.RIGHT

            if obj.collide_y(0):
                coll_flag |= DIRECTION.UP

            if obj.collide_y(self.size["h"]):
                coll_flag |= DIRECTION.DOWN

            if coll_flag & ~DIRECTION.NONE:
                event_type = ShootingRange.GameObj.WALLCOLLISION
                coll_event = pg.event.Event(event_type,
                                            {"taget": obj,
                                             "dir": coll_flag})
                pg.event.post(coll_event)

    def call(self, event):
        '''
        Функция, принимающая события от обработчика событий и
        возвращающая его лог в формате словаря (или None,
        если событие не было обработано)
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
        self.manager = event_manager

        for obj in self.pool:
            add_event = pg.event.Event(EventManager.ADDOBJ,
                                       {"target": obj})
            pg.event.post(add_event)

    def __str__(self):
        '''
        Функция, привязывающая __str__ к имени объекта
        '''
        return self.name.log_name()


screen = MainScreen(WIN_SIZE)
manager = EventManager()
clock = pg.time.Clock()

sh_range = ShootingRange({"x": 50, "y": 75},
                         {"w": 700, "h": 500})
screen.add_obj(sh_range)
manager.add_obj(sh_range)

while manager.run():
    screen.update()
    clock.tick(FPS)

pg.quit()
