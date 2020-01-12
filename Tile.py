import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, tile, tile_images, all_sprites, need_group, x, y):
        super(Tile, self).__init__(need_group, all_sprites)
        self.image = tile_images[tile.type][tile.name]
        self.rect = self.image.get_rect().move(16 * x, 16 * y)
