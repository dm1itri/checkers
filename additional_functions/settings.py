import pygame
from random import randrange

from additional_functions.button import Button
from additional_functions.particle import create_particles


def mouse_coords(mouse_coords, sett):

    x, y = mouse_coords[0], mouse_coords[1]
    flag = False
    if width * 0.875 <= x <= width * 0.925:
        if 0 <= y <= 0 + 40 + 280:
            if sett[0] == 100:
                sett[0] = 100
            else:
                sett[0] += 10
                flag = True
        elif height * 0.1 + 280 <= y <= height * 0.1 + 40 + 280:
            if sett[1] == 100:
                sett[1] = 100
            else:
                sett[1] += 10
                flag = True
        elif height * 0.2 + 280 <= y <= height * 0.2 + 40 + 280:
            if sett[2] == 75:
                sett[2] = 75
            else:
                sett[2] += 5
                flag = True
        elif height * 0.3 + 280 <= y <= height * 0.3 + 40 + 280:
            sett[3] = 1
            flag = True
        elif height * 0.4 + 280 <= y <= height * 0.4 + 40 + 280:
            sett[4] = 1
            flag = True
    elif width * 0.8 <= x <= width * 0.85:
        if 0 <= y <= 0 + 40 + 280:
            if sett[0] == 20:
                sett[0] = 20
            else:
                sett[0] -= 10
                flag = True
        elif height * 0.1 + 280 <= y <= height * 0.1 + 40 + 280:
            if sett[1] == 40:
                sett[1] = 40
            else:
                sett[1] -= 10
                flag = True
        elif height * 0.2 + 280 <= y <= height * 0.2 + 40 + 280:
            if sett[2] == 30:
                sett[2] = 30
            else:
                sett[2] -= 5
                flag = True
        elif height * 0.3 + 280 <= y <= height * 0.3 + 40 + 280:
            sett[3] = 0
            flag = True
        elif height * 0.4 + 280 <= y <= height * 0.4 + 40 + 280:
            sett[4] = 0
            flag = True
    with open('additional_functions/data/settings.txt', 'w') as f:
        f.write(' '.join(str(i) for i in sett))
    return flag


