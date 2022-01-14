import pygame


class Button(pygame.sprite.Sprite):
    """Универсальная кнопка"""

    def __init__(self, x, y, height, width, text, color, win, *groups):
        super().__init__(*groups)
        self.height = height
        self.width = width
        self.image = pygame.Surface((width, height))
        self.image.fill('white')
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.text = text
        self.win = win

    def onclick(self, pos):
        x_click, y_click = pos[0], pos[1]
        if self.rect.x < x_click < self.rect.x + self.width and self.rect.y < y_click < self.rect.y + self.height:
            return True
        return False

    def update(self):
        # рамка
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height), 5)

        self.win.blit(self.text, (self.rect.x + self.width // 20, self.rect.y + self.height // 10))
