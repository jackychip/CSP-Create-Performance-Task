import letter
import input
import state
import random
import pygame

class Game:

    # constructor
    def __init__(self, main_surface:pygame.Surface):
        self._main_surface = main_surface

        # draw default letter and input boxes
        self._board = self.__init_letter_boxes()
        self._inputs = self.__init_input_boxes()

        pygame.display.update()

        #tracking variables
        self._current_row = 0
        self._current_col = 0

        #determine random word
        w_list = open("words.txt", "r")
        self._word_list = w_list.read().split("\n")
        self._word = self._word_list[random.randint(0, 5756)]

    # getters
    def get_board(self):
        return self._board
    
    def get_inputs(self):
        return self._inputs

    def get_word(self):
        return self._word

    # appending Letter objects to board[] and drawing default boxes
    def __init_letter_boxes(self):
        board = []

        # starting positions
        x = 101
        y = 100 
        for _ in range(6):
            col = []
            for _ in range(5):
                col.append(letter.Letter(self._main_surface, x, y, "", state.State.DEFAULT_LETTER_BOX.value)) # add Letter object to board
                x += 60
            board.append(col)
            y += 60 
            x = 101

        return board

    # appending Input objects to inputs[] and drawing default boxes
    def __init_input_boxes(self):
        inputs = []

        input_letters = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"] # order of inputs for each row

        # starting positions
        x = 27 
        y = 520

        for i in range(3):
            col = []
            for letter in input_letters[i]:
                col.append(input.Input(self._main_surface, x, y, letter, state.State.DEFAULT_INPUT_BOX.value)) # add Input object to inputs
                x += 45
            inputs.append(col)
            y += 57
            if (i == 0):
                x = 50
            elif (i == 1):
                x = 93

        return inputs

    # add letter to board on current row
    def add_letter(self, letter:str):
        # only accept input if there is space
        if self._current_col > 4:
            return
        
        current_letter_box = self._board[self._current_row][self._current_col] # get Letter object from position on board
        current_letter_box.set_letter(letter) # set letter to draw
        current_letter_box.set_letter_box() # draw letter in box
        self._current_col += 1 # go to next column in the same row
    
    # remove letter from board on current row
    def remove_letter(self):
        # only delete when there are letters on current row
        if self._current_col < 1:
            return
        
        self._board[self._current_row][self._current_col - 1].del_letter_box() # get Letter object at position and delete
        self._current_col -= 1 # go to previous column in the same row

    # evaluates guessed word
    def guess_word(self):
        # form word from letters in row
        word = ""
        for box in self._board[self._current_row]:
            word += box.get_letter()

        # if word is not 5 letters
        if len(word) != 5:
            return;

        # if word isn't a real word
        if word.lower() not in self._word_list:
            return;
    
        # evaluate word
        for i in range(5):
            input_key = self._find_input(word[i])

            # if letter is in the right column
            if self._word[i].upper() == word[i]:
                # change box colour to green
                colour = state.State.GREEN_LETTER_BOX.value
                self._board[self._current_row][i].set_state(colour)
                input_key.set_state(colour)

            # if letter exists in word but isn't in right column
            elif word[i] in self._word.upper() and self._determine_yellow(i, word, self._word.upper()):
                # change box colour to yellow
                colour = state.State.YELLOW_LETTER_BOX.value
                self._board[self._current_row][i].set_state(colour)

                # only change input box colour if input is unused and not already right (green)
                if input_key.get_state() != state.State.GREY_INPUT_BOX.value and input_key.get_state() != state.State.GREEN_INPUT_BOX.value:
                    input_key.set_state(colour)

            #if letter doesn't exist in word
            else:
                # set box colour to grey
                colour = state.State.GREY_LETTER_BOX.value
                self._board[self._current_row][i].set_state(colour)

                #only change input box colour when letter was never used
                if input_key.get_state() == state.State.DEFAULT_INPUT_BOX.value:
                    input_key.set_state(colour)
            
            # draw updated versions of input and letter boxes
            self._board[self._current_row][i].set_guess_box()
            input_key.draw_input_box()
            pygame.display.update()

        # word is the correct word (end game)
        if word == self._word.upper():
            return 1
        
        #ran out of guesses
        if self._current_row == 5:
            return -1

        # reset trackers
        self._current_col = 0
        self._current_row += 1

        return 0

    # updates score text
    def update_score(self, score):
        # blits text of the score
        font = pygame.font.Font("assets/ClearSans-Bold.ttf", 35)
        text = font.render(str(score), True, "#F8F8F8")
        text_rect = text.get_rect()
        text_rect.center = (248, 45)
        self._main_surface.blit(text, text_rect)

    # finds and returns the Input object for a letter
    def _find_input(self, letter):
        for i in range(3):
            for j in range(len(self._inputs[i])):
                if letter.upper() == self._inputs[i][j].get_letter():
                    return self._inputs[i][j]
                
        return None
    
    # determines whether a letter is yellow; handles edge cases (repeated letters, duplicate yellows)
    def _determine_yellow(self, index, guessed_word, actual_word):
        letter = guessed_word[index]
        g_word = guessed_word
        a_word = actual_word

        # replace letters in the correct column with empty string
        for i in range(5):
            if g_word[i] == letter and a_word[i] == letter:
                g_word = g_word[0:i] + " " + g_word[i + 1:]
                a_word = a_word[0:i] + " " + a_word[i + 1:]

        # replace nearest matching letters in guessed_word and actual_word with empty string
        for idx in range(5):
            for pointer in range(5):
                if g_word[idx] == letter and a_word[pointer] == letter:
                    g_word = g_word[0:idx] + " " + g_word[idx + 1:]
                    a_word = a_word[0:pointer] + " " + a_word[pointer + 1:]

        # return if letter at index is empty (empty string indicates that letter exists in word and matches to another letter in actual word)
        return g_word[index] == " "