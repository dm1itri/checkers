import pygame
import os
from additional_functions.server.network import Network
from additional_functions.board import load_move, send_move
from additional_functions.load_image import load_image


def search_game_run(main_font, sounds):
    pygame.init()
    size = width, height = 500, 500
    fps = 30
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    load_sprites = pygame.sprite.Group()
    pygame.display.set_caption('Поиск игры')
    clock = pygame.time.Clock()

    network = Network()

    running = True

    font = pygame.font.Font(main_font, 60)
    text = font.render('Игра в поиске', True, 'black')
    network.connect()
    count_fps = 0

    AnimatedSprite(load_image('load_frames.png'), 8, 1, width // 2 - 32, height // 2 , load_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sounds['click'].play(0)
                    return False
        screen.fill('white')
        screen.blit(text, (width // 2 - text.get_size()[0] // 2, height // 2 - text.get_size()[1] // 2 - 80))

        count_fps += 1
        if count_fps % 50:
            color = network.send('first_connect')
            print(color)
            if color is not None and color != 'end' and color:
                is_ready = int(network.send('is_ready'))
                print(is_ready, 'is_ready')
                if is_ready:
                    return network, color
        if count_fps % 5:
            load_sprites.update()

        load_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, all_sprites):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        print(sheet.get_width() // columns,
              sheet.get_height() // rows)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

        print(self.frames)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

