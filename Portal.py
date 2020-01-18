import pygame
from Functions import load_image


class Portal(pygame.sprite.Sprite):

    def __init__(self, x, y, animated_sprites, all_sprites):
        super(Portal, self).__init__(animated_sprites, all_sprites)
        self.frames = []
        self.cut_sheet(load_image('Tiles\\Animated', 'portal.png'), 1, 8)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(16 * (x - 1), 16 * (y - 2))

    def cut_sheet(self, sheet, rows, columns):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(
                    pygame.Rect(frame_location, self.rect.size)
                ))

    def update(self, player):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)

        if pygame.sprite.collide_mask(self, player):
            player.score += 5 * player.health
            player.next_level = True
