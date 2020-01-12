import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, ide_sheet, run_sheet,
                 rows, columns, x, y, player_group, all_sprites):
        super(Player, self).__init__(player_group, all_sprites)
        self.ide_frames = []
        self.run_frames = []
        self.cut_sheet(ide_sheet, rows, columns, self.ide_frames)
        self.cut_sheet(run_sheet, rows, columns, self.run_frames)
        self.cur_frame = 0
        self.image = self.ide_frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.now_anim = 'ide'

        self.previous_x = x
        self.previous_y = y

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
        if self.rect.x == self.previous_x and self.rect.y == self.previous_y:
            if self.now_anim.startswith('ide'):
                self.cur_frame = (self.cur_frame + 1) % len(self.ide_frames)
                self.image = self.ide_frames[self.cur_frame]
            else:
                self.cur_frame = 0
                self.image = self.ide_frames[self.cur_frame]
        else:
            if self.now_anim.startswith('run'):
                self.cur_frame = (self.cur_frame + 1) % len(self.ide_frames)
                self.image = self.ide_frames[self.cur_frame]
            else:
                self.now_anim = 'run'
                self.cur_frame = 0
                self.image = self.run_frames[self.cur_frame]
