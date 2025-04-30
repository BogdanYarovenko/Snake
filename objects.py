import pygame as pg
from random import randrange
vector = pg.math.Vector2
class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.get_random_pos()
        self.direct = vector(0, 0)
        self.time = 0
        self.step = game.snake_speed
        self.len = 1
        self.seg = []
        self.dir = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}

    def border(self):
       if(self.is_out_of_bounds()):
            self.game.new_game()

    def is_out_of_bounds(self)-> bool:
        return self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE or self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE
    
    def check(self):
        if (self.has_collision()):
            self.game.apple.rect.center = self.get_random_pos()
            self.len += 1

    def has_collision(self) -> bool:
        return self.rect.colliderect(self.game.apple.rect)
    
    def has_self_collision(self) -> bool:
        return len(self.seg) != len(set(segment.center for segment in self.seg))

    def selfeat(self):
        if self.has_self_collision():
            self.game.new_game()

    def controls(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and self.dir[pg.K_UP]:
                self.direct = vector(0, -self.size)
            elif event.key == pg.K_DOWN and self.dir[pg.K_DOWN]:
                self.direct = vector(0, self.size)
            elif event.key == pg.K_LEFT and self.dir[pg.K_LEFT]:
                self.direct = vector(-self.size, 0)
            elif event.key == pg.K_RIGHT and self.dir[pg.K_RIGHT]:
                self.direct = vector(self.size, 0)
            self.dir = {
                pg.K_UP: self.direct.y >= 0,
                pg.K_DOWN: self.direct.y <= 0,
                pg.K_LEFT: self.direct.x >= 0,
                pg.K_RIGHT: self.direct.x <= 0
            }

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
        self.rect.center = game.snake.get_random_pos()

    def draw(self):
        pg.draw.rect(self.game.screen, 'green', self.rect)
