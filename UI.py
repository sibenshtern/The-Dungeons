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
