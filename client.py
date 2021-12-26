from additional_functions.server.network import Network
from additional_functions.server.load_board import load_board, send_board
from additional_functions.board import Board

board = Board(8, 8)
lol = send_board(board).encode()
print(lol.decode())