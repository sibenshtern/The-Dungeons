import pygame


class AnimatedTile(pygame.sprite.Sprite):

    def __init__(self, sheet, rows, columns, x, y, animated_sprites,
                 all_sprites):
        super(AnimatedTile, self).__init__(animated_sprites, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, rows, columns, self.frames)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(16 * x, 16 * y)

    def cut_sheet(self, sheet, rows, columns, array):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                array.append(sheet.subsurface(
                    pygame.Rect(frame_location, self.rect.size)
                ))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
