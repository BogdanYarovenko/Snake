import pygame as pg
from random import randrange

vec2 = pg.math.Vector2


class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.get_random_pos()
        self.direct = vec2(0, 0)
        self.time = 0
        self.step = game.snake_speed
        self.len = 1
        self.seg = []
        self.dir = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}

    def border(self):
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            self.game.new_game()
        if self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE:
            self.game.new_game()

    def check(self):
        if self.rect.center == self.game.apple.rect.center:
            self.game.apple.rect.center = self.get_random_pos()
            self.len += 1

    def selfeat(self):
        if len(self.seg) != len(set(segment.center for segment in self.seg)):
            self.game.new_game()

    def controls(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and self.dir[pg.K_UP]:
                self.dir = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
                self.direct = vec2(0, -self.size)
            if event.key == pg.K_DOWN and self.dir[pg.K_DOWN]:
                self.dir = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}
                self.direct = vec2(0, self.size)
            if event.key == pg.K_LEFT and self.dir[pg.K_LEFT]:
                self.dir = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}
                self.direct = vec2(-self.size, 0)
            if event.key == pg.K_RIGHT and self.dir[pg.K_RIGHT]:
                self.dir = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}
                self.direct = vec2(self.size, 0)

    def del_time(self):
        time_n = pg.time.get_ticks()
        if time_n - self.time > self.step:
            self.time = time_n
            return True
        return False

    def move(self):
        if self.del_time():
            self.rect.move_ip(self.direct)
            self.seg.append(self.rect.copy())
            self.seg = self.seg[-self.len:]

    def get_random_pos(self):
        return [randrange(self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size)] * 2

    def update(self):
        self.selfeat()
        self.check()
        self.move()
        self.border()

    def draw(self):
        [pg.draw.rect(self.game.screen, self.game.snake_color, segment) for segment in self.seg]


class Apple:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.game.snake.get_random_pos()

    def draw(self):
        pg.draw.rect(self.game.screen, 'green', self.rect)
