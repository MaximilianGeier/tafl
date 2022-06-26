BOARD_WH = 0
BOARD_POS = 0
SQUARE_WH = 0

class Logic:
    def __init__(self, board, board_wh, board_pos, square_wh):
        self.board = board
        global BOARD_WH
        BOARD_WH = board_wh
        global BOARD_POS
        BOARD_POS = board_pos
        global SQUARE_WH
        SQUARE_WH = square_wh

    def set_board(self, board):
        self.board = board

    def remove_figure_with_pos(self, pos, all_sprites):
        for figure in all_sprites:
            figure_pos = self.get_square_number((figure.rect.x, figure.rect.y))
            if figure_pos[0] == pos[0] and figure_pos[1] == pos[1] and figure.rank != -2:
                all_sprites.remove(figure)
                self.board[pos[1] * BOARD_WH + pos[0]] = 0
                return 0
        return -1

    def control_figures(self, figure, all_sprites):
        figure_pos = self.get_square_number((figure.rect.x, figure.rect.y))
        if figure.rank == -2:
            if (figure_pos[0], figure_pos[1]) == (0, 0) or (figure_pos[0], figure_pos[1]) == (BOARD_WH - 1, BOARD_WH - 1) or \
                (figure_pos[0], figure_pos[1]) == (0, BOARD_WH - 1) or (figure_pos[0], figure_pos[1]) == (BOARD_WH - 1, 0):
                return 1 #attackers lose
        else:
            for index in range(0, BOARD_POS):
                if self.board[index] == -2:
                    king_x = index % BOARD_WH
                    king_y = index // BOARD_WH
                    if king_x > 0 and king_y > 0 and king_x < BOARD_WH - 1 and king_y < BOARD_WH - 1:
                        if (self.board[(king_y - 1) * BOARD_WH + king_x] == 1 or (king_x * 2 + 1 == BOARD_WH and (king_y - 1) * 2 + 1 == BOARD_WH)) \
                            and (self.board[(king_y + 1) * BOARD_WH + king_x] == 1 or (king_x * 2 + 1 == BOARD_WH and (king_y + 1) * 2 + 1 == BOARD_WH)) \
                            and (self.board[king_y * BOARD_WH + (king_x - 1)] == 1 or ((king_x - 1) * 2 + 1 == BOARD_WH and king_y * 2 + 1 == BOARD_WH)) \
                            and (self.board[king_y * BOARD_WH + (king_x + 1)] == 1 or ((king_x + 1) * 2 + 1 == BOARD_WH and king_y * 2 + 1 == BOARD_WH)):
                            return 2 #attackers win
        if figure.rank < 0:
            if figure_pos[0] > 1 and self.board[figure_pos[1] * BOARD_WH + (figure_pos[0] - 2)] < 0 \
                and self.board[figure_pos[1] * BOARD_WH + (figure_pos[0] - 1)] > 0:
                self.remove_figure_with_pos((figure_pos[0] - 1, figure_pos[1]), all_sprites)
            if figure_pos[1] > 1 and self.board[(figure_pos[1] - 2) * BOARD_WH + figure_pos[0]] < 0 \
                and self.board[(figure_pos[1] - 1) * BOARD_WH + figure_pos[0]] > 0:
                self.remove_figure_with_pos((figure_pos[0], figure_pos[1] - 1), all_sprites)
            if figure_pos[0] < BOARD_WH - 2 and self.board[figure_pos[1] * BOARD_WH + (figure_pos[0] + 2)] < 0 \
                and self.board[figure_pos[1] * BOARD_WH + (figure_pos[0] + 1)] > 0:
                self.remove_figure_with_pos((figure_pos[0] + 1, figure_pos[1]))
            if figure_pos[1] < BOARD_WH - 2 and self.board[(figure_pos[1] + 2) * BOARD_WH + figure_pos[0]] < 0 \
                and self.board[(figure_pos[1] + 1) * BOARD_WH + figure_pos[0]] > 0:
                self.remove_figure_with_pos((figure_pos[0], figure_pos[1] + 1), all_sprites)
        else:
            if figure_pos[0] > 1 and self.board[figure_pos[1] * BOARD_WH + (figure_pos[0] - 2)] > 0 \
                and self.board[figure_pos[1] * BOARD_WH + (figure_pos[0] - 1)] < 0:
                self.remove_figure_with_pos((figure_pos[0] - 1, figure_pos[1]), all_sprites)
            if figure_pos[1] > 1 and self.board[(figure_pos[1] - 2) * BOARD_WH + figure_pos[0]] > 0 \
                and self.board[(figure_pos[1] - 1) * BOARD_WH + figure_pos[0]] < 0:
                self.remove_figure_with_pos((figure_pos[0], figure_pos[1] - 1), all_sprites)
            if figure_pos[0] < BOARD_WH - 2 and self.board[figure_pos[1] * BOARD_WH + (figure_pos[0] + 2)] > 0 \
                and self.board[figure_pos[1] * BOARD_WH + (figure_pos[0] + 1)] < 0:
                self.remove_figure_with_pos((figure_pos[0] + 1, figure_pos[1]), all_sprites)
            if figure_pos[1] < BOARD_WH - 2 and self.board[(figure_pos[1] + 2) * BOARD_WH + figure_pos[0]] > 0 \
                and self.board[(figure_pos[1] + 1) * BOARD_WH + figure_pos[0]] < 0:
                self.remove_figure_with_pos((figure_pos[0], figure_pos[1] + 1), all_sprites)
        if figure.rank < 0:
            if figure_pos[0] > 1 and ((figure_pos[1] * 2 + 1) == BOARD_WH and ((figure_pos[0] - 2) * 2 + 1) == BOARD_WH \
                or (figure_pos[0] - 2 == 0 and figure_pos[1] == 0) or (figure_pos[0] - 2 == 0 and figure_pos[1] == BOARD_WH - 1)) \
                and self.board[figure_pos[1] * BOARD_WH + (figure_pos[0] - 1)] > 0:
                self.remove_figure_with_pos((figure_pos[0] - 1, figure_pos[1]), all_sprites)
            if figure_pos[1] > 1 and (((figure_pos[1] - 2) * 2 + 1) == BOARD_WH and (figure_pos[0] * 2 + 1) == BOARD_WH \
                or (figure_pos[0] == 0 and figure_pos[1] - 2 == 0) or (figure_pos[0] == BOARD_WH - 1 and figure_pos[1] - 2 == 0)) \
                and self.board[(figure_pos[1] - 1) * BOARD_WH + figure_pos[0]] > 0:
                self.remove_figure_with_pos((figure_pos[0], figure_pos[1] - 1), all_sprites)
            if figure_pos[0] < BOARD_WH - 2 and ((figure_pos[1] * 2 + 1) == BOARD_WH and ((figure_pos[0] + 2) * 2 + 1) == BOARD_WH \
                or (figure_pos[0] + 2 == BOARD_WH - 1 and figure_pos[1] == 0) or (figure_pos[0] + 2 == BOARD_WH - 1 and figure_pos[1] == BOARD_WH - 1)) \
                and self.board[figure_pos[1] * BOARD_WH + (figure_pos[0] + 1)] > 0:
                self.remove_figure_with_pos((figure_pos[0] + 1, figure_pos[1]), all_sprites)
            if figure_pos[1] < BOARD_WH - 2 and (((figure_pos[1] + 2) * 2 + 1) == BOARD_WH and (figure_pos[0] * 2 + 1) == BOARD_WH \
                or (figure_pos[0] == 0 and figure_pos[1] + 2 == BOARD_WH - 1) or (figure_pos[0] == BOARD_WH - 1 and figure_pos[1] + 2 == BOARD_WH - 1)) \
                and self.board[(figure_pos[1] + 1) * BOARD_WH + figure_pos[0]] > 0:
                self.remove_figure_with_pos((figure_pos[0], figure_pos[1] + 1), all_sprites)
        else:
            if figure_pos[0] > 1 and ((figure_pos[1] * 2 + 1) == BOARD_WH and ((figure_pos[0] - 2) * 2 + 1) == BOARD_WH \
                or (figure_pos[0] - 2 == 0 and figure_pos[1] == 0) or (figure_pos[0] - 2 == 0 and figure_pos[1] == BOARD_WH - 1)) \
                and self.board[figure_pos[1] * BOARD_WH + (figure_pos[0] - 1)] < 0:
                self.remove_figure_with_pos((figure_pos[0] - 1, figure_pos[1]), all_sprites)
            if figure_pos[1] > 1 and (((figure_pos[1] - 2) * 2 + 1) == BOARD_WH and (figure_pos[0] * 2 + 1) == BOARD_WH \
                or (figure_pos[0] == 0 and figure_pos[1] - 2 == 0) or (figure_pos[0] == BOARD_WH - 1 and figure_pos[1] - 2 == 0)) \
                and self.board[(figure_pos[1] - 1) * BOARD_WH + figure_pos[0]] < 0:
                self.remove_figure_with_pos((figure_pos[0], figure_pos[1] - 1), all_sprites)
            if figure_pos[0] < BOARD_WH - 2 and ((figure_pos[1] * 2 + 1) == BOARD_WH and ((figure_pos[0] + 2) * 2 + 1) == BOARD_WH \
                or (figure_pos[0] + 2 == BOARD_WH - 1 and figure_pos[1] == 0) or (figure_pos[0] + 2 == BOARD_WH - 1 and figure_pos[1] == BOARD_WH - 1)) \
                and self.board[figure_pos[1] * BOARD_WH + (figure_pos[0] + 1)] < 0:
                self.remove_figure_with_pos((figure_pos[0] + 1, figure_pos[1]), all_sprites)
            if figure_pos[1] < BOARD_WH - 2 and (((figure_pos[1] + 2) * 2 + 1) == BOARD_WH and (figure_pos[0] * 2 + 1) == BOARD_WH \
                or (figure_pos[0] == 0 and figure_pos[1] + 2 == BOARD_WH - 1) or (figure_pos[0] == BOARD_WH - 1 and figure_pos[1] + 2 == BOARD_WH - 1)) \
                and self.board[(figure_pos[1] + 1) * BOARD_WH + figure_pos[0]] < 0:
                self.remove_figure_with_pos((figure_pos[0], figure_pos[1] + 1), all_sprites)
        return 0

    def move_figure(self, mouse_pos, figure):
        figure_pos = (figure.rect[0], figure.rect[1])
        x, y = figure_pos[0], figure_pos[1]
        square_pos = self.get_square_number(mouse_pos)
        square_with_figure_pos = self.get_square_number(figure_pos)
        if square_pos == None or square_with_figure_pos == None:
            return (x, y)
        elif (square_pos[0] == 0 and square_pos[1] == 0) or (square_pos[0] == BOARD_WH - 1 and square_pos[1] == BOARD_WH - 1) \
        or (square_pos[0] == 0 and square_pos[1] == BOARD_WH - 1) or (square_pos[0] == BOARD_WH - 1 and square_pos[1] == 0):
            if figure.rank != -2:
                return (x, y)
        elif square_pos[0] == BOARD_WH // 2 and square_pos[1] == BOARD_WH // 2:
            return (x, y)
        if square_pos[0] == square_with_figure_pos[0] or square_pos[1] == square_with_figure_pos[1]:
            flag = True
            direction = 1
            if square_pos[0] > square_with_figure_pos[0]:
                direction = -1
            for i in range(square_pos[0], square_with_figure_pos[0], direction):
                if self.board[square_with_figure_pos[1] * BOARD_WH + i] != 0:
                    flag = False
            if square_pos[1] > square_with_figure_pos[1]:
                direction = -1
            for i in range(square_pos[1], square_with_figure_pos[1], direction):
                if self.board[i * BOARD_WH + square_with_figure_pos[0]] != 0:
                    flag = False
            if flag:
                x = BOARD_POS + (SQUARE_WH * square_pos[0])
                y = BOARD_POS + (SQUARE_WH * square_pos[1])
                self.board[square_with_figure_pos[1] * BOARD_WH + square_with_figure_pos[0]] = 0
                self.board[square_pos[1] * BOARD_WH + square_pos[0]] = figure.rank
        return (x, y)

    def get_square_number(self, pos):
        x = int((pos[0] - BOARD_POS) / SQUARE_WH)
        y = int((pos[1] - BOARD_POS) / SQUARE_WH)
        if pos[0] < 58 or pos[1] < BOARD_POS or x >= BOARD_WH or y >= BOARD_WH:
            return (None, None)
        return (x, y)