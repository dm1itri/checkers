import pygame
from additional_functions.server.network import Network
from additional_functions.server.load_board import load_board, send_board


def search_game_run():
    pygame.init()
    size = width, height = 500, 500
    fps = 30
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Поиск игры')
    clock = pygame.time.Clock()
    network = Network()
    running = True

    font = pygame.font.Font(None, 60)
    text = font.render('Игра в поиске', True, 'black')
    count_fps = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('white')
        screen.blit(text, (width // 2 - text.get_size()[0] // 2, height // 2 - text.get_size()[1] // 2))
        clock.tick(fps)
        pygame.display.flip()

        count_fps += 1
        if count_fps % 5:
            data = network.connect()
            if data:
                return data, network


if __name__ == '__main__':
    search_game_run()
