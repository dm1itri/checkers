import pygame
from random import randrange

from additional_functions.button import Button
from additional_functions.board import online_run, offline_run
from additional_functions.settings import settings_run
from additional_functions.particle import create_particles

from additional_functions.load_image import load_image
from additional_functions.search_game import search_game_run
from additional_functions.dialog_win import dialog_run
from additional_functions.game_over import game_over_run
from additional_functions.online_offline_win import on_off_run

import sys


def terminate():
    pygame.quit()
    sys.exit()


class Menu:
    def __init__(self):
        self.main_font = 'additional_functions/fonts/main.ttf'
        pass

    def run(self):
        pygame.init()
        size = width, height = 700, 500
        fps = 60
        # screen — холст, на котором нужно рисовать:
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Меню')
        clock = pygame.time.Clock()
        buttons_group = pygame.sprite.Group()
        part_group = pygame.sprite.Group()
        background = load_image('main_background.jpg')
        screen.fill(pygame.color.Color('white'))

        main_text = self.text(self.main_font, 50, 'Шашки Онлайн', 'black')

        print(main_text)
        # создание кнопок
        texts = {i[0]: i[1] for i in enumerate(['Играть', 'Настройки'])}
        buttons = {}
        for i in range(1, len(texts) + 1):
            text = self.text(self.main_font, 50, texts[i - 1], '#c15c0f')
            btn = Button(200, 100 * i, 70, 300, text, '#a04c0b', screen, buttons_group)
            buttons[btn] = texts[i - 1]

        # добваление музыки
        pygame.mixer.music.load('additional_functions/data/main_s.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1, 0, 10)

        sounds = {}
        click = pygame.mixer.Sound('additional_functions/data/click.wav')
        find_sound = pygame.mixer.Sound('additional_functions/data/find.wav')
        move = pygame.mixer.Sound('additional_functions/data/move.wav')

        sounds['click'] = click
        sounds['find'] = find_sound
        sounds['move'] = move
        sounds['on_sounds'] = True
        sounds['on_music'] = True

        clock = pygame.time.Clock()
        running = True

        count_fps = 0
        while running:
            pygame.display.set_caption('Меню')
            size = width, height = 700, 500
            screen = pygame.display.set_mode(size)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for but in buttons:
                            if but.onclick(event.pos):
                                if sounds['on_sounds']:
                                    click.play(0)
                                text_btn = buttons[but]
                                if text_btn == 'Играть':
                                    out = on_off_run(self.main_font, sounds)
                                    if out == 'online':
                                        data = search_game_run(self.main_font, sounds)
                                        if data:
                                            if sounds['on_sounds']:
                                                sounds['find'].play(0)
                                            network, my_color = data
                                            if dialog_run('Мы нашли игру,\nприсоединиться?',
                                                          self.main_font, sounds):
                                                pygame.mixer.music.set_volume(0.05)
                                                winner = online_run(network, my_color, 'white', sounds)
                                                pygame.mixer.music.set_volume(0.2)
                                                game_over_run(winner, self.main_font, sounds)

                                            else:
                                                network.send('end')
                                    elif out == 'offline':
                                        offline_run(sounds)
                                elif text_btn == 'Настройки':
                                    settings_run(self.main_font, sounds)
                    elif event.button == 3:
                        pass
            count_fps += 1

            screen.fill(pygame.color.Color('white'))
            part_group.draw(screen)
            part_group.update()
            screen.blit(main_text, (width // 2 - (main_text.get_size()[0] // 2), 20))
            buttons_group.draw(screen)
            buttons_group.update()

            if count_fps % 30 == 0:
                create_particles((randrange(0, width), -50), part_group)

            pygame.display.flip()
            clock.tick(fps)

    def text(self, font, size, text, color):
        font = pygame.font.Font(font, size)
        return font.render(text, True, color)


if __name__ == '__main__':
    menu = Menu()
    menu.run()
