import socket
from _thread import *
import pickle
from additional_functions.board import Board, Usual
from additional_functions.server.load_board import load_board, send_board

server = '192.168.0.3'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print('Waiting for a connection, Server Started')

# print(board[0])


def threaded_client(conn):

    conn.send('Приветик'.encode())
    reply = ''
    while True:
        try:
            data = conn.recv(2048).decode()
            print(data)
            board = load_board(data)
            print(board)
            if not data:
                print('Disconnected')
                break
            else:
                reply = board
                print('Received: ', reply)
                print('Sending: ', reply)
            conn.sendall(reply.encode())
        except Exception as e:
            print(e, 'тип ошибочка')
            break
    print('Lost connection')
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print('Connected to:', addr)

    start_new_thread(threaded_client, (conn,))
    currentPlayer += 1
