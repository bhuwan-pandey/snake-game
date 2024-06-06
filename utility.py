import pygame
from random import randint
from widgets import Button

pygame.init()
DISPLAY_INFO = pygame.display.Info()
RESUMED_SCREEN = pygame.display.set_mode(
    (DISPLAY_INFO.current_w-500, DISPLAY_INFO.current_h-250))
PAUSED_SCREEN = pygame.display.set_mode(
    (DISPLAY_INFO.current_w-500, DISPLAY_INFO.current_h-250))
CLOCK = pygame.time.Clock()

game_is_not_closed = True
game_is_paused = False
time_delta = 0
ALLOW_THROUGH_WALL = True
MOVE_FACTOR = 2



def pause_game():
    PAUSED_SCREEN.fill('yellow')
    resume_button = Button(PAUSED_SCREEN,"Resume")
    resume_button.border_width=5
    resume_button.background_color='red'
    resume_button.draw()
    # pygame.display.flip()