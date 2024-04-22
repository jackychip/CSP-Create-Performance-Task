'''
TO-DO:
- implement winner and loser screens
- implement replay feature
- implement error messages (e.g. word not in list)
- fix bug where letters already green will show up as yellow in separate space
'''

import pygame
import game

pygame.init()

# constants
WIDTH = 500 
HEIGHT = 700

#create display and backgroun
main_surface = pygame.display.set_mode((WIDTH, HEIGHT))
main_surface.fill("#121213")

#set icon, caption, and update display
wordle_icon = pygame.image.load("assets/logo.png")
pygame.display.set_caption("Wordle")
pygame.display.set_icon(wordle_icon)

#initialize game handler
game_handler = game.Game(main_surface)

#start game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_handler.guess_word() == 1:
                    print("you won")
                    break
                elif game_handler.guess_word() == -1:
                    print("you lost")
                    print(game_handler.get_word())
                    break
            elif event.key == pygame.K_BACKSPACE:
                game_handler.remove_letter()
            else:
                if event.unicode != "" and event.unicode.upper() in "QWERTYUIOPASDFGHJKLZXCVBNM":
                    game_handler.add_letter(event.unicode.upper())

    pygame.display.update()