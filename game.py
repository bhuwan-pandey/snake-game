import pygame
from snake import Snake
from food import NormalFood, SpecialFood
from widgets import Button, Paused_Window
from typing import Literal

pygame.init()
pygame.display.set_caption('Snake')


class Game():
    DISPLAY_INFO = pygame.display.Info()
    CLOCK = pygame.time.Clock()

    def __init__(self) -> None:
        self.PLAYGROUND = pygame.display.set_mode(
            (Game.DISPLAY_INFO.current_w-500, Game.DISPLAY_INFO.current_h-250))
        self._paused_window: Paused_Window = Paused_Window(self.PLAYGROUND)
        self._time_delta = 0
        self.is_not_closed = True
        self.state: Literal['resumed', 'paused', 'over'] = 'resumed'
        self.allow_through_wall = True
        self.move_speed = 2
        self.snake: Snake = Snake()
        self.normal_food: NormalFood = NormalFood()
        self.special_food: SpecialFood = SpecialFood()

    def initialize(self):
        self.snake.food_to_search_for = [self.normal_food, self.special_food]
        self.snake._game = self
        self.normal_food._game = self
        self.special_food._game = self

    def run(self):
        while self.is_not_closed:
            pressed_keys = pygame.key.get_pressed()

            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_not_closed = False
                if event.type == pygame.KEYUP and pressed_keys[pygame.K_ESCAPE]:
                    self.pause_or_resume()

            if self.state == 'paused':
                self.pause()
                self._time_delta = Game.CLOCK.tick(60) / 1000
                continue

            # background color of main resume screen
            self.PLAYGROUND.fill('purple')

            self.normal_food.serve()
            self.special_food.serve()

            # check for key directions
            if pressed_keys[pygame.K_UP]:
                self.snake.move_up()
            elif pressed_keys[pygame.K_DOWN]:
                self.snake.move_down()
            elif pressed_keys[pygame.K_LEFT]:
                self.snake.move_left()
            elif pressed_keys[pygame.K_RIGHT]:
                self.snake.move_right()
            elif self.snake.current_direction == pygame.K_UP:
                self.snake.move_up()
            elif self.snake.current_direction == pygame.K_DOWN:
                self.snake.move_down()
            elif self.snake.current_direction == pygame.K_LEFT:
                self.snake.move_left()
            elif self.snake.current_direction == pygame.K_RIGHT:
                self.snake.move_right()

            # flip() the display to put your work on RESUMED_SCREEN
            pygame.display.flip()

            # limits FPS to 60
            # _time_delta is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self._time_delta = Game.CLOCK.tick(60) / 1000
        pygame.quit()

    def pause_or_resume(self):
        if self.state == 'paused':
            self.resume()
        elif self.state == 'resumed':
            self.pause()

    def resume(self):
        self.state = 'resumed'

    def pause(self):
        self.state = 'paused'
        self._paused_window._window.background_color = 'green'
        self._paused_window.draw()
