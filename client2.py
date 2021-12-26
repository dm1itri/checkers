from additional_functions.menu import Menu
from additional_functions.server.network import Network
from additional_functions.server.load_board import load_board, send_board
from time import sleep
if __name__ == '__main__':

    network = Network()
    board = load_board('w.w.w.w.%.w.w.w.w%w.w.w.w.%........%........%b.b.b.b.%.b.b.b.b%b.b.b.b.')
    data = send_board(board)
    network.send(data)

    new_data = network.load()
    print(new_data)
    while True:
        sleep(3)
    # menu = Menu()
    # menu.run()
