import os

import pygame
from Functions import load_image


class Heart(pygame.sprite.Sprite):

    def __init__(self, coordinates, group):
        self.full_heart = load_image(r'images\ui', 'ui_heart_full.png')
        self.half_heart = load_image(r'images\ui', 'ui_heart_half.png')
        self.empty_heart = load_image(r'images\ui', 'ui_heart_empty.png')
        super(Heart, self).__init__(group)
        self.coordinates = coordinates
        self.image = self.full_heart
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(coordinates)


class Text(pygame.sprite.Sprite):

    def __init__(self, text, group):
        super(Text, self).__init__(group)
        self.font = pygame.font.Font(os.path.join('data', 'font.ttf'), 24)

        self.image = self.font.render(text, 1, pygame.Color('white'))
        self.rect = self.image.get_rect()
        self.rect.x = 32
        self.rect.y = 64

    def update(self, text):
        self.image = self.font.render(text, 1, pygame.Color('white'))

