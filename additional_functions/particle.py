import random

import pygame
from additional_functions.load_image import load_image


screen_rect = (0, 0, 700, 575)
gravity = 0.1


class Particle(pygame.sprite.Sprite):
    """Визуальные эффекты"""

    # сгенерируем частицы разного размера
    fire = [pygame.transform.scale(load_image("black.png"), (60, 60)),
            pygame.transform.scale(load_image('white.png'), (60, 60))]

    def __init__(self, pos, dx, dy, part_group):
        super().__init__(part_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость - это вектор
        self.velocity = dx
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой
        self.gravity = gravity

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity += self.gravity
        # перемещаем частицу
        self.rect.y += self.velocity
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position, part_group):
    # количество создаваемых частиц
    particle_count = 1
    # возможные скорости
    numbers = range(0, 1)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), part_group)
