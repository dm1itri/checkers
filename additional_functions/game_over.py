import pygame
from additional_functions.server.network import Network
from additional_functions.board import load_move, send_move
from additional_functions.button import Button


def game_over_run(winner, main_font, sounds, offline=False):
    """Диалоговое окно завершения игры"""

    pygame.init()
    size = width, height = 550, 300
    fps = 30
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Конец игры')
    clock = pygame.time.Clock()
    buttons_group = pygame.sprite.Group()
    running = True

    texts = {i[0]: i[1] for i in enumerate(['Ок'])}
    buttons = {}
    for i in range(1, len(texts) + 1):
        text = _text(main_font, 35, texts[i - 1], '#c15c0f')
        btn = Button(100 + 100 * i, 180, 65, 70, text, '#a04c0b', screen, buttons_group)
        buttons[btn] = texts[i - 1]

    if winner is None:
        if not offline:
            text = 'Игра завершена,\nтак как один из\nигроков покинул ее'
        else:
            text = '\nИгра завершена'
    elif winner:
        text = 'Игра завершена,\nВы одержали победу'
    else:

        text = 'Игра завершена,\nВы потерпели\nпоражение'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in buttons:
                    if but.onclick(event.pos):
                        if sounds['on_sounds']:
                            sounds['click'].play(0)
                        text_btn = buttons[but]
                        if text_btn == 'Ок':
                            return
        screen.fill('white')
        lines = text.splitlines()
        for i, l in enumerate(lines):
            screen.blit(_text(main_font, 50, l, 'black'), (40, 30 + 40 * i))

        buttons_group.draw(screen)
        buttons_group.update()

        clock.tick(fps)
        pygame.display.flip()


def _text(font, size, text, color):
    font = pygame.font.Font(font, size)
    return font.render(text, True, color)
