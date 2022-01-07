import pygame
from additional_functions.button import Button


def settings_run(main_font, click):
    pygame.init()
    size = width, height = 500, 500
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Шашки')
    buttons_group = pygame.sprite.Group()
    clock = pygame.time.Clock()
    running = True

    texts = {i[0]: i[1] for i in enumerate(['Включено'])}
    buttons = {}
    for i in range(1, len(texts) + 1):
        text = _text(main_font, 35, texts[i - 1], '#c15c0f')
        btn = Button(180, 40 * i - 10, 60, 190, text, '#a04c0b', screen, buttons_group)
        buttons[btn] = texts[i - 1]

    text = 'Звук'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in list(buttons.keys()):
                    if but.onclick(event.pos):
                        click.play(0)
                        text_btn = buttons[but]
                        if text_btn == 'Включено' or text_btn == 'Выключено':
                            buttons.pop(but)
                            but.kill()
                            if text_btn == 'Включено':
                                pygame.mixer.music.pause()

                                text_render_sound = _text(main_font, 35, 'Выключено', '#c15c0f')
                                text_btn = 'Выключено'
                                width = 210
                            else:
                                pygame.mixer.music.unpause()

                                text_render_sound = _text(main_font, 35, 'Включено', '#c15c0f')
                                text_btn = 'Включено'
                                width = 190
                            btn = Button(but.rect.x, but.rect.y, but.height, width, text_render_sound, but.color, but.win,
                                         buttons_group)
                            buttons[btn] = text_btn

        screen.fill('white')
        lines = text.splitlines()
        for i, l in enumerate(lines):
            screen.blit(_text(main_font, 50, l, 'black'), (40, 30 + 40 * i))

        buttons_group.draw(screen)
        buttons_group.update()
        print(buttons_group, buttons)
        pygame.display.flip()


def _text(font, size, text, color):
    font = pygame.font.Font(font, size)
    return font.render(text, True, color)
