import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, ide_sheet, x, y, rows, columns, player_group,
                 all_sprites, animated, health, score):
        super(Player, self).__init__(player_group, all_sprites)
        self.ide_frames = []
        self.cut_sheet(ide_sheet, rows, columns, self.ide_frames)
        self.cur_frame = 0
        self.image = self.ide_frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.now_anim = 'ide'
        self.set_coordinates(x, y)

        self.previous_x = 0
        self.previous_y = 0

        self.health = health
        self.score = score

        self.animated = animated

        self.die = False
        self.next_level = False  # КОСТЫЛЬ КОСТЫЛЬНЫЙ

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

    def check_enemies(self, enemies):
        for sprite in enemies:
            if pygame.sprite.collide_mask(self, sprite):
                pygame.mixer.music.load('data\\hit.wav')
                pygame.mixer.music.set_volume(0.02)
                pygame.mixer.music.play(1)
                sprite.kill()
                self.score += 10

    def move(self, distance, *collided_sprites, up=False, right=False,
             down=False, left=False):
        if not self.die:
            for sprite_group in collided_sprites:
                for sprite in sprite_group:
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
