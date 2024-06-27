import pygame as pg
from obj import *
import sys


class Game:
    def __init__(self):
        pg.init()
        self.WINDOW_SIZE = 800
        self.TILE_SIZE = 40
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.new_game()

    def draw_grid(self):
        [pg.draw.line(self.screen, [40] * 3, (x, 0), (x, self.WINDOW_SIZE))
         for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        [pg.draw.line(self.screen, [40] * 3, (0,y), (self.WINDOW_SIZE,y))
         for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]

    def new_game(self):
        self.snake = Snake(self)
        self.apple = Apple(self)

    def update(self):
        self.snake.update()
        pg.display.flip()
        self.clock.tick(60)

    def draw(self):
        self.screen.fill('black')
        self.draw_grid()
        self.snake.draw()
        self.apple.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.snake.controls(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
