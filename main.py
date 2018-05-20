
import pygame,sys

from pygame.locals import *

from player import Player
from utils import get_switched_player

pygame.init()

game_res = (500,240)

DISPLAYSURF = pygame.display.set_mode(game_res, 0 , 32)

pygame.display.set_caption("GAMBLE tic tac toe")

game_board = pygame.image.load('board.png')

bet_input = pygame.Rect(420, 80, 50, 18)
bet_input_state = False
bet_input_number = ""
DISPLAYSURF.blit(game_board,(0,0))
#DISPLAYSURF.blit(bet_input)


player_1 = Player('player 1')
player_2 = Player('player 2')
curr_player = player_1



color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 12)

lock_button = pygame.Rect(380,150, 80, 30)
lock_button_color = pygame.Color('lightskyblue3')


while True:
    DISPLAYSURF.blit(game_board, (0, 0))
    for event in pygame.event.get():
        if event.type ==QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if bet_input.collidepoint(event.pos):
                # Toggle the active variable.
                bet_input_state = not bet_input_state
            else:
                bet_input_state = False

            if lock_button.collidepoint(event.pos):
                curr_player.bet_coins(int(bet_input_number))
                curr_player = get_switched_player(curr_player, player_1, player_2)

            color = color_active if bet_input_state else color_inactive
        if event.type == pygame.KEYDOWN:
            if bet_input_state:
                if event.key == pygame.K_RETURN:
                    print(bet_input_number)
                    bet_input_number = ''
                elif event.key == pygame.K_BACKSPACE:
                    bet_input_number = bet_input_number[:-1]
                elif event.key in range(48,57):
                    bet_input_number += event.unicode

        if bet_input_number and int(bet_input_number) <= int(curr_player.get_coins_left()):
            lock_color_code = (0,0,0)
            lock_button_color = pygame.Color('dodgerblue2')
        else:
            lock_color_code = (0,100,100)
            lock_button_color = pygame.Color('lightskyblue3')
    curr_player_text = myfont.render(curr_player.name + " is betting", False, (0, 0, 0))
    coins_left = myfont.render(curr_player.get_coins_left(), False, (0, 0, 0))
    DISPLAYSURF.blit(coins_left, (420, 43))
    DISPLAYSURF.blit(curr_player_text, (300,0))
    lock_button_text = myfont.render("Lock Bet", False, lock_color_code)
    bet_input_number_text = myfont.render(bet_input_number, False, (0, 0, 0))
    DISPLAYSURF.blit(bet_input_number_text,(420, 80))
    pygame.draw.rect(DISPLAYSURF,  color, bet_input, 2)
    pygame.draw.rect(DISPLAYSURF, lock_button_color, lock_button,2 )
    DISPLAYSURF.blit(lock_button_text, (395,155))
    pygame.display.update()
