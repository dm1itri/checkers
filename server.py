import socket
from threading import *

from additional_functions.board import load_move, send_move
from additional_functions.server.online_game import OnlineGame

host = socket.gethostbyname(socket.gethostname())
server = host
print(host)
port = 6668

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


class ThreadMain(Thread):
    def __init__(self, conn, p, gameId):
        super().__init__()
        self.daemon = True
        self.conn = conn
        self.p = p
        self.gameId = gameId

    def run(self):
        global COLOR, WHITE, BLACK, idCount
        self.conn.send(str.encode(str(p)))
        reply = ''
        while True:
            try:
                data = self.conn.recv(2048).decode()

                if self.gameId in games:
                    game = games[self.gameId]
                    if not data:
                        print('Disconnected')
                        game.end = True
                        if not game.ready:
                            idCount += 1
                        break
                    else:

                        if game.end and not game.winner:
                            del games[self.gameId]
                            reply = 'end'.encode()
                            self.conn.sendall(reply)
                            break

                        elif data == 'winner':
                            game.winner = True

                        elif data == 'get_move':
                            if self.p == 0:
                                if game.p2Move:
                                    reply = send_move(game.p2Move[0], game.p2Move[1]).encode()
                                    game.p2Move = False
                                else:
                                    reply = 'None'.encode()
                            if self.p == 1:
                                if game.p1Move:
                                    reply = send_move(game.p1Move[0], game.p1Move[1]).encode()
                                    game.p1Move = False

                                else:
                                    reply = 'None'.encode()
                        elif data == 'get_colorWent':
                            reply = game.colorWent.encode()
                        elif data == 'first_connect':
                            reply = WHITE.encode() if self.p == 0 else BLACK.encode()
                        elif data == 'is_ready':
                            reply = str(game.ready).encode()
                        elif data == 'end':
                            game.end = True
                            reply = 'end'.encode()
                            self.conn.sendall(reply)
                            break
                        else:
                            if self.p == 0:
                                move = load_move(data)
                                move = (7 - move[0][0], 7 - move[0][1]),\
                                       list(map(lambda x: (7 - x[0], 7 - x[1]), move[1]))
                                game.p1Move = move
                            else:
                                move = load_move(data)
                                move = (7 - move[0][0], 7 - move[0][1]),\
                                       list(map(lambda x: (7 - x[0], 7 - x[1]), move[1]))
                                game.p2Move = move
                            COLOR = WHITE if COLOR == BLACK else BLACK
                            reply = '-'.encode()

                        print('Received: ', reply)
                        print('Sending: ', reply)
                        self.conn.sendall(reply)

            except Exception as e:
                print(e)
                break

        print('Lost connection')
        self.conn.close()


while True:
    conn, addr = s.accept()
    print('Connected to:', addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = OnlineGame(gameId)
        print('Creating a new game ...')
    else:
        games[gameId].ready = 1
        p = 1
    thread = ThreadMain(conn, p, gameId)
    thread.start()