def settings_run(main_font, sounds):
    """Окно поиска игры"""

    global width, height
    pygame.init()
    size = width, height = 700, 575
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Настройки')
    buttons_group = pygame.sprite.Group()
    part_group = pygame.sprite.Group()
    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font('additional_functions/data/fonts/main.ttf', 30)
    running = True

    settings_text = 'Музыка\nЗвуки\nЭффекты'
    texts = {i[0]: i[1] for i in enumerate(['Включено' if sounds['on_music'] else 'Выключено',
                                            'Включено' if sounds['on_sounds'] else 'Выключено',
                                            'Включено' if sounds['on_effects'] else 'Выключено'])}
    buttons = {}
    settings = {}
    for i in range(1, len(texts) + 1):
        text = _text(main_font, 35, texts[i - 1], '#c15c0f')
        if texts[i - 1].startswith('Включено'):
            btn = Button(width * 0.1 + 250, 80 * i - 50, 60, 190, text, '#a04c0b', screen, buttons_group)
        else:
            btn = Button(width * 0.1 + 250, 80 * i - 50, 60, 210, text, '#a04c0b', screen, buttons_group)

        buttons[btn] = texts[i - 1]
        settings[btn] = settings_text.split('\n')[i - 1]

    count_fps = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    data = mouse_coords(event.pos, sett)
                    if data:
                        sounds['click'].play(0)
                for but in list(buttons.keys()):
                    if but.onclick(event.pos):
                        if sounds['on_sounds']:
                            sounds['click'].play(0)
                        text_btn = buttons[but]
                        buttons.pop(but)
                        but.kill()
                        if settings[but] == 'Музыка':
                            if text_btn == 'Включено':
                                pygame.mixer.music.pause()
                                sounds['on_music'] = False

                                text_render_sound = _text(main_font, 35, 'Выключено', '#c15c0f')
                                text_btn = 'Выключено'
                                width_btn = 210
                            elif text_btn == 'Выключено':
                                pygame.mixer.music.unpause()
                                sounds['on_music'] = True

                                text_render_sound = _text(main_font, 35, 'Включено', '#c15c0f')
                                text_btn = 'Включено'
                                width_btn = 190
                        elif settings[but] == 'Звуки':
                            if text_btn == 'Включено':
                                sounds['on_sounds'] = False

                                text_render_sound = _text(main_font, 35, 'Выключено', '#c15c0f')
                                text_btn = 'Выключено'
                                width_btn = 210
                            elif text_btn == 'Выключено':
                                sounds['on_sounds'] = True

                                text_render_sound = _text(main_font, 35, 'Включено', '#c15c0f')
                                text_btn = 'Включено'
                                width_btn = 190
                        elif settings[but] == 'Эффекты':
                            if text_btn == 'Включено':
                                sounds['on_effects'] = False
                                text_render_sound = _text(main_font, 35, 'Выключено', '#c15c0f')
                                text_btn = 'Выключено'
                                width_btn = 210
                            elif text_btn == 'Выключено':
                                sounds['on_effects'] = True
                                text_render_sound = _text(main_font, 35, 'Включено', '#c15c0f')
                                text_btn = 'Включено'
                                width_btn = 190
                        btn = Button(but.rect.x, but.rect.y, but.height, width_btn, text_render_sound, but.color,
                                     but.win,
                                     buttons_group)
                        buttons[btn] = text_btn
                        settings[btn] = settings[but]
                        del settings[but]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    sounds['click'].play(0)
        count_fps += 1

        screen.fill('white')

        part_group.draw(screen)
        part_group.update()

        lines = settings_text.splitlines()
        for i, l in enumerate(lines):
            screen.blit(_text(main_font, 50, l, 'black'), (width * 0.1, 30 + 80 * i))

        with open('additional_functions/data/settings.txt') as f:
            sett = [int(i) for i in f.read().split()]
        sp = [f'Левый и правый отступ={sett[0]}', f'Верхний и нижний отступ={sett[1]}', f'Ширина клетки={sett[2]}',
              f'Подсветка ходов={"ON" if sett[3] else "OFF"}', f'Анимация хода={"ON" if sett[4] else "OFF"}']
        for i, t in enumerate(sp):
            text1 = font.render(t, True, 'black')
            screen.blit(text1, (width * 0.1, height * 0.1 * i + 280))

            pygame.draw.rect(screen, '#a04c0b', (width * 0.875 - 4, height * 0.1 * i + 280 - 4, 45, 50), 0)
            pygame.draw.rect(screen, '#a04c0b', (width * 0.8 - 4, height * 0.1 * i + 280 - 4, 45, 50), 0)
            pygame.draw.rect(screen, 'white', (width * 0.875 - 2, height * 0.1 * i + 280 - 2, 41, 46), 0)
            pygame.draw.rect(screen, 'white', (width * 0.8 - 2, height * 0.1 * i + 280 - 2, 41, 46), 0)

            pygame.draw.line(screen, '#a04c0b', (width * 0.9, height * 0.1 * i + 280),
                             (width * 0.9, height * 0.1 * i + 40 + 280),
                             width=5)
            pygame.draw.line(screen, '#a04c0b', (width * 0.875, height * 0.1 * i + 20 + 280),
                             (width * 0.925, height * 0.1 * i + 20 + 280), width=5)
            pygame.draw.line(screen, '#a04c0b', (width * 0.8, height * 0.1 * i + 20 + 280),
                             (width * 0.85, height * 0.1 * i + 20 + 280), width=5)

        buttons_group.draw(screen)
        buttons_group.update()

        if count_fps % 60 == 0:
            if sounds['on_effects']:
                create_particles((randrange(0, width), -50), part_group)

        pygame.display.flip()
        clock.tick(fps)


def _text(font, size, text, color):
    font = pygame.font.Font(font, size)
    return font.render(text, True, color)
