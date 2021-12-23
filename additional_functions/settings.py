import pygame


def settings_run():
    pygame.init()
    size = width, height =500, 500
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Шашки')
    clock = pygame.time.Clock()
    running = True

    font = pygame.font.Font(None, 60)
    text = font.render('В разработке', True, 'black')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('white')
        screen.blit(text, (width // 2 - text.get_size()[0] // 2, height // 2 - text.get_size()[1] // 2))
        pygame.display.flip()


if __name__ == '__main__':
    settings_run()
