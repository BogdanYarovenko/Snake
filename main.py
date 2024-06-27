import pygame as pg
from obj import *
import sys


class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pg.font.Font(None, 74)
        self.options = ["New Game", "Settings", "Exit"]
        self.selected = 0

    def draw(self):
        self.screen.fill('black')
        for i, option in enumerate(self.options):
            color = 'white' if i == self.selected else 'gray'
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.game.WINDOW_SIZE / 2, self.game.WINDOW_SIZE / 2 + i * 100))
            self.screen.blit(text, text_rect)
        pg.display.flip()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    if event.key == pg.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    if event.key == pg.K_RETURN:
                        if self.selected == 0:
                            return 'new_game'
                        elif self.selected == 1:
                            return 'settings'
                        elif self.selected == 2:
                            pg.quit()
                            sys.exit()

            self.draw()


class Settings:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pg.font.Font(None, 50)
        self.options = ["Window Size", "Snake Color", "Speed", "Save"]
        self.values = [800, 'yellow', 100]  # Default values
        self.selected = 0
        self.colors = ['yellow', 'green', 'red', 'blue']
        self.color_index = 0

    def draw(self):
        self.screen.fill('black')
        for i, option in enumerate(self.options):
            color = 'white' if i == self.selected else 'gray'
            if option == "Save":
                text = self.font.render(option, True, color)
            else:
                text = self.font.render(f"{option}: {self.values[i]}", True, color)
            text_rect = text.get_rect(center=(self.game.WINDOW_SIZE / 2, self.game.WINDOW_SIZE / 2 + i * 100))
            self.screen.blit(text, text_rect)
        pg.display.flip()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    if event.key == pg.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    if event.key == pg.K_RETURN:
                        if self.selected == 0:  # Window Size
                            self.values[0] = 600 if self.values[0] == 800 else 800
                        elif self.selected == 1:  # Snake Color
                            self.color_index = (self.color_index + 1) % len(self.colors)
                            self.values[1] = self.colors[self.color_index]
                        elif self.selected == 2:  # Speed
                            self.values[2] = 50 if self.values[2] == 100 else 100
                        elif self.selected == 3:  # Save
                            return self.values

            self.draw()


class Game:
    def __init__(self):
        pg.init()
        self.WINDOW_SIZE = 800
        self.TILE_SIZE = 40
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.snake_color = 'yellow'
        self.snake_speed = 100
        self.menu = Menu(self)
        self.settings = Settings(self)
        self.new_game()

    def draw_grid(self):
        [pg.draw.line(self.screen, [40] * 3, (x, 0), (x, self.WINDOW_SIZE))
         for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        [pg.draw.line(self.screen, [40] * 3, (0, y), (self.WINDOW_SIZE, y))
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
            action = self.menu.run()
            if action == 'new_game':
                self.new_game()
                while True:
                    self.check_events()
                    self.update()
                    self.draw()
            elif action == 'settings':
                self.WINDOW_SIZE, self.snake_color, self.snake_speed = self.settings.run()
                self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
                self.new_game()
                while True:
                    self.check_events()
                    self.update()
                    self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
