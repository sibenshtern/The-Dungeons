import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self, image, pos_x, pos_y, need_sprites,
                 all_sprites):
        super(Enemy, self).__init__(need_sprites, all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(16 * pos_x, 16 * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, player):
        if player.rect.x > self.rect.x:
            self.rect.x += 2
        elif player.rect.x < self.rect.x:
            self.rect.x -= 2

        if player.rect.y > self.rect.y:
            self.rect.y += 2
        elif player.rect.y < self.rect.y:
            self.rect.y -= 2

    def check_player(self, player):
        if pygame.sprite.collide_mask(self, player):
            player.health -= 1

