import pygame
from graphic import Graphics

start_game_board = [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0,
         0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1,
         1, 0, 0, 0, -1, -1, -1, 0, 0, 0, 1,
         1, 1, 0, -1, -1, -2, -1, -1, 0, 1, 1,
         1, 0, 0, 0, -1, -1, -1, 0, 0, 0, 1,
         1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
         0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0]  # -2 конунг, -1 защитники, 1 нападающие (attackers)

WIDTH = 736
HEIGHT = 736

screen = pygame.display.set_mode((WIDTH, HEIGHT))
graphics = Graphics(start_game_board)
graphics.init_menu(screen)