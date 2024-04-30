import pygame
import state

class Letter:

    width = 55 # width of letter box
    height = 55 # height of letter box

    # constructor
    def __init__(self, surface:pygame.Surface, x:int, y:int, letter:str, state:state.State):
        self._surface = surface
        self._letter = letter
        self._state = state
        self._x = x
        self._y = y
        self.__draw_default_letter_box()

    # setters
    def set_state(self, state:state.State):
        self._state = state

    def set_letter(self, letter:str):
        self._letter = letter

    # getters
    def get_letter(self):
        return self._letter
    
    def get_state(self):
        return self._state
    
    # draw the default letter box
    def __draw_default_letter_box(self):
        self.set_state(state.State.BACKGROUND.value)
        self.set_letter("")
        pygame.draw.rect(self._surface, self._state, pygame.Rect(self._x, self._y, Letter.width, Letter.height))
        self.set_state(state.State.DEFAULT_LETTER_BOX.value)
        pygame.draw.rect(self._surface, self._state, pygame.Rect(self._x, self._y, Letter.width, Letter.height), 2)
    
    # draw letters (before entering word) into row
    def set_letter_box(self):
        font = pygame.font.Font("assets/ClearSans-Bold.ttf", 30)
        text = font.render(self._letter, True, "#F8F8F8")
        text_rect = text.get_rect()
        text_rect.center = (self._x + Letter.width/2, self._y + Letter.height/2.1)
        self.set_state(state.State.BACKGROUND.value)
        self._surface.blit(text, text_rect)

    # deleting letters 
    def del_letter_box(self):
        self.__draw_default_letter_box() # cover box with default

    # draw letter box after guessed
    def set_guess_box(self):
        font = pygame.font.Font("assets/ClearSans-Bold.ttf", 30)
        text = font.render(self._letter, True, "#F8F8F8")
        text_rect = text.get_rect()
        text_rect.center = (self._x + Letter.width/2, self._y + Letter.height/2.1)
        pygame.draw.rect(self._surface, self._state, pygame.Rect(self._x, self._y, Letter.width, Letter.height))
        self._surface.blit(text, text_rect)