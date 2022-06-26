import pygame
import pygame_menu
from asyncio.windows_events import NULL
from tkinter import X
from turtle import back, pos
from xmlrpc.client import Boolean

import tafl_logic

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



class Graphics:
    def __init__(self, start_game_board):
        pygame.init()
        #pygame.mixer.init()
        self.board = start_game_board.copy()
        self.__background = pygame.image.load('board.jpg')
        self.all_sprites = self.init_sprites()
        self.clock = pygame.time.Clock()

    def __main_loop(self, screen):
        logic = tafl_logic.Logic(self.board, BOARD_WH, BOARD_POS, SQUARE_WH)
        selected_figure = None
        isAttackersMove = True
        running = True
        is_mouse_pressed = False
        while running:
            self.clock.tick(FPS) #контроль FPS
            self.all_sprites.update()
            screen.blit(self.__background, (0, 0))
            last_mouse_pos = pygame.mouse.get_pos()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    for sprite in self.all_sprites:
                        if sprite.rect.collidepoint(e.pos):
                            selected_figure = sprite
                            is_mouse_pressed = True
                            break
                elif e.type == pygame.MOUSEBUTTONUP and selected_figure is not None:
                    is_mouse_pressed = False
                    if not ((selected_figure.rank == 1 and isAttackersMove) or (selected_figure.rank == -1 and not isAttackersMove) or (selected_figure.rank == -2 and not isAttackersMove)):
                        break
                    position = logic.move_figure(e.pos, selected_figure)
                    if position[0] == selected_figure.rect.x and position[1] == selected_figure.rect.y:
                        selected_figure = None
                        break
                    else:
                        selected_figure.rect.x = position[0]
                        selected_figure.rect.y = position[1]
                        result = logic.control_figures(selected_figure, self.all_sprites)
                        selected_figure = None
                        isAttackersMove = not isAttackersMove
                        if result == 1:
                            self.__end_message('attackers lose!', screen)
                            running = False
                        elif result == 2:
                            self.__end_message('attackers win!', screen)
                            running = False
                        break
            # if is_mouse_pressed:
            #     print(pygame.mouse.get_pos())
            #     sprite= selected_figure
            #     sprite.rect.x = sprite.rect.x + (pygame.mouse.get_pos()[0] - last_mouse_pos[0])
            #     sprite.rect.y = sprite.rect.y + (pygame.mouse.get_pos()[1] - last_mouse_pos[1])
            self.all_sprites.draw(screen)
            pygame.display.flip()

    def __end_message(self, message, screen):
        self.board = start_game_board.copy()
        self.all_sprites = self.init_sprites()
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
            font = pygame.font.SysFont('Comic Sans MS', 40)
            text_end_game = font.render(message, True, (255, 0, 0))
            screen.blit(text_end_game, (0, HEIGHT - 50))
            pygame.display.flip()
    
    def init_menu(self, screen):
        menu = pygame_menu.Menu('Tafl', WIDTH, HEIGHT,
                                theme=pygame_menu.themes.THEME_BLUE)
        #menu.add.text_input('Name :', default='Noname')
        menu.add.button('Play', self.__main_loop, (screen))
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(screen)
        pygame.quit()
    
    def init_sprites(self):
        all_sprites = pygame.sprite.Group()
        for i in range(0, len(self.board)):
            if self.board[i] != 0:
                figure = Figure()
                figure.rect.x = (i % BOARD_WH) * SQUARE_WH + BOARD_POS
                figure.rect.y = int(i / BOARD_WH) * SQUARE_WH + BOARD_POS
                if self.board[i] == -1:
                    figure.image.fill(BLACK)
                    figure.rank = -1
                elif self.board[i] == -2:
                    figure.image.fill(RED)
                    figure.rank = -2
                all_sprites.add(figure)
        return all_sprites


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



screen = pygame.display.set_mode((WIDTH, HEIGHT))
graphics = Graphics(start_game_board)
graphics.init_menu(screen)