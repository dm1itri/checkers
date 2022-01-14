import pygame
from sqlite3 import connect
from random import randrange
from additional_functions.particle import create_particles


def draw(screen, main_font):
    conn = connect('additional_functions/data/database/profile.sqlite')
    with conn:  # возвращение информации
        t = conn.cursor().execute(f'SELECT * from statistics_matches').fetchone()
    texts = [f'Кол-во начатых матчей', 'Кол-во сыгранных матчей', 'Процент побед',
             'Среднее время матча (мин.)']
    screen.fill('white', (10, 20, 230, 100))
    screen.fill('white', (260, 20, 230, 100))
    screen.fill('white', (125, 150, 250, 100))
    screen.fill('white', (125, 300, 250, 100))
    pygame.draw.rect(screen, '#a04c0b', (10, 20, 230, 100), 5)
    pygame.draw.rect(screen, '#a04c0b', (260, 20, 230, 100), 5)
    pygame.draw.rect(screen, '#a04c0b', (125, 150, 250, 100), 5)
    pygame.draw.rect(screen, '#a04c0b', (125, 300, 250, 100), 5)

    texts1 = [_text(main_font, 18, i, 'black') for i in texts]
    screen.blit(texts1[0], (15, 30, 230, 100))
    screen.blit(texts1[1], (265, 30, 230, 100))
    screen.blit(texts1[2], (130, 160, 250, 100))
    screen.blit(texts1[3], (130, 310, 250, 100))

    texts = [str(t[0]), str(t[1]), str(round(t[2] / t[1], ndigits=4) * 100) + '%',
             str(round(t[3] / 60 / t[1], ndigits=2))]
    texts1 = [_text(main_font, 40, i, '#c15c0f') for i in texts]
    screen.blit(texts1[0], (15, 50, 230, 100))
    screen.blit(texts1[1], (265, 50, 230, 100))
    screen.blit(texts1[2], (130, 180, 250, 100))
    screen.blit(texts1[3], (130, 330, 250, 100))


def statistics(main_font, sounds):
    pygame.init()
    size = width, height = 500, 500
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    part_group = pygame.sprite.Group()
    screen.fill((255, 255, 255))
    pygame.display.set_caption('Статистика')
    running = True

    count_fps = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('white')
        part_group.draw(screen)
        part_group.update()

        draw(screen, main_font)
        if count_fps % 60 == 0:
            if sounds['on_effects']:
                create_particles((randrange(0, width), -50), part_group)
        count_fps += 1
        clock.tick(60)
        pygame.display.flip()


def _text(font, size, text, color):
    font = pygame.font.Font(font, size)
    return font.render(text, True, color)
