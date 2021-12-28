import sys
import pygame
import os


def load_image(name, colorkey=None, size=(50, 50), alpha=255):
    fullname = os.path.join('additional_functions/data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if alpha != 255:
        image.set_alpha(alpha)
    image = pygame.transform.scale(image, size)
    return image
