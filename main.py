import pygame as pg
from threading import Thread, RLock
from datetime import datetime
from random import choice, randrange
from string import ascii_letters
import win32api as wapi

pg.init()
pg.display.set_caption('Press Esc to Exit, Size is 80x10')

# Настройки дисплея
WIDTH, HEIGHT = 575, 160
SURFACE = pg.display.set_mode((WIDTH, HEIGHT))

# Настройки шрифтов
FONT_SIZE = 16
FONT = pg.font.SysFont('Arial', FONT_SIZE, bold=False)

CLOCK = pg.time.Clock()

# Генерируем список всех букв и цифр
ALPHABET_AND_NUMBERS = list(ascii_letters) + [i for i in range(0, 10)]
GREEN_ALPHABET_AND_NUMBERS = [FONT.render(str(char), True, pg.Color('green')) for char in ALPHABET_AND_NUMBERS]

# Объект замка
LOCK = RLock()

down_key = ""
keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    keyList.append(char)


class Symbol:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(GREEN_ALPHABET_AND_NUMBERS)
        self.interval = randrange(30, 60)

    def draw(self):
        frames = pg.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(GREEN_ALPHABET_AND_NUMBERS)
        self.y = self.y + self.speed if self.y < HEIGHT else -FONT_SIZE + 48
        SURFACE.blit(self.value, (self.x, self.y))


class SymbolColumn:
    def __init__(self, x, y):
        self.column_height = randrange(6, 10)
        self.symbols = [Symbol(x, i, speed=0.8) for i in range(y, y - FONT_SIZE * self.column_height, -FONT_SIZE)]

    def draw(self):
        [symbol.draw() for symbol in self.symbols]


def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys


# def название_воркера():
#     print('Воркер \'Навзание воркера\' начинает работу')
#
#     while True:
#         что-то делает...


def random_chars():
    print('Воркер \'Рандомные символы\' начинает работу')

    while True:
        SURFACE.fill('black')
        [symbol_column.draw() for symbol_column in symbol_columns]

        LOCK.acquire()
        CLOCK.tick(60)
        LOCK.release()


def date_status():
    print('Воркер \'Статус даты\' начинает работу')

    while True:
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        now_ren = FONT.render(now, True, pg.Color('white'))

        SURFACE.blit(now_ren, (450, 0))
        pg.display.flip()

        LOCK.acquire()
        CLOCK.tick(60)
        LOCK.release()


def key_status():
    print('Воркер \'Статус даты\' начинает работу')

    while True:
        if pg.key.get_pressed():
            key = FONT.render("".join(key_check()).encode("UTF-8"), True, pg.Color('white'))
            down_key = key
        SURFACE.blit(down_key, (300, 0))
        pg.display.flip()

        LOCK.acquire()
        CLOCK.tick(60)
        LOCK.release()


if __name__ == '__main__':
    print('Программа запустилась')

    symbol_columns = [SymbolColumn(x, randrange(-HEIGHT + 208, 208)) for x in range(0, WIDTH, FONT_SIZE)]

    # Создаем потоки
    chars_thread = Thread(target=random_chars)
    date_thread = Thread(target=date_status)
    key_thread = Thread(target=key_status)

    # Флаг отвечает за то, что потоки живы, до конца жизненного цикла основной программы
    chars_thread.setDaemon(True)
    date_thread.setDaemon(True)
    key_thread.setDaemon(True)

    # Стартум потоки
    chars_thread.start()
    date_thread.start()
    key_thread.start()

    # Отслеживаем события для выхода из программы
    run = True
    while run:
        # Список всех нажатых клавиш
        keys = pg.key.get_pressed()

        # По нажатию на ESCAPE
        if keys[pg.K_ESCAPE]:
            run = False

        # По выходу через крестик
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                run = False

quit()
