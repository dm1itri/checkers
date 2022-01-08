import pygame


def mouse_coords(mouse_coords, sett):
    x, y = mouse_coords[0], mouse_coords[1]
    if width * 0.875 <= x <= width * 0.925:
        if 0 <= y <= 0 + 40:
            sett[0] = 100 if sett[0] == 100 else sett[0] + 10
        elif height * 0.2 <= y <= height * 0.2 + 40:
            sett[1] = 100 if sett[1] == 100 else sett[1] + 10
        elif height * 0.4 <= y <= height * 0.4 + 40:
            sett[2] = 75 if sett[2] == 75 else sett[2] + 5
    elif width * 0.075 <= x <= width * 0.125:
        if 0 <= y <= 0 + 40:
            sett[0] = 0 if sett[0] == 0 else sett[0] - 10
        elif height * 0.2 <= y <= height * 0.2 + 40:
            sett[1] = 40 if sett[1] == 40 else sett[1] - 10
        elif height * 0.4 <= y <= height * 0.4 + 40:
            sett[2] = 30 if sett[2] == 30 else sett[2] - 5
    with open('additional_functions/data/settings.txt', 'w') as f:
        f.write(' '.join(str(i) for i in sett))


def settings_run():
    global width, height
    pygame.init()
    size = width, height = 700, 500
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Настройки')
    running = True
    font = pygame.font.Font('additional_functions/fonts/main.ttf', 30)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_coords(event.pos, sett)
        screen.fill('white')
        with open('additional_functions/data/settings.txt') as f:
            sett = [int(i) for i in f.read().split()]
        sp = [f'Левый и правый отступ={sett[0]}', f'Верхний и нижний отступ={sett[1]}', f'Ширина клетки={sett[2]}']
        for i, t in enumerate(sp):
            text = font.render(t, True, 'black')
            screen.blit(text, (width * 0.2, height * 0.2 * i))
            pygame.draw.line(screen, '#a04c0b', (width * 0.9, height * 0.2 * i), (width * 0.9, height * 0.2 * i + 40), width=5)
            pygame.draw.line(screen, '#a04c0b', (width * 0.875, height * 0.2 * i + 20), (width * 0.925, height * 0.2 * i + 20), width=5)
            pygame.draw.line(screen, '#a04c0b', (width * 0.075, height * 0.2 * i + 20), (width * 0.125, height * 0.2 * i + 20), width=5)
        pygame.display.flip()


if __name__ == '__main__':
    settings_run()
