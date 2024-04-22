import pygame
import state

class Input:

    width = 40
    height = 50

    def __init__(self, surface:pygame.Surface, x:int, y:int, letter:str, state:state.State):
        self._surface = surface
        self._letter = letter
        self._state = state
        self._x = x
        self._y = y
        self.draw_input_box()

    def set_state(self, state:state.State):
        self._state = state
    
    def get_letter(self):
        return self._letter

    def draw_input_box(self):
        font = pygame.font.Font("assets/ClearSans-Bold.ttf", 20)
        pygame.draw.rect(self._surface, self._state, pygame.Rect(self._x, self._y, Input.width, Input.height), border_radius=3)
        text = font.render(self._letter, True, "#F8F8F8")
        text_rect = text.get_rect()
        text_rect.center = (self._x + Input.width/2, self._y + Input.height/2)
        self._surface.blit(text, text_rect)
