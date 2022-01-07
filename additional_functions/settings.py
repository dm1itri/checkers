import pygame


def settings_run(main_font):
    pygame.init()
    size = width, height = 500, 500
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Шашки')
    clock = pygame.time.Clock()
    running = True

    font = pygame.font.Font(None, 60)
    text = 'Звук'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('white')
        lines = text.splitlines()
        for i, l in enumerate(lines):
            screen.blit(_text(main_font, 50, l, 'black'), (40, 30 + 40 * i))
        pygame.display.flip()


def _text(font, size, text, color):
    font = pygame.font.Font(font, size)
    return font.render(text, True, color)
