import pygame
import sys
from additional_functions.board import Board, Usual, Queen


def load_board(data):
    data = data.split('%')
    board = Board(8, 8)
    test_group = pygame.sprite.Group()
    for i in range(len(board.field)):
        string = board.field[i]
        for j in range(len(string)):
            if data[i][j] == '.':
                board.field[i][j] = None
            elif data[i][j] == 'w':
                board.field[i][j] = Usual(test_group, 'white')
            elif data[i][j] == 'b':
                board.field[i][j] = Usual(test_group, 'black')
            elif data[i][j] == 'W':
                board.field[i][j] = Queen(test_group, 'white')
            elif data[i][j] == 'B':
                board.field[i][j] = Queen(test_group, 'black')
    return board


def send_board(board):
    data = []
    for i in range(len(board.field)):
        string = []
        for j in range(len(board.field[0])):
            if board.field[i][j] is None:
                string.append('.')
            elif isinstance(board.field[i][j], Usual):
                if board.field[i][j].color == 'white':
                    string.append('w')
                elif board.field[i][j].color == 'black':
                    string.append('b')
            elif isinstance(board.field[i][j], Queen):
                if board.field[i][j].color == 'white':
                    string.append('W')
                elif board.field[i][j].color == 'black':
                    string.append('B')
        data.append(''.join(string))
    return '%'.join(data)
