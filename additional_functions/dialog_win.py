import pygame
from additional_functions.server.network import Network
from additional_functions.board import load_move, send_move
from additional_functions.button import Button


def dialog_run(text, main_font, click):
    pygame.init()
    size = width, height = 500, 300
    fps = 30
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Question')
    clock = pygame.time.Clock()
    buttons_group = pygame.sprite.Group()
    running = True

    font = pygame.font.Font(None, 60)
    text = font.render(text, True, 'black')

    main_text = 'Мы нашли игру,\nприсоединиться?'
    texts = {i[0]: i[1] for i in enumerate(['Да', 'Нет'])}
    buttons = {}
    for i in range(1, len(texts) + 1):
        text = _text(main_font, 35, texts[i - 1], '#c15c0f')
        btn = Button(50 + 100 * i, 180, 65, 70, text, '#a04c0b', screen, buttons_group)
        buttons[btn] = texts[i - 1]

    print(buttons_group)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in buttons:
                    if but.onclick(event.pos):
                        click.play(0)
                        text_btn = buttons[but]
                        if text_btn == 'Да':
                            return True
                        elif text_btn == 'Нет':
                            return False
        screen.fill('white')
        lines = main_text.splitlines()
        for i, l in enumerate(lines):
            screen.blit(_text(main_font, 50, l, 'black'), (70, 50 + 35*i))

        buttons_group.draw(screen)
        buttons_group.update()

        clock.tick(fps)
        pygame.display.flip()


def _text(font, size, text, color):
    font = pygame.font.Font(font, size)
    return font.render(text, True, color)
