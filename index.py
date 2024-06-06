
from food import *
from snake import *
import utility


snake = Snake()
normal_food = NormalFood()
special_food = SpecialFood()
snake.food_to_search_for = [normal_food, special_food]

while utility.game_is_not_closed:
    pressed_keys = utility.pygame.key.get_pressed()

    # poll for events
    # utility.pygame.QUIT event means the user clicked X to close your window
    for event in utility.pygame.event.get():
        if event.type == utility.pygame.QUIT:
            utility.game_is_not_closed = False
        if event.type == utility.pygame.KEYUP and pressed_keys[utility.pygame.K_ESCAPE]:
            utility.game_is_paused = not utility.game_is_paused

    if utility.game_is_paused:
        utility.pause_game()
        utility.time_delta = utility.CLOCK.tick(60) / 1000
        continue

    # fill the utility.RESUMED_SCREEN with a color to wipe away anything from last frame
    utility.RESUMED_SCREEN.fill("purple")

    normal_food.serve()
    special_food.serve()

    # check for key directions
    if pressed_keys[utility.pygame.K_UP]:
        snake.move_up()
    elif pressed_keys[utility.pygame.K_DOWN]:
        snake.move_down()
    elif pressed_keys[utility.pygame.K_LEFT]:
        snake.move_left()
    elif pressed_keys[utility.pygame.K_RIGHT]:
        snake.move_right()
    elif snake.current_direction == utility.pygame.K_UP:
        snake.move_up()
    elif snake.current_direction == utility.pygame.K_DOWN:
        snake.move_down()
    elif snake.current_direction == utility.pygame.K_LEFT:
        snake.move_left()
    elif snake.current_direction == utility.pygame.K_RIGHT:
        snake.move_right()

    # flip() the display to put your work on utility.RESUMED_SCREEN
    utility.pygame.display.flip()

    # limits FPS to 60
    # utility.time_delta is delta time in seconds since last frame, used for framerate-
    # independent physics.
    utility.time_delta = utility.CLOCK.tick(60) / 1000

utility.pygame.quit()
