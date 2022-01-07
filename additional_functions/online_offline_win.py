import pygame
from additional_functions.button import Button


def on_off_run(main_font, sounds):
    pygame.init()
    size = width, height = 500, 500
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Шашки')
    buttons_group = pygame.sprite.Group()
    clock = pygame.time.Clock()
    running = True

    texts = {i[0]: i[1] for i in enumerate(['Онлайн игра', 'Оффлайн игра'])}
    buttons = {}
    for i in range(1, len(texts) + 1):
        text = _text(main_font, 35, texts[i - 1], '#c15c0f')
        btn = Button(120, 80 * i + 30, 60, 280, text, '#a04c0b', screen, buttons_group)

        buttons[btn] = texts[i - 1]

    main_text = _text(main_font, 50, 'Выбор', 'black')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in list(buttons.keys()):
                    if but.onclick(event.pos):
                        if sounds['on_sounds']:
                            sounds['click'].play(0)
                        text_btn = buttons[but]
                        if text_btn == 'Онлайн игра':
                            return 'online'
                        return 'offline'
        screen.fill('white')
        screen.blit(main_text, (width // 2 - (main_text.get_size()[0] // 2), 20))

        buttons_group.draw(screen)
        buttons_group.update()
        pygame.display.flip()


def _text(font, size, text, color):
    font = pygame.font.Font(font, size)
    return font.render(text, True, color)
