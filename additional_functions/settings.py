import pygame
from random import randrange

from additional_functions.button import Button
from additional_functions.particle import create_particles


def settings_run(main_font, sounds):
    pygame.init()
    size = width, height = 500, 500
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Шашки')
    buttons_group = pygame.sprite.Group()
    part_group = pygame.sprite.Group()
    clock = pygame.time.Clock()
    fps = 60
    running = True

    texts = {i[0]: i[1] for i in enumerate(['Включено' if sounds['on_music'] else 'Выключено',
                                            'Включено ' if sounds['on_sounds'] else 'Выключено '])}
    buttons = {}
    for i in range(1, len(texts) + 1):
        text = _text(main_font, 35, texts[i - 1], '#c15c0f')
        if texts[i - 1].startswith('Включено'):
            btn = Button(240, 80 * i - 50, 60, 190, text, '#a04c0b', screen, buttons_group)
        else:
            btn = Button(240, 80 * i - 50, 60, 210, text, '#a04c0b', screen, buttons_group)

        buttons[btn] = texts[i - 1]

    text = 'Музыка\nЗвуки'

    count_fps = 0
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
                        if text_btn.startswith('Включено') or text_btn.startswith('Выключено'):
                            buttons.pop(but)
                            but.kill()
                            if text_btn == 'Включено':
                                pygame.mixer.music.pause()
                                sounds['on_music'] = False

                                text_render_sound = _text(main_font, 35, 'Выключено', '#c15c0f')
                                text_btn = 'Выключено'
                                width = 210
                            elif text_btn == 'Выключено':
                                pygame.mixer.music.unpause()
                                sounds['on_music'] = True

                                text_render_sound = _text(main_font, 35, 'Включено', '#c15c0f')
                                text_btn = 'Включено'
                                width = 190
                            elif text_btn == 'Включено ':
                                sounds['on_sounds'] = False

                                text_render_sound = _text(main_font, 35, 'Выключено', '#c15c0f')
                                text_btn = 'Выключено '
                                width = 210
                            elif text_btn == 'Выключено ':
                                sounds['on_sounds'] = True

                                text_render_sound = _text(main_font, 35, 'Включено', '#c15c0f')
                                text_btn = 'Включено '
                                width = 190
                            btn = Button(but.rect.x, but.rect.y, but.height, width, text_render_sound, but.color,
                                         but.win,
                                         buttons_group)
                            buttons[btn] = text_btn

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    sounds['click'].play(0)


        count_fps += 1

        screen.fill('white')

        part_group.draw(screen)
        part_group.update()

        lines = text.splitlines()
        for i, l in enumerate(lines):
            screen.blit(_text(main_font, 50, l, 'black'), (40, 30 + 80 * i))

        buttons_group.draw(screen)
        buttons_group.update()

        if count_fps % 60 == 0:
            create_particles((randrange(0, width), -50), part_group)

        pygame.display.flip()
        clock.tick(fps)


def _text(font, size, text, color):
    font = pygame.font.Font(font, size)
    return font.render(text, True, color)
