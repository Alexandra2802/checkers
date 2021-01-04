import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):

        if self.board.winner()==WHITE:
            winner='White'
        elif self.board.winner()==RED:
            winner='Red'
        else:
            winner=None
        return winner


    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:#s-a selectat un patrat care nu e gol
            # si linia si coloana la care se va feca mutarea e valida
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)] #piesa peste care s-a sarit
            if skipped:
                self.board.remove(skipped) #se elimina piesa peste care s-a sarit
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        '''
        Marcheaza toate mutarile pe care piesa selectata le poate face
        :param moves: mutarile valide
        :return:
        '''
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED