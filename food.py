import game
from random import randint


class Food():
    def __init__(self) -> None:
        self.name = 'Food'
        self.calorie = 0
        self.expiry = 0  # in ms
        self.size = 5  # radius because of circle
        self.last_served_at = 0  # ms
        self.position = game.pygame.Vector2(50, 50)
        self.serve_count = 0  # count of served
        self.consume_count = 0  # count of consumed
        self.serve_time = 600000  # serve at new location every ms

    def serve(self):
        pass


class NormalFood(Food):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Normal Food'
        self.calorie = 15

    def serve(self):
        if self.position.x < 1 and self.position.y < 1:  # x/y less than 1 means snake ate the food
            self.serve_count += 1
            self.last_served_at = game.pygame.time.get_ticks()
            self.position.x = randint(
                self.size, game.game.PLAYGROUND.get_width()-self.size)
            self.position.y = randint(
                self.size, game.game.PLAYGROUND.get_height()-self.size)
        game.pygame.draw.circle(
            game.game.PLAYGROUND, 'yellow', self.position, self.size)

class SpecialFood(Food):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Special Food'
        self.calorie = 30
        self.size = 10
        self.expiry = 10000
        self.serve_time = 60000

    def serve(self):
        if (self.position.x < 1 and self.position.y < 1):  # not rendered/visible
            if game.pygame.time.get_ticks()-self.last_served_at > self.serve_time:
                self.serve_count += 1
                self.last_served_at = game.pygame.time.get_ticks()
                self.position.x = randint(
                    self.size, game.game.PLAYGROUND.get_width()-self.size)
                self.position.y = randint(
                    self.size, game.game.PLAYGROUND.get_height()-self.size)
        elif (game.pygame.time.get_ticks()-self.last_served_at > self.expiry):  # rendered and expiry
            self.position.x = -self.size*2
            self.position.y = -self.size*2
        game.pygame.draw.circle(
            game.game.PLAYGROUND, 'yellow', self.position, self.size)
