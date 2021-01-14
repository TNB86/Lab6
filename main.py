import os
import pygame as pg
from random import choice, randrange
import datetime


class Symbol:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(green_alf)
        self.interval = randrange(30, 60)

    def draw(self):
        frames = pg.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green_alf)
        self.y = self.y + self.speed if self.y < HEIGHT else -FONT_SIZE + 48
        surface.blit(self.value, (self.x, self.y))


class SymbolColumn:
    def __init__(self, x, y):
        self.column_height = randrange(6, 10)
        self.symbols = [Symbol(x, i, speed=0.8) for i in range(y, y - FONT_SIZE * self.column_height, -FONT_SIZE)]

    def draw(self):
        [symbol.draw() for symbol in self.symbols]


os.environ['SDL_VIDEO_CENTERED'] = '1'
RES = WIDTH, HEIGHT = 640, 160
FONT_SIZE = 16

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()

alf = [chr(int("0x0030", 16) + i) for i in range(80)]
now = datetime.datetime.now()
now = now.strftime("%d.%m.%Y %H:%M:%S")
font = pg.font.SysFont('Arial', FONT_SIZE, bold=False)
now_ren = font.render(str(now).encode('UTF-8'), True, pg.Color('white'))
green_alf = [font.render(char, True, pg.Color('green')) for char in alf]

symbol_columns = [SymbolColumn(x, randrange(-HEIGHT + 208, 208)) for x in range(0, WIDTH, FONT_SIZE)]

while True:
    surface.fill(pg.Color('black'))

    surface.blit(now_ren, (520, 0))

    [symbol_column.draw() for symbol_column in symbol_columns]

    [exit() for i in pg.event.get() if i.type == pg.QUIT]
    pg.display.flip()
    clock.tick(60)
