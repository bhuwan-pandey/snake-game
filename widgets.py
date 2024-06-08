import pygame
from typing import Literal


class Property():
    def __init__(self) -> None:
        super(Property, self).__init__()
        self.visible = True
        self.enabled = True
        self.position: pygame.Vector2 = pygame.Vector2(0, 0)


class Style():
    def __init__(self) -> None:
        super(Style, self).__init__()
        self.foreground_color = 'black'
        self.background_color = None
        self.vertical_alignment: Literal['top',
                                         'center', 'bottom'] = 'center'
        self.horizontal_alignment: Literal['left',
                                           'center', 'right'] = 'center'


class Text_Style(Style):
    def __init__(self) -> None:
        super(Text_Style, self).__init__()
        self.bold = False
        self.italic = False


class Text(Text_Style, Property):
    def __init__(self) -> None:
        super(Text, self).__init__()
        self.text_caption = 'Text'
        self.font_name = 'Arial'
        self.text_size = 12
        self.font_object: pygame.font.Font = None
        self.surface: pygame.surface.Surface = None

    def __init__(self, text_caption='Text', font_name='Arial', text_size=12, bold=False, italic=False, foreground_color='black', background_color=None, position: pygame.Vector2 = pygame.Vector2(0, 0), vertical_alignment='center', horizontal_alignment='center'):
        super(Text, self).__init__()
        self.text_caption = text_caption
        self.font_name = font_name
        self.text_size = text_size
        self.bold = bold
        self.italic = italic
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.position = position
        self.vertical_alignment = vertical_alignment
        self.horizontal_alignment = horizontal_alignment
        self.font_object: pygame.font.Font = None
        self.surface: pygame.surface.Surface = None


class Button(Style, Property):
    def __init__(self) -> None:
        super(Button, self).__init__()
        self.width = 100
        self.height = 30
        self.border_width = 2
        self.border_radius = -1
        self.border_top_left_radius = -1
        self.border_top_right_radius = -1
        self.border_bottom_left_radius = -1
        self.border_bottom_right_radius = -1
        self.button_text = 'Button'
        self._parent_surface: pygame.surface.Surface = None
        self._text_object: Text = Text()
        self._font_object: pygame.font.Font = pygame.font.SysFont(
            self._text_object.font_name, self._text_object.text_size, self._text_object.bold, self._text_object.italic)
        self._text_surface: pygame.surface.Surface = self._font_object.render(
            self._text_object.font_name, False, self._text_object.foreground_color, self._text_object.background_color)
        self.on_click: function = None

    def __init__(self, _parent_surface: pygame.surface.Surface, button_text: str):
        super(Button, self).__init__()
        self.width = 100
        self.height = 30
        self.border_width = 2
        self.border_radius = -1
        self.border_top_left_radius = -1
        self.border_top_right_radius = -1
        self.border_bottom_left_radius = -1
        self.border_bottom_right_radius = -1
        self.button_text = button_text
        self._surface: pygame.surface.Surface = None
        self._parent_surface = _parent_surface
        self._text_object: Text = Text()
        self._font_object: pygame.font.Font = pygame.font.SysFont(
            self._text_object.font_name, self._text_object.text_size, self._text_object.bold, self._text_object.italic)
        self._text_surface: pygame.surface.Surface = self._font_object.render(
            button_text, False, self._text_object.foreground_color, self._text_object.background_color)
        self.on_click: function = None

    def draw(self):
        if self.visible:
            pygame.draw.rect(self._parent_surface, self.foreground_color, (self.position.x, self.position.y, self.width, self.height),
                             self.border_width, self.border_radius, self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius)
            if self.background_color:
                background_surface = pygame.surface.Surface(
                    (self.width-self.border_width*2, self.height-self.border_width*2))
                background_surface.fill(self.background_color)
            button_text_position_inside_borders = pygame.Vector2(
                self.position.x, self.position.y)
            # horizontal alignment
            if self._text_object.horizontal_alignment == 'left':
                button_text_position_inside_borders.x = self.border_width
            elif self._text_object.horizontal_alignment == 'center':
                button_text_position_inside_borders.x = (
                    self.width/2-self._text_surface.get_width()/2)-self.border_width/2
            elif self._text_object.horizontal_alignment == 'right':
                button_text_position_inside_borders.x = self.width - \
                    self._text_surface.get_width()-self.border_width
            # vertical alignment
            if self._text_object.vertical_alignment == 'top':
                button_text_position_inside_borders.y = self.border_width
            elif self._text_object.vertical_alignment == 'center':
                button_text_position_inside_borders.y = (
                    (self.height/2)-self._text_surface.get_height()/2)-self.border_width/2
            elif self._text_object.vertical_alignment == 'bottom':
                button_text_position_inside_borders.y = self.height - \
                    self._text_surface.get_height()-self.border_width
            background_surface.blit(
                self._text_surface, button_text_position_inside_borders)
            self._parent_surface.blit(
                background_surface, (self.position.x+self.border_width, self.position.y+self.border_width))
            # self._parent_surface.blit(
            #     self._text_surface, button_text_position_inside_borders)
            pygame.display.flip()
        # return self so that draw can be called upon creating instance and return instance itself to store it
        return self


