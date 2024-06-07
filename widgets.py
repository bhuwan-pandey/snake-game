import pygame
from typing import Literal


class Property():
    def __init__(self) -> None:
        super(Property,self).__init__()
        self.visible=True
        self.enabled=True
        self.position: pygame.Vector2 = pygame.Vector2(0, 0)

class Style():
    def __init__(self) -> None:
        super(Style,self).__init__()
        self.foreground_color = 'black'
        self.background_color = None
        self.vertical_alignment: Literal['top',
                                         'center', 'bottom'] = 'center'
        self.horizontal_alignment: Literal['left',
                                           'center', 'right'] = 'center'

class Text_Style(Style):
    def __init__(self) -> None:
        super(Text_Style,self).__init__()
        self.bold = False
        self.italic = False


class Text(Text_Style,Property):
    def __init__(self) -> None:
        super(Text,self).__init__()
        self.text_caption = 'Text'
        self.font_name = 'Arial'
        self.text_size = 12
        self.font_object: pygame.font.Font = None
        self.surface: pygame.surface.Surface = None

    def __init__(self, text_caption='Text', font_name='Arial', text_size=12, bold=False, italic=False, foreground_color='black', background_color=None, position: pygame.Vector2 = pygame.Vector2(0, 0), vertical_alignment='center', horizontal_alignment='center'):
        super(Text,self).__init__()
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


class Button(Style,Property):
    def __init__(self) -> None:
        super(Button,self).__init__()
        self.width = 100
        self.height = 30
        self.border_width = 2
        self.border_radius = -1
        self.border_top_left_radius = -1
        self.border_top_right_radius = -1
        self.border_bottom_left_radius = -1
        self.border_bottom_right_radius = -1
        self._parent_surface: pygame.surface.Surface = None
        self._text_object: Text = Text()
        self._font_object: pygame.font.Font = pygame.font.SysFont(
            self._text_object.font_name, self._text_object.text_size, self._text_object.bold, self._text_object.italic)
        self._text_surface: pygame.surface.Surface = self._font_object.render(
            self._text_object.font_name, False, self._text_object.foreground_color, self._text_object.background_color)

    def __init__(self, _parent_surface: pygame.surface.Surface, button_text: str):
        super(Button,self).__init__()
        self.width = 100
        self.height = 30
        self.border_width = 2
        self.border_radius = -1
        self.border_top_left_radius = -1
        self.border_top_right_radius = -1
        self.border_bottom_left_radius = -1
        self.border_bottom_right_radius = -1
        self._parent_surface = _parent_surface
        self._text_object: Text = Text()
        self._font_object: pygame.font.Font = pygame.font.SysFont(
            self._text_object.font_name, self._text_object.text_size, self._text_object.bold, self._text_object.italic)
        self._text_surface: pygame.surface.Surface = self._font_object.render(
            button_text, False, self._text_object.foreground_color, self._text_object.background_color)

    def draw(self): 
        if self.visible:
            pygame.draw.rect(self._parent_surface, self.foreground_color, (self.position.x, self.position.y, self.position.x+self.width, self.position.y+self.height),
                             self.border_width, self.border_radius, self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius)
            if self.background_color:
                background_surface=pygame.surface.Surface((self.width-self.border_width*2, self.height-self.border_width*2))
                background_surface.fill(self.background_color)
                self._parent_surface.blit(background_surface,(self.position.x+self.border_width,self.position.y+self.border_width))
            button_position_on_display = pygame.Vector2(
                self.position.x, self.position.y)
            # horizontal alignment
            if self._text_object.horizontal_alignment == 'left':
                button_position_on_display.x = self.position.x+self.border_width
            elif self._text_object.horizontal_alignment == 'center':
                button_position_on_display.x = (
                    (self.position.x+self.width-self.position.x)/2)-self._text_surface.get_width()/2
            elif self._text_object.horizontal_alignment == 'right':
                button_position_on_display.x = self.position.x+self.width - \
                    self._text_surface.get_width()-self.border_width
            # vertical alignment
            if self._text_object.vertical_alignment == 'top':
                button_position_on_display.y = self.position.y+self.border_width
            elif self._text_object.vertical_alignment == 'center':
                button_position_on_display.y = (
                    (self.position.y+self.height-self.position.y)/2)-self._text_surface.get_height()/2
            elif self._text_object.vertical_alignment == 'bottom':
                button_position_on_display.y = self.position.y+self.height - \
                    self._text_surface.get_height()-self.border_width
            self._parent_surface.blit(
                self._text_surface, button_position_on_display)
            pygame.display.flip()
        # return self so that draw can be called upon creating instance and return instance itself to store it
        return self


class Window(Property):
    def __init__(self,parent_surface:pygame.surface.Surface) -> None:
        super().__init__()
        self._surface:pygame.surface.Surface=None
        # self._surface:pygame.surface.Surface=None
        self._parent_surface:pygame.surface.Surface=parent_surface
        self.title='Window'
        self.width=200
        self.height=200
        self.background_color='white'
        self.title_line_color='black'
        self.title_background_color='white'
    
    def draw(self):
        if not self._surface and self._parent_surface:
            self._surface=pygame.surface.Surface((self.width,self.height))
        if self.position.x<=0 and self.position.y<=0:
            self.position.x=self._parent_surface.get_width()/2-self._surface.get_width()/2
            self.position.y=self._parent_surface.get_height()/2-self._surface.get_height()/2
        if self.visible and self._surface:
            self._surface.fill(self.background_color)
            pygame.draw.line(self._surface,self.title_line_color,(self.position.x,self.position.y+20),(self.position.x+self.width,self.position.y+20))
            self._parent_surface.blit(self._surface,self.position)

class Paused_Window():
    def __init__(self,parent_surface:pygame.surface.Surface) -> None:
        # super().__init__()
        self._window:Window=Window(parent_surface)
        self._window.title='Game Paused'
        self.resume_button:Button=None
        
    
    def draw(self):
        if not self._window._surface: # initialize window surface
            self._window.draw()
        if self._window.visible:
            if not self.resume_button: # resume button not initialized
                self.resume_button=Button(self._window._surface,'Resume')
                self.resume_button.background_color='cyan'
            self.resume_button.draw()
            self._window._parent_surface.blit(self._window._surface,self._window.position)
            

            