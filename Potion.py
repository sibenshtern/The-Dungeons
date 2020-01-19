import pygame
from Functions import load_image


class Potion(pygame.sprite.Sprite):

    def __init__(self, x, y, potion_sprites, all_sprites):
        super(Potion, self).__init__(potion_sprites, all_sprites)
        self.image = load_image('Tiles\\Items', 'health_potion.png')
        self.rect = self.image.get_rect().move(16 * x, 16 * y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, player):
        if pygame.sprite.collide_mask(self, player):
            player.health = player.health + 2
            print(player.health)
            self.kill()
