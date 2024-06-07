import game
from food import Food
from typing import List

class Snake():
    def __init__(self) -> None:
        self._game:game.Game=None
        self.width = 10
        self.position_of_head = game.pygame.Vector2(100,100)
        self.position_of_directions = [game.pygame.Vector2(
            self.position_of_head.x+10, self.position_of_head.y)]
        self.current_direction = game.pygame.K_LEFT
        # list of dictionary of direction and draw_next.
        # draw_next helps to determine whether or not two line vertices should be connected/drawn.
        # this is used for phase_shift.
        self.directions_of_position = [
            {'direction': self.current_direction, 'draw_next': True}]
        self.food_to_search_for : List[Food] = []
        # flag to determine whether or not the snake touched and went through a wall
        self.phase_shifted = False
    
    def move(self):
        if self.current_direction == game.pygame.K_UP:
            self.move_up()
        elif self.current_direction == game.pygame.K_DOWN:
            self.move_down()
        elif self.current_direction == game.pygame.K_LEFT:
            self.move_left()
        elif self.current_direction == game.pygame.K_RIGHT:
            self.move_right()

    def move_up(self):
        # prevent reversing the direction in a straight line
        if self.current_direction != game.pygame.K_DOWN:
            # donot/no-need insert/bend if the moving direction and pressed direction are same
            if self.current_direction and self.current_direction != game.pygame.K_UP:
                self.position_of_directions.insert(0, game.pygame.Vector2(
                    self.position_of_head.x, self.position_of_head.y))
                self.directions_of_position.insert(
                    0, {'direction': game.pygame.K_UP, 'draw_next': True})
            self.current_direction = game.pygame.K_UP
            self.position_of_head.y -= self._game.move_speed
            self.slither()
        else:
            # snake was moving down, but up key was pressed.
            # so continue snake moving down
            self.move_down()

    def move_down(self):
        # prevent reversing the direction in a straight line
        if self.current_direction != game.pygame.K_UP:
            # donot/no-need insert/bend if the moving direction and pressed direction are same
            if self.current_direction and self.current_direction != game.pygame.K_DOWN:
                self.position_of_directions.insert(0, game.pygame.Vector2(
                    self.position_of_head.x, self.position_of_head.y))
                self.directions_of_position.insert(
                    0, {'direction': game.pygame.K_DOWN, 'draw_next': True})
            self.current_direction = game.pygame.K_DOWN
            self.position_of_head.y += self._game.move_speed
            self.slither()
        else:
            # snake was moving up, but down key was pressed.
            # so continue snake moving up
            self.move_up()

    def move_left(self):
        # prevent reversing the direction in a straight line
        if self.current_direction != game.pygame.K_RIGHT:
            # donot/no-need insert/bend if the moving direction and pressed direction are same
            if self.current_direction and self.current_direction != game.pygame.K_LEFT:
                self.position_of_directions.insert(0, game.pygame.Vector2(
                    self.position_of_head.x, self.position_of_head.y))
                self.directions_of_position.insert(
                    0, {'direction': game.pygame.K_LEFT, 'draw_next': True})
            self.current_direction = game.pygame.K_LEFT
            self.position_of_head.x -= self._game.move_speed
            self.slither()
        else:
            # snake was moving right, but left key was pressed.
            # so continue snake moving right
            self.move_right()

    def move_right(self):
        # prevent reversing the direction in a straight line
        if self.current_direction != game.pygame.K_LEFT:
            # donot/no-need insert/bend if the moving direction and pressed direction are same
            if self.current_direction and self.current_direction != game.pygame.K_RIGHT:
                self.position_of_directions.insert(0, game.pygame.Vector2(
                    self.position_of_head.x, self.position_of_head.y))
                self.directions_of_position.insert(
                    0, {'direction': game.pygame.K_RIGHT, 'draw_next': True})
            self.current_direction = game.pygame.K_RIGHT
            self.position_of_head.x += self._game.move_speed
            self.slither()
        else:
            # snake was moving left, but right key was pressed.
            # so continue snake moving left
            self.move_left()

    def slither(self, appear=True,phase_shift=True,search_for_food=True,prevent_self_injury=True):
        # decrease the last tail of the snake
        if self.directions_of_position[-1]['direction'] == game.pygame.K_UP:
            self.position_of_directions[-1].y -= self._game.move_speed
            if len(self.position_of_directions) > 1:
                if self.position_of_directions[-1].y <= self.position_of_directions[-2].y:
                    self.position_of_directions.pop()
                    self.directions_of_position.pop()
        elif self.directions_of_position[-1]['direction'] == game.pygame.K_DOWN:
            self.position_of_directions[-1].y += self._game.move_speed
            if len(self.position_of_directions) > 1:
                if self.position_of_directions[-1].y >= self.position_of_directions[-2].y:
                    self.position_of_directions.pop()
                    self.directions_of_position.pop()
        elif self.directions_of_position[-1]['direction'] == game.pygame.K_LEFT:
            self.position_of_directions[-1].x -= self._game.move_speed
            if len(self.position_of_directions) > 1:
                if self.position_of_directions[-1].x <= self.position_of_directions[-2].x:
                    self.position_of_directions.pop()
                    self.directions_of_position.pop()
        elif self.directions_of_position[-1]['direction'] == game.pygame.K_RIGHT:
            self.position_of_directions[-1].x += self._game.move_speed
            if len(self.position_of_directions) > 1:
                if self.position_of_directions[-1].x >= self.position_of_directions[-2].x:
                    self.position_of_directions.pop()
                    self.directions_of_position.pop()
        if not self._game.allow_through_wall:
            if self.position_of_head.x < 5 or self.position_of_head.x+5 >= self._game.PLAYGROUND.get_width() or self.position_of_head.y < 5 or self.position_of_head.y+5 >= self._game.PLAYGROUND.get_height():
                self._game.state='paused'
        if appear:
            self.appear()
        if phase_shift:
            self.phase_shift()
        if search_for_food:
            self.search_for_food()
        if prevent_self_injury:
            self.prevent_self_injury()

    def appear(self):
        # draw snake FROM TAIL TO HEAD
        reversed_directions_of_position = self.directions_of_position.copy()
        reversed_directions_of_position.reverse()
        reversed_position_of_directions = self.position_of_directions.copy()
        reversed_position_of_directions.reverse()
        # draw body segments if any
        for index_of_current_position_of_direction, current_position_of_direction in enumerate(reversed_position_of_directions):
            if len(reversed_position_of_directions) > index_of_current_position_of_direction+1 and reversed_directions_of_position[index_of_current_position_of_direction]['draw_next']:
                game.pygame.draw.line(self._game.PLAYGROUND, "red", (current_position_of_direction.x, current_position_of_direction.y), (
                    reversed_position_of_directions[index_of_current_position_of_direction+1].x, reversed_position_of_directions[index_of_current_position_of_direction+1].y), self.width)
        # finally connect to head
        game.pygame.draw.line(self._game.PLAYGROUND, "red", (self.position_of_directions[0].x, self.position_of_directions[0].y), (
            self.position_of_head.x, self.position_of_head.y), self.width)

        # draw head/curve and the eyes
        if self.current_direction == game.pygame.K_UP:
            # head
            game.pygame.draw.circle(
                self._game.PLAYGROUND, 'red', (self.position_of_head.x+1, self.position_of_head.y), 5)
            # eyes
            game.pygame.draw.circle(
                self._game.PLAYGROUND, 'blue', (self.position_of_head.x-2, self.position_of_head.y), 1)
            game.pygame.draw.circle(
                self._game.PLAYGROUND, 'blue', (self.position_of_head.x+3, self.position_of_head.y), 1)
            # tongue
            game.pygame.draw.line(self._game.PLAYGROUND, 'red', (self.position_of_head.x,
                                     self.position_of_head.y), (self.position_of_head.x-2, self.position_of_head.y-8), 1)
            game.pygame.draw.line(self._game.PLAYGROUND, 'red', (self.position_of_head.x,
                                     self.position_of_head.y), (self.position_of_head.x+2, self.position_of_head.y-8), 1)
        elif self.current_direction == game.pygame.K_DOWN:
            # head
            game.pygame.draw.circle(
                self._game.PLAYGROUND, 'red', (self.position_of_head.x+1, self.position_of_head.y), 5)
            # eyes
            game.pygame.draw.circle(
                self._game.PLAYGROUND, 'blue', (self.position_of_head.x-2, self.position_of_head.y), 1)
            game.pygame.draw.circle(
                self._game.PLAYGROUND, 'blue', (self.position_of_head.x+3, self.position_of_head.y), 1)
            # tongue
            game.pygame.draw.line(self._game.PLAYGROUND, 'red', (self.position_of_head.x,
                                     self.position_of_head.y), (self.position_of_head.x-2, self.position_of_head.y+8), 1)
            game.pygame.draw.line(self._game.PLAYGROUND, 'red', (self.position_of_head.x,
                                     self.position_of_head.y), (self.position_of_head.x+2, self.position_of_head.y+8), 1)
        elif self.current_direction == game.pygame.K_LEFT:
            # head
            game.pygame.draw.circle(
                self._game.PLAYGROUND, 'red', (self.position_of_head.x, self.position_of_head.y+1), 5)
            # eyes
            game.pygame.draw.circle(
                self._game.PLAYGROUND, 'blue', (self.position_of_head.x, self.position_of_head.y-2), 1)
            game.pygame.draw.circle(
                self._game.PLAYGROUND, 'blue', (self.position_of_head.x, self.position_of_head.y+3), 1)
            # tongue
            game.pygame.draw.line(self._game.PLAYGROUND, 'red', (self.position_of_head.x,
                                     self.position_of_head.y), (self.position_of_head.x-8, self.position_of_head.y-2), 1)
            game.pygame.draw.line(self._game.PLAYGROUND, 'red', (self.position_of_head.x,
                                     self.position_of_head.y), (self.position_of_head.x-8, self.position_of_head.y+2), 1)
        elif self.current_direction == game.pygame.K_RIGHT:
            # head
            game.pygame.draw.circle(
                self._game.PLAYGROUND, 'red', (self.position_of_head.x, self.position_of_head.y+1), 5)
            # eyes
            game.pygame.draw.circle(
                self._game.PLAYGROUND, 'blue', (self.position_of_head.x, self.position_of_head.y-2), 1)
            game.pygame.draw.circle(
                self._game.PLAYGROUND, 'blue', (self.position_of_head.x, self.position_of_head.y+3), 1)
            # tongue
            game.pygame.draw.line(self._game.PLAYGROUND, 'red', (self.position_of_head.x,
                                     self.position_of_head.y), (self.position_of_head.x+8, self.position_of_head.y-2), 1)
            game.pygame.draw.line(self._game.PLAYGROUND, 'red', (self.position_of_head.x,
                                     self.position_of_head.y), (self.position_of_head.x+8, self.position_of_head.y+2), 1)

    def get_horizontal_body_coordinates(self):
        coordinates = []
        # copy(to avoid mutation) and reverse the positions and directions
        reversed_directions_of_position = self.directions_of_position.copy()
        reversed_directions_of_position.reverse()
        reversed_position_of_directions = self.position_of_directions.copy()
        reversed_position_of_directions.reverse()
        for index_of_position, position_of_direction in enumerate(reversed_position_of_directions):
            # if the position/line starts towards either right or left
            if reversed_directions_of_position[index_of_position]['direction'] in (game.pygame.K_LEFT, game.pygame.K_RIGHT):
                # length 1 means only tail exist. so return range from tail to head
                if len(reversed_position_of_directions) == 1 or index_of_position+1 >= len(reversed_position_of_directions):
                    coordinates.append(
                        [position_of_direction, self.position_of_head])
                else:  # if there are actually bends/curves except for the tail
                    coordinates.append(
                        [position_of_direction, reversed_position_of_directions[index_of_position+1]])
        return coordinates

    def get_vertical_body_coordinates(self):
        coordinates = []
        # copy(to avoid mutation) and reverse the positions and directions
        reversed_directions_of_position = self.directions_of_position.copy()
        reversed_directions_of_position.reverse()
        reversed_position_of_directions = self.position_of_directions.copy()
        reversed_position_of_directions.reverse()
        for index_of_position, position_of_direction in enumerate(reversed_position_of_directions):
            # if the position/line starts towards either right or left
            if reversed_directions_of_position[index_of_position]['direction'] in (game.pygame.K_UP, game.pygame.K_DOWN):
                # length 1 means only tail exist. so return range from tail to head
                if len(reversed_position_of_directions) == 1 or index_of_position+1 >= len(reversed_position_of_directions):
                    coordinates.append(
                        [position_of_direction, self.position_of_head])
                else:  # if there are actually bends/curves except for the tail
                    coordinates.append(
                        [position_of_direction, reversed_position_of_directions[index_of_position+1]])
        return coordinates

    def prevent_self_injury(self):
        if len(self.position_of_directions) <= 1:
            return
        reversed_directions_of_position = self.directions_of_position.copy()
        reversed_directions_of_position.reverse()
        reversed_position_of_directions = self.position_of_directions.copy()
        reversed_position_of_directions.reverse()
        for index_of_position, position_of_direction in enumerate(reversed_position_of_directions):
            if (self.position_of_head.x == position_of_direction.x and self.position_of_head.y == position_of_direction.y):
                continue
            if index_of_position+1 >= len(reversed_position_of_directions):
                continue
            if self.current_direction == game.pygame.K_UP:  # snake moving up
                # body line moving towards left
                if reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_LEFT:
                    if self.position_of_head.x > reversed_position_of_directions[index_of_position+1].x and self.position_of_head.x < position_of_direction.x and self.position_of_head.y < position_of_direction.y+self.width/2 and self.position_of_head.y > position_of_direction.y-self.width/2:
                        self._game.state='paused'
                        print("up left")
                # body line moving towards right
                elif reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_RIGHT:
                    if self.position_of_head.x > position_of_direction.x and self.position_of_head.x < reversed_position_of_directions[index_of_position+1].x and self.position_of_head.y < position_of_direction.y+self.width/2 and self.position_of_head.y > position_of_direction.y-self.width/2:
                        self._game.state='paused'
                        print("up right")
                # body line moving towards up
                elif reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_UP:
                    if self.position_of_head.x > position_of_direction.x-self.width/2 and self.position_of_head.x < position_of_direction.x+self.width/2 and self.position_of_head.y < position_of_direction.y and self.position_of_head.y > reversed_position_of_directions[index_of_position+1].y:
                        self._game.state='paused'
                        print("up up")
                # body line moving towards down
                elif reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_DOWN:
                    if self.position_of_head.x > position_of_direction.x-self.width/2 and self.position_of_head.x < position_of_direction.x+self.width/2 and self.position_of_head.y < reversed_position_of_directions[index_of_position+1].y and self.position_of_head.y > position_of_direction.y:
                        self._game.state='paused'
                        print("up down")
            elif self.current_direction == game.pygame.K_DOWN:  # snake moving down
                # body line moving towards left
                if reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_LEFT:
                    if self.position_of_head.x > reversed_position_of_directions[index_of_position+1].x and self.position_of_head.x < position_of_direction.x and self.position_of_head.y > position_of_direction.y-self.width/2 and self.position_of_head.y < position_of_direction.y+self.width/2:
                        self._game.state='paused'
                        print("down left")
                # body line moving towards right
                elif reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_RIGHT:
                    if self.position_of_head.x > position_of_direction.x and self.position_of_head.x < reversed_position_of_directions[index_of_position+1].x and self.position_of_head.y > position_of_direction.y-self.width/2 and self.position_of_head.y < position_of_direction.y+self.width/2:
                        self._game.state='paused'
                        print("down right")
                # body line moving towards up
                elif reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_UP:
                    if self.position_of_head.x > position_of_direction.x-self.width/2 and self.position_of_head.x < position_of_direction.x+self.width/2 and self.position_of_head.y > reversed_position_of_directions[index_of_position+1].y and self.position_of_head.y < position_of_direction.y:
                        self._game.state='paused'
                        print("down up")
                # body line moving towards down
                elif reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_DOWN:
                    if self.position_of_head.x > position_of_direction.x-self.width/2 and self.position_of_head.x < position_of_direction.x+self.width/2 and self.position_of_head.y > position_of_direction.y and self.position_of_head.y < reversed_position_of_directions[index_of_position+1].y:
                        self._game.state='paused'
                        print("down down")
            elif self.current_direction == game.pygame.K_LEFT:  # snake moving down
                # body line moving towards left
                if reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_LEFT:
                    if self.position_of_head.x < position_of_direction.x and self.position_of_head.x > reversed_position_of_directions[index_of_position+1].x and self.position_of_head.y > position_of_direction.y-self.width/2 and self.position_of_head.y < position_of_direction.y+self.width/2:
                        self._game.state='paused'
                        print("left left")
                # body line moving towards right
                elif reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_RIGHT:
                    if self.position_of_head.x < reversed_position_of_directions[index_of_position+1].x and self.position_of_head.x > position_of_direction.x and self.position_of_head.y > position_of_direction.y-self.width/2 and self.position_of_head.y < position_of_direction.y+self.width/2:
                        self._game.state='paused'
                        print("left right")
                # body line moving towards up
                elif reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_UP:
                    if self.position_of_head.x < position_of_direction.x+self.width/2 and self.position_of_head.x > position_of_direction.x-self.width/2 and self.position_of_head.y < position_of_direction.y and self.position_of_head.y > reversed_position_of_directions[index_of_position+1].y:
                        self._game.state='paused'
                        print("left up")
                # body line moving towards down
                elif reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_DOWN:
                    if self.position_of_head.x < position_of_direction.x+self.width/2 and self.position_of_head.x > position_of_direction.x-self.width/2 and self.position_of_head.y > position_of_direction.y and self.position_of_head.y < reversed_position_of_directions[index_of_position+1].y:
                        self._game.state='paused'
                        print("left down")
            elif self.current_direction == game.pygame.K_RIGHT:  # snake moving down
                # body line moving towards left
                if reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_LEFT:
                    if self.position_of_head.x > reversed_position_of_directions[index_of_position+1].x and self.position_of_head.x < position_of_direction.x and self.position_of_head.y > position_of_direction.y-self.width/2 and self.position_of_head.y < position_of_direction.y+self.width/2:
                        self._game.state='paused'
                        print("right left")
                # body line moving towards right
                elif reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_RIGHT:
                    if self.position_of_head.x > position_of_direction.x and self.position_of_head.x < reversed_position_of_directions[index_of_position+1].x and self.position_of_head.y > position_of_direction.y-self.width/2 and self.position_of_head.y < position_of_direction.y+self.width/2:
                        self._game.state='paused'
                        print("right right")
                # body line moving towards up
                elif reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_UP:
                    if self.position_of_head.x > position_of_direction.x-self.width/2 and self.position_of_head.x < position_of_direction.x+self.width/2 and self.position_of_head.y > reversed_position_of_directions[index_of_position+1].y and self.position_of_head.y < position_of_direction.y:
                        self._game.state='paused'
                        print("right up")
                # body line moving towards down
                elif reversed_directions_of_position[index_of_position]['direction'] == game.pygame.K_DOWN:
                    if self.position_of_head.x > position_of_direction.x-self.width/2 and self.position_of_head.x < position_of_direction.x+self.width/2 and self.position_of_head.y > position_of_direction.y and self.position_of_head.y < reversed_position_of_directions[index_of_position+1].y:
                        self._game.state='paused'
                        print("right down")

    def search_for_food(self):
        for food in self.food_to_search_for:
            if food.position.x > 0 and food.position.y > 0:  # x/y less than 1 means food not available/rendered
                if self.position_of_head.x > food.position.x-food.size and self.position_of_head.x < food.position.x+food.size and self.position_of_head.y > food.position.y-food.size and self.position_of_head.y < food.position.y+food.size:
                    food.position.x = -food.size*2
                    food.position.y = -food.size*2
                    food.consume_count += 1
                    # increase head by half the calorie
                    if self.current_direction == game.pygame.K_UP:
                        if self.position_of_head.y-(food.calorie/2) > 0:
                            self.position_of_head.y -= food.calorie/2
                    elif self.current_direction == game.pygame.K_DOWN:
                        if self.position_of_head.y+(food.calorie/2) < self._game.PLAYGROUND.get_height():
                            self.position_of_head.y += food.calorie/2
                    elif self.current_direction == game.pygame.K_LEFT:
                        if self.position_of_head.x-(food.calorie/2) > 0:
                            self.position_of_head.x -= food.calorie/2
                    elif self.current_direction == game.pygame.K_RIGHT:
                        if self.position_of_head.x+(food.calorie/2) < self._game.PLAYGROUND.get_width():
                            self.position_of_head.x += food.calorie/2
                    # increase tail by half the calorie
                    if self.directions_of_position[-1]['direction'] == game.pygame.K_UP:
                        if self.position_of_directions[-1].y+(food.calorie/2) < self._game.PLAYGROUND.get_height():
                            self.position_of_directions[-1].y += food.calorie/2
                    elif self.directions_of_position[-1]['direction'] == game.pygame.K_DOWN:
                        if self.position_of_directions[-1].y-(food.calorie/2) > 0:
                            self.position_of_directions[-1].y -= food.calorie/2
                    elif self.directions_of_position[-1]['direction'] == game.pygame.K_LEFT:
                        if self.position_of_directions[-1].x+(food.calorie/2) < self._game.PLAYGROUND.get_width():
                            self.position_of_directions[-1].x += food.calorie/2
                    elif self.directions_of_position[-1]['direction'] == game.pygame.K_RIGHT:
                        if self.position_of_directions[-1].x-(food.calorie/2) > 0:
                            self.position_of_directions[-1].x -= food.calorie/2

    def total_body_length(self):
        length = 0
        reversed_directions_of_position = self.directions_of_position.copy()
        reversed_directions_of_position.reverse()
        reversed_position_of_directions = self.position_of_directions.copy()
        reversed_position_of_directions.reverse()
        # count body length except for upto head
        for index_of_current_position_of_direction, current_position_of_direction in enumerate(reversed_position_of_directions):
            if len(reversed_position_of_directions) > index_of_current_position_of_direction+1 and reversed_directions_of_position[index_of_current_position_of_direction]['draw_next']:
                if reversed_directions_of_position[index_of_current_position_of_direction]['direction'] in (game.pygame.K_LEFT, game.pygame.K_RIGHT):
                    length += abs(current_position_of_direction.x -
                                  reversed_position_of_directions[index_of_current_position_of_direction+1].x)
                else:
                    length += abs(current_position_of_direction.y -
                                  reversed_position_of_directions[index_of_current_position_of_direction+1].y)
        # count to head
        if self.current_direction in (game.pygame.K_LEFT, game.pygame.K_RIGHT):
            length += abs(self.position_of_directions[0].x -
                          self.position_of_head.x)
        else:
            length += abs(self.position_of_directions[0].y -
                          self.position_of_head.y)
        return length

    def phase_shift(self):
        if not self._game.allow_through_wall:
            if self.position_of_head.x < 5 or self.position_of_head.x+5 >= self._game.PLAYGROUND.get_width() or self.position_of_head.y < 5 or self.position_of_head.y+5 >= self._game.PLAYGROUND.get_height():
                self._game.state='paused'
        else:
            if not self.phase_shifted:
                if self.current_direction == game.pygame.K_LEFT:
                    if self.position_of_head.x < 1:
                        self.position_of_directions.insert(
                            0, game.pygame.Vector2(0, self.position_of_head.y))
                        self.directions_of_position.insert(
                            0, {'direction': self.current_direction, 'draw_next': False})
                        self.position_of_directions.insert(0, game.pygame.Vector2(
                            self._game.PLAYGROUND.get_width(), self.position_of_head.y))
                        self.directions_of_position.insert(
                            0, {'direction': self.current_direction, 'draw_next': True})
                        self.position_of_head.x = self.position_of_head.x+self._game.PLAYGROUND.get_width()
                        # reduce tail without recursing
                        self.slither(False,False,False,False)
                        self.phase_shifted = True
                elif self.current_direction == game.pygame.K_RIGHT:
                    if self.position_of_head.x >=self._game.PLAYGROUND.get_width():
                        self.position_of_directions.insert(
                            0, game.pygame.Vector2(self._game.PLAYGROUND.get_width(), self.position_of_head.y))
                        self.directions_of_position.insert(
                            0, {'direction': self.current_direction, 'draw_next': False})
                        self.position_of_directions.insert(0, game.pygame.Vector2(
                            0, self.position_of_head.y))
                        self.directions_of_position.insert(
                            0, {'direction': self.current_direction, 'draw_next': True})
                        self.position_of_head.x =self.position_of_head.x-self._game.PLAYGROUND.get_width()
                        # reduce tail without recursing
                        self.slither(False,False,False,False)
                        self.phase_shifted = True
                elif self.current_direction == game.pygame.K_UP:
                    if self.position_of_head.y <1:
                        self.position_of_directions.insert(
                            0, game.pygame.Vector2(self.position_of_head.x,0))
                        self.directions_of_position.insert(
                            0, {'direction': self.current_direction, 'draw_next': False})
                        self.position_of_directions.insert(0, game.pygame.Vector2(
                            self.position_of_head.x,self._game.PLAYGROUND.get_height()))
                        self.directions_of_position.insert(
                            0, {'direction': self.current_direction, 'draw_next': True})
                        self.position_of_head.y = self.position_of_head.y+self._game.PLAYGROUND.get_height()
                        # reduce tail without recursing
                        self.slither(False,False,False,False)
                        self.phase_shifted = True
                elif self.current_direction == game.pygame.K_DOWN:
                    if self.position_of_head.y >=self._game.PLAYGROUND.get_height():
                        self.position_of_directions.insert(
                            0, game.pygame.Vector2(self.position_of_head.x,self._game.PLAYGROUND.get_height()))
                        self.directions_of_position.insert(
                            0, {'direction': self.current_direction, 'draw_next': False})
                        self.position_of_directions.insert(0, game.pygame.Vector2(
                            self.position_of_head.x,0))
                        self.directions_of_position.insert(
                            0, {'direction': self.current_direction, 'draw_next': True})
                        self.position_of_head.y = self.position_of_head.y-self._game.PLAYGROUND.get_height()
                        # reduce tail without recursing
                        self.slither(False,False,False,False)
                        self.phase_shifted = True
            else:
                self.phase_shifted = False
