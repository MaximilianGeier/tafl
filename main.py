from asyncio.windows_events import NULL
from turtle import back, pos
from xmlrpc.client import Boolean
import pygame
import random

board = [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0,
         0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1,
         1, 0, 0, 0, -1, -1, -1, 0, 0, 0, 1,
         1, 1, 0, -1, -1, -2, -1, -1, 0, 1, 1,
         1, 0, 0, 0, -1, -1, -1, 0, 0, 0, 1,
         1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
         0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0] # -2 конунг, -1 защитники, 1 нападающие (attackers)

BOARD_WH = 11
BOARD_POS = 64
SQUARE_WH = 55 #56.5

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 736
HEIGHT = 736
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
background = pygame.image.load('board.jpg')

all_sprites = pygame.sprite.Group() #структура для хранения всех спрайтов

class Figure(pygame.sprite.Sprite):
    rank = 1
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        pass

for i in range(0, len(board)):
    if board[i] != 0:
        figure = Figure()
        figure.rect.x = (i % BOARD_WH) * SQUARE_WH + BOARD_POS
        figure.rect.y = int(i / BOARD_WH) * SQUARE_WH + BOARD_POS
        if board[i] == -1:
            figure.image.fill(BLACK)
            figure.rank = -1
        elif board[i] == -2:
            figure.image.fill(RED)
            figure.rank = -2
        all_sprites.add(figure)


def get_square_number(pos):
    x = int((pos[0] - BOARD_POS) / SQUARE_WH)
    y = int((pos[1] - BOARD_POS) / SQUARE_WH)
    if pos[0] < 58 or pos[1] < BOARD_POS or x >= BOARD_WH or y >= BOARD_WH:
        return (None, None)
    return (x, y)

def move_figure(mouse_pos, figure):
    figure_pos = (sprite.rect[0], sprite.rect[1])
    x, y = figure_pos[0], figure_pos[1]
    square_pos = get_square_number(mouse_pos)
    square_with_figure_pos = get_square_number(figure_pos)
    if square_pos == None or square_with_figure_pos == None:
        return (x, y)
    if square_pos[0] == square_with_figure_pos[0] or square_pos[1] == square_with_figure_pos[1]:
        flag = True
        direction = 1
        if square_pos[0] > square_with_figure_pos[0]:
            direction = -1
        for i in range(square_pos[0], square_with_figure_pos[0], direction):
            if board[square_with_figure_pos[1] * BOARD_WH + i] != 0:
                flag = False
        if square_pos[1] > square_with_figure_pos[1]:
            direction = -1
        for i in range(square_pos[1], square_with_figure_pos[1], direction):
            if board[i * BOARD_WH + square_with_figure_pos[0]] != 0:
                flag = False
        if flag:
            x = BOARD_POS + (SQUARE_WH * square_pos[0])
            y = BOARD_POS + (SQUARE_WH * square_pos[1])
            board[square_with_figure_pos[1] * BOARD_WH + square_with_figure_pos[0]] = 0
            board[square_pos[1] * BOARD_WH + square_pos[0]] = figure.rank
    return (x, y) 

running = True
selected_figure = None
isAttackersMove = True

while running: #main loop
    clock.tick(FPS) #контроль FPS
    all_sprites.update()
    screen.blit(background, (0, 0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            for sprite in all_sprites:
                if sprite.rect.collidepoint(e.pos):
                    selected_figure = sprite
                    print(selected_figure)
        elif e.type == pygame.MOUSEBUTTONUP and selected_figure is not None:
            for sprite in all_sprites:
                if sprite == selected_figure:
                    if not ((sprite.rank == 1 and isAttackersMove) or (sprite.rank == -1 and not isAttackersMove) or (sprite.rank == -2 and not isAttackersMove)):
                        break
                    position = move_figure(e.pos, sprite)
                    if position[0] == sprite.rect.x and position[1] == sprite.rect.y:
                        selected_figure = None
                        break
                    else:
                        sprite.rect.x = position[0]
                        sprite.rect.y = position[1]
                        selected_figure = None
                        isAttackersMove = not isAttackersMove
                        break
    all_sprites.draw(screen)
    pygame.display.flip() #двойная буферезация

pygame.quit()