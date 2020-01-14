import math
import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self, sheet, rows, columns, pos_x, pos_y, need_sprites,
                 all_sprites):
        super(Enemy, self).__init__(need_sprites, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, rows, columns, self.frames)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(16 * pos_x, 16 * pos_y)

    def cut_sheet(self, sheet, rows, columns, array):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                array.append(sheet.subsurface(
                    pygame.Rect(frame_location, self.rect.size)
                ))

    def update(self, player):
        if player.rect.x - self.rect.x > 0:
            if player.rect.y - self.rect.y < 0:
                if math.fabs(player.rect.x - self.rect.x) > \
                        math.fabs(player.rect.y - self.rect.y):
                    self.rect.x += 2
                else:
                    self.rect.y -= 2
            else:
                if math.fabs(player.rect.x - self.rect.x) > \
                        math.fabs(player.rect.y - self.rect.y):
                    self.rect.x += 2
                else:
                    self.rect.y -= 2

        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)

