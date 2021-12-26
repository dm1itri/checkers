import socket
from _thread import *

import pygame.sprite

from additional_functions.board import Board, Usual
from additional_functions.board import load_board, send_board

server = '192.168.0.3'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print('Waiting for a connection, Server Started')

WHITE = 'white'
BLACK = 'black'
COLOR = WHITE
main_board = Board(8, 8)
main_board.set_view(50, 50, 50)
all_sprites = pygame.sprite.Group()


def threaded_client(conn):
    global COLOR, WHITE, BLACK, main_board
    conn.send(send_board(main_board).encode())
    reply = ''
    while True:
        print('hi')
        try:
            print('перед data')
            data = conn.recv(2048).decode()
            print('после data', data)
            if not data:
                print('Disconnected')
                break
            else:
                if data == 'RECEIVE':
                    conn.sendall(send_board(main_board).encode())
                    print('RECIEVE main board')
                    continue
                else:

                    board = load_board(data, main_board, all_sprites)
                    reply = board
                    print('Received: ', reply)
                    print('.... changing reply ....')
                    main_board = change_board(board, COLOR)
                    print('Sending: ', send_board(main_board))
                    COLOR = WHITE if COLOR == BLACK else BLACK

            conn.sendall(send_board(main_board).encode())
        except Exception as e:
            print(e, 'ОШИБКА')
            break

    print('Lost connection')
    conn.close()


def change_board(board: Board, color):
    for i in range(len(board.field)):
        string = board.field[i]
        for j in range(len(string)):
            if string[j] != main_board.field[i][j]:
                if string[j] is not None and string[j].color == color:
                    print('че то есть')
                    main_board.field[i][j] = string[j]
                elif string[j] is None and main_board.field[i][j].color == color:
                    print('реал')
                    main_board.field[i][j] = string[j]
    return main_board


currentPlayer = 0
while True:
    print('okey')
    conn, addr = s.accept()
    print('Connected to:', addr)

    start_new_thread(threaded_client, (conn,))
    currentPlayer += 1
