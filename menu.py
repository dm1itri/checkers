import pygame
from pgu import gui
from additional_functions.button import Button
from additional_functions.board import online_run
from additional_functions.settings import settings_run
from additional_functions.particle import create_particles, part_group

from additional_functions.search_game import search_game_run
from additional_functions.dialog_win import dialog_run
from additional_functions.game_over import game_over_run

import sys


def terminate():
    pygame.quit()
    sys.exit()


class SimpleDialog(gui.Dialog):
    def __init__(self):
        title = gui.Label("Spam")
        main = gui.Container(width=20, height=20)
        # I patched PGU to use new style classes.
        super(SimpleDialog, self).__init__(title, main, width=40, height=40)

    def close(self, *args, **kwargs):
        print("closing")
        return super(SimpleDialog, self).close(*args, **kwargs)


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
        sounds['click'] = click
        sounds['find'] = find_sound

        clock = pygame.time.Clock()
        running = True
        while running:
            size = width, height = 700, 500
            screen = pygame.display.set_mode(size)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for but in buttons:
                            if but.onclick(event.pos):
                                click.play(0)
                                text_btn = buttons[but]
                                if text_btn == 'Играть':
                                    data = search_game_run(self.main_font)
                                    if data:
                                        sounds['find'].play(0)
                                        network, my_color = data
                                        if dialog_run('Мы нашли игру,\nприсоединиться?',
                                                      self.main_font, click):
                                            pygame.mixer.music.set_volume(0.05)
                                            winner = online_run(network, my_color, 'white')
                                            pygame.mixer.music.set_volume(0.2)
                                            game_over_run(winner, self.main_font, sounds)

                                        else:
                                            network.send('end')
                                elif text_btn == 'Настройки':
                                    settings_run(self.main_font, click)
                    elif event.button == 3:
                        pass

            screen.fill(pygame.color.Color('white'))
            screen.blit(main_text, (width // 2 - (main_text.get_size()[0] // 2), 20))
            buttons_group.draw(screen)
            buttons_group.update()
            part_group.draw(screen)
            part_group.update()

            pygame.display.flip()
            clock.tick(fps)

    def text(self, font, size, text, color):
        font = pygame.font.Font(font, size)
        return font.render(text, True, color)


if __name__ == '__main__':
    menu = Menu()
    menu.run()
