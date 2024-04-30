import pygame
import game

pygame.init()

# constants
WIDTH = 500 
HEIGHT = 700

# create display and background
main_surface = pygame.display.set_mode((WIDTH, HEIGHT))
main_surface.fill("#121213")

# set icon, caption, and update display
wordle_icon = pygame.image.load("assets/logo.png")
pygame.display.set_caption("Wordle")
pygame.display.set_icon(wordle_icon)

# main function
def main():

    # initialize game handler
    game_handler = game.Game(main_surface)

    # add score text and set score to 0
    score = 0
    game_handler.update_score(score)

    # start game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit program when exiting window
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN: # if a key is pressed
                if event.key == pygame.K_RETURN:
                    if game_handler.guess_word() == 1: # correct word is entered
                        pygame.time.wait(500)
                        score += 1 # add to score

                        #reset board/screen and update text
                        main_surface.fill("#121213")
                        game_handler = game.Game(main_surface)
                        game_handler.update_score(score)

                    elif game_handler.guess_word() == -1: # ran out of guesses
                        pygame.time.wait(500)
                        score = 0 # reset score

                        #reset board/screen and update text
                        main_surface.fill("#121213")
                        game_handler = game.Game(main_surface)
                        game_handler.update_score(score)

                elif event.key == pygame.K_BACKSPACE:
                    game_handler.remove_letter() # remove letter from current row on board
                else:
                    if event.unicode != "" and event.unicode.upper() in "QWERTYUIOPASDFGHJKLZXCVBNM": # if key is pressed is in the alphabet
                        game_handler.add_letter(event.unicode.upper()) # add letter to current row on board

        pygame.display.update() # update all changes to the display

main()