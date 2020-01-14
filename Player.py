import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, ide_sheet, run_sheet, x, y,
                 rows, columns, player_group, all_sprites, animated):
        super(Player, self).__init__(player_group, all_sprites)
        self.ide_frames = []
        self.run_frames = []
        self.cut_sheet(ide_sheet, rows, columns, self.ide_frames)
        self.cut_sheet(run_sheet, rows, columns, self.run_frames)
        self.cur_frame = 0
        self.image = self.ide_frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.now_anim = 'ide'
        self.set_coordinates(x, y)

        self.previous_x = 0
        self.previous_y = 0

        self.health = 20

        self.animated = animated

        self.die = False

    def set_coordinates(self, x, y):
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

    def move(self, distance, collided_sprites, up=False, right=False,
             down=False, left=False):
        if not self.die:
            for sprite in collided_sprites:
                if pygame.sprite.collide_mask(self, sprite):
                    sprite_x = sprite.rect.x
                    sprite_y = sprite.rect.y
                    if sprite_x > self.rect.x:
                        left = False
                    if sprite_x < self.rect.x:
                        right = False
                    if sprite_y < self.rect.y:
                        up = False
                    if sprite_y > self.rect.y:
                        down = False

            if up:
                self.rect.y -= distance
            if left:
                self.rect.x += distance
            if right:
                self.rect.x -= distance
            if down:
                self.rect.y += distance

    def update(self):
        if not self.die:
            if self.now_anim.startswith('ide'):
                self.cur_frame = (self.cur_frame + 1) % len(self.ide_frames)
                self.image = self.ide_frames[self.cur_frame]
            else:
                self.now_anim = 'ide'
                self.cur_frame = 0
                self.image = self.ide_frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)

            self.previous_x = self.rect.x
            self.previous_y = self.rect.y

            for sprite in self.animated:
                if pygame.sprite.collide_mask(self, sprite) and \
                        sprite.cur_frame > 1:
                    self.health -= 1
                    if self.health <= 0:
                        self.die = True
