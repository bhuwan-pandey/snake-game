import pygame
from snake import Snake
from food import NormalFood, SpecialFood
from widgets import Button, Paused_Window
from typing import Literal
from os.path import exists

pygame.init()


class Game():
    DISPLAY_INFO = pygame.display.Info()
    CLOCK = pygame.time.Clock()

    def __init__(self) -> None:
        self.title = 'Snake'
        self.high_score = 0
        self.data_filename = 'data.dat'
        self.PLAYGROUND = pygame.display.set_mode(
            (Game.DISPLAY_INFO.current_w-500, Game.DISPLAY_INFO.current_h-250))
        self._paused_window: Paused_Window = Paused_Window(self.PLAYGROUND)
        self._time_delta = 0
        self.game_has_started = False
        self.is_not_closed = True
        self.state: Literal['resumed', 'paused', 'over'] = 'resumed'
        self.allow_through_wall = True
        self.move_speed = 2
        self.snake: Snake = None
        self.normal_food: NormalFood = None
        self.special_food: SpecialFood = None

    def initialize(self):
        # self.game_has_started = False
        self.snake: Snake = Snake()
        self.snake.position_of_head.x=self.PLAYGROUND.get_width()/2
        self.snake.position_of_directions[0].x=self.snake.position_of_head.x+10
        self.normal_food: NormalFood = NormalFood()
        self.special_food: SpecialFood = SpecialFood()
        self.snake.food_to_search_for = [self.normal_food, self.special_food]
        self.snake._game = self
        self.normal_food._game = self
        self.special_food._game = self
        # read persisted data if exists
        if exists(self.data_filename):
            with open(self.data_filename, 'r') as data:
                line_counter = 1
                for line in data.readlines():
                    try:
                        if line_counter == 1:
                            self.high_score = int(line)
                        elif line_counter == 2:
                            self.move_speed = int(line)
                        elif line_counter == 3:
                            self.allow_through_wall = int(line)
                        line_counter += 1
                    except ValueError:
                        pass
        self.update_caption()

    def update_caption(self):
        level = ''
        if self.move_speed >= 10:
            level = 'Daemon'
        elif self.move_speed >= 8:
            level = 'Legend'
        elif self.move_speed >= 6:
            level = 'Hard'
        elif self.move_speed >= 4:
            level = 'Medium'
        else:
            level = 'Easy'
        current_score = (self.normal_food.consume_count *
                         self.normal_food.calorie)+(self.special_food.consume_count*self.special_food.calorie)
        if current_score > self.high_score:
            self.high_score = current_score
        pygame.display.set_caption(self.title + ' ---> | Score: '+str(current_score)+' | Hight Score: '+str(self.high_score)
                                   + ' | Level: '+level + ' | Wall bypass: ' + ('Yes' if self.allow_through_wall else 'No') + ' |')
        # persist data
        with open(self.data_filename, 'w') as data:
            for line in [self.high_score, self.move_speed, int(self.allow_through_wall)]:
                data.writelines(str(line)+'\n')

    def run(self):
        while self.is_not_closed:
            pressed_keys = pygame.key.get_pressed()

            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_not_closed = False
                if event.type == pygame.KEYUP:
                    if pressed_keys[pygame.K_ESCAPE]:
                        self.pause_or_resume()
                    elif pressed_keys[pygame.K_q]:
                        if self.state != 'resumed':
                            self.is_not_closed = False
                    elif pressed_keys[pygame.K_r]:
                        if self.state != 'resumed':
                            self.state = 'over'
                        # self.initialize()
                    elif pressed_keys[pygame.K_b]:  # toggle allow through wall or not
                        if self.state != 'resumed':
                            self.allow_through_wall = not self.allow_through_wall
                            self.update_caption()
                    elif pressed_keys[pygame.K_l]:  # change level
                        if self.state != 'resumed':
                            if self.move_speed >= 10:
                                self.move_speed = 2
                            else:
                                self.move_speed += 2
                            self.update_caption()

            if self.state == 'paused':
                self.pause()
                self._time_delta = Game.CLOCK.tick(60) / 1000
                continue

            if self.state == 'over':
                self.initialize()
                self.pause()
                self._time_delta = Game.CLOCK.tick(60) / 1000
                continue

            # background color of main resume screen
            self.PLAYGROUND.fill('black')

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

            # to initially display the help information
            if not self.game_has_started:
                self.game_has_started = True
                self.state = 'paused'

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