class Window(Property):
    def __init__(self, parent_surface: pygame.surface.Surface) -> None:
        super().__init__()
        self._surface: pygame.surface.Surface = None
        # self._surface:pygame.surface.Surface=None
        self._parent_surface: pygame.surface.Surface = parent_surface
        self.width = 200
        self.height = 200
        self.background_color = 'white'
        self.title_line_color = 'black'
        self.title_background_color = 'white'
        self.title_text = 'Window'
        self.title_text_color = 'black'
        self._text_object: Text = Text()
        self._font_object: pygame.font.Font = None
        self._text_surface: pygame.surface.Surface = None
        self._close_button: Button = None

    def on_close(self):
        self.visible = False

    def draw(self):
        if not self._surface and self._parent_surface:
            self._surface = pygame.surface.Surface((self.width, self.height))
        if self.position.x <= 0 and self.position.y <= 0:
            self.position.x = self._parent_surface.get_width()/2-self._surface.get_width()/2
            self.position.y = self._parent_surface.get_height()/2-self._surface.get_height()/2
        if self.visible and self._surface:
            self._surface.fill(self.background_color)
            # render title
            if self.title_background_color:
                title_background_surface = pygame.surface.Surface(
                    (self.width, 30))
                title_background_surface.fill(self.title_background_color)
                self._surface.blit(title_background_surface, (0, 0))
            self._font_object: pygame.font.Font = pygame.font.SysFont(
                'Arial', 16)
            self._text_surface: pygame.surface.Surface = self._font_object.render(
                self.title_text, False, self.title_text_color)
            self._surface.blit(self._text_surface, (self.width/2 -
                               self._text_surface.get_width()/2, 30/2-self._text_surface.get_height()/2))
            # close button
            # if self._surface and not self._close_button:
            #     self._close_button = Button(self._surface, 'X')
            #     self._close_button.background_color = 'red'
            #     self._close_button.foreground_color = 'white'
            #     self._close_button.width = 25
            #     self._close_button.position.x = self.width-self._close_button.width
            #     self._close_button.draw()
            # blit and render
            pygame.draw.line(self._surface, self.title_line_color,
                             (0, 30), (self._surface.get_width(), 30))
            self._parent_surface.blit(self._surface, self.position)
            pygame.display.flip()


class Paused_Window():
    def __init__(self, parent_surface: pygame.surface.Surface) -> None:
        # super().__init__()
        self._window: Window = Window(parent_surface)
        self._window.width = parent_surface.get_width()/2
        self._window.height = parent_surface.get_height()/2
        self._window.title_text = 'Information'

    def draw(self):
        if not self._window._surface:  # initialize window surface
            self._window.draw()
        if self._window.visible:
            font_object = pygame.font.SysFont(
                'Arial', 16)
            text_surface1 = font_object.render(
                '1. Press ESC to toggle between pause and resume game.', False, 'black')
            self._window._surface.blit(text_surface1, (20, 50))
            text_surface2 = font_object.render(
                '2. Press B to toggle between bypassing/allowing through wall or not.', False, 'black')
            text_surface3 = font_object.render(
                '3. Press R to restart the game.', False, 'black')
            text_surface4 = font_object.render(
                '4. Press L to change the level of the game.', False, 'black')
            text_surface5 = font_object.render(
                '5. Press Q to quit the game.', False, 'black')
            text_surface6 = font_object.render(
                "*** Game data are displayed in the game's window title ***", False, 'black')
            self._window._surface.blit(text_surface1, (20, 50))
            self._window._surface.blit(text_surface2, (20, 80))
            self._window._surface.blit(text_surface3, (20, 110))
            self._window._surface.blit(text_surface4, (20, 140))
            self._window._surface.blit(text_surface5, (20, 170))
            self._window._surface.blit(
                text_surface6, (self._window.width/2-text_surface6.get_width()/2, self._window.height-text_surface6.get_height()-10))
            self._window._parent_surface.blit(
                self._window._surface, self._window.position)
        pygame.display.flip()
