import letter
import input
import state
import random
import pygame

class Game:

    def __init__(self, main_surface:pygame.Surface):
        self._main_surface = main_surface
        self._board = self.__init_letter_boxes()
        self._inputs = self.__init_input_boxes()

        pygame.display.update()

        #tracking variables
        self._current_row = 0
        self._current_col = 0

        #determine word
        w_list = open("words.txt", "r")
        self._word_list = w_list.read().split("\n")
        self._word = "twine"
        self._word_list[random.randint(0, 2309)]

        # print(self._word)

    #getter methods
    def get_board(self):
        return self._board
    
    def get_inputs(self):
        return self._inputs

    def get_word(self):
        return self._word

    #init functions
    def __init_letter_boxes(self):
        board = []

        x = 101
        y = 77
        for _ in range(6):
            col = []
            for _ in range(5):
                col.append(letter.Letter(self._main_surface, x, y, "", state.State.DEFAULT_LETTER_BOX.value))
                x += 60
            board.append(col)
            y += 60
            x = 101

        return board

    def __init_input_boxes(self):
        inputs = []

        input_letters = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

        x = 27
        y = 520

        for i in range(3):
            col = []
            for letter in input_letters[i]:
                col.append(input.Input(self._main_surface, x, y, letter, state.State.DEFAULT_INPUT_BOX.value))
                x += 45
            inputs.append(col)
            y += 57
            if (i == 0):
                x = 50
            elif (i == 1):
                x = 93

        return inputs

    #game methods
    def add_letter(self, letter:str):
        if self._current_col > 4:
            return
        
        current_letter_box = self._board[self._current_row][self._current_col]
        current_letter_box.set_letter(letter)
        current_letter_box.set_letter_box()
        self._current_col += 1
    
    def remove_letter(self):
        if self._current_col < 1:
            return
        
        self._board[self._current_row][self._current_col - 1].del_letter_box()
        self._current_col -= 1

    def guess_word(self):
        word = ""
        for box in self._board[self._current_row]:
            word += box.get_letter()

        if len(word) != 5:
            return;
    
        if word.lower() not in self._word_list:
            return;
    
        #evaluate word
        for i in range(5):
            input_key = self._find_input(word[i])

            if self._word[i].upper() == word[i]:
                colour = state.State.GREEN_LETTER_BOX.value
                self._board[self._current_row][i].set_state(colour)
                input_key.set_state(colour)

            elif word[i] in self._word.upper() and self._determine_yellow(i, word, self._word.upper()):
                colour = state.State.YELLOW_LETTER_BOX.value
                self._board[self._current_row][i].set_state(colour)
                if input_key.get_state() == state.State.DEFAULT_INPUT_BOX.value or state.State.GREY_INPUT_BOX:
                    input_key.set_state(colour)

            else:
                colour = state.State.GREY_LETTER_BOX.value
                self._board[self._current_row][i].set_state(colour)
                if input_key.get_state() == state.State.DEFAULT_INPUT_BOX.value:
                    input_key.set_state(colour)
            
            self._board[self._current_row][i].set_guess_box()
            input_key.draw_input_box()
            pygame.display.update()

        if word == self._word.upper():
            return 1
        
        if self._current_row == 5:
            return -1

        self._current_col = 0
        self._current_row += 1

        return 0

    #helper methods
    def _find_input(self, letter):
        for i in range(3):
            for j in range(len(self._inputs[i])):
                if letter.upper() == self._inputs[i][j].get_letter():
                    return self._inputs[i][j]
                
        return None
    
    def _determine_yellow(self, index, guessed_word, actual_word):
        letter = guessed_word[index]
        g_word = guessed_word
        a_word = actual_word

        for i in range(5):
            if g_word[i] == letter and a_word[i] == letter:
                g_word = g_word[0:i] + " " + g_word[i + 1:]
                a_word = a_word[0:i] + " " + a_word[i + 1:]

        pointer = 0
        for idx in range(5):
            for pointer in range(5):
                if g_word[idx] == letter and a_word[pointer] == letter:
                    g_word = g_word[0:idx] + " " + g_word[idx + 1:]
                    a_word = a_word[0:pointer] + " " + a_word[pointer + 1:]

        return g_word[index] == " "