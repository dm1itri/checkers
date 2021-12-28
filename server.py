import socket
from _thread import *

import pygame.sprite

from additional_functions.board import Board, Usual
from additional_functions.board import load_board, send_board
from additional_functions.server.online_game import OnlineGame

server = '192.168.0.3'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print('Waiting for a connection, Server Started')

connected = set()
games = {}
idCount = 0

WHITE = 'white'
BLACK = 'black'
COLOR = WHITE
all_sprites = pygame.sprite.Group()


def threaded_client(conn, p, gameId):
    global COLOR, WHITE, BLACK, idCount
    conn.send(str.encode(str(p)))
    reply = ''
    while True:
        try:
            data = conn.recv(2048).decode()

            if gameId in games:
                game = games[gameId]
                main_board = game.board
                if not data:
                    print('Disconnected')
                    break
                else:
                    if data == 'get_board':
                        reply = send_board(main_board).encode()
                    elif data == 'get_colorWent':
                        reply = game.colorWent.encode()
                    elif data == 'first_connect':
                        reply = WHITE.encode() if p == 0 else BLACK.encode()
                    elif data == 'is_ready':
                        reply = str(game.ready).encode()
                    elif data == 'end':
                        game.end = True
                    else:
                        if not game.end:
                            load_board(data, main_board, all_sprites)
                            COLOR = WHITE if COLOR == BLACK else BLACK
                            reply = send_board(main_board).encode()
                        else:
                            reply = 'end'.encode()
                    print('Received: ', reply)
                    print('Sending: ', reply)
                    conn.sendall(reply)

        except Exception as e:
            print(e)
            break

    print('Lost connection')
    conn.close()


# def change_board(board: Board, color):
#     for i in range(len(board.field)):
#         string = board.field[i]
#         for j in range(len(string)):
#             if string[j] != main_board.field[i][j]:
#                 if string[j] is not None and string[j].color == color:
#                     main_board.field[i][j] = string[j]
#                 elif string[j] is None and main_board.field[i][j].color == color:
#                     main_board.field[i][j] = string[j]
#     return main_board


while True:
    conn, addr = s.accept()
    print('Connected to:', addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        main_board = Board(8, 8)
        games[gameId] = OnlineGame(main_board, gameId)
        print('Creating a new game ...')
    else:
        games[gameId].ready = 1
        p = 1
    start_new_thread(threaded_client, (conn, p, gameId))
