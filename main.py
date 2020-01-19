from __future__ import annotations
import os
import sys
import webbrowser
from collections import namedtuple

import pygame

# import files with need classes
import UI
import Tile
import Enemy
import Tiles
import Potion
import Portal
import Button
import Camera
import Player
import AnimatedTile

from Functions import load_image
from LevelGenerator import generate_level
from MapGenerator import generate_field, Room


class Game:

    def __init__(self, window_width, window_height):
        pygame.init()

        self.size = window_width, window_height
        self.window_width = window_width
        self.window_height = window_height

        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.camera = Camera.Camera(self.window_width, self.window_height)
        self.floor = namedtuple('Floor', ['type', 'name'])('floor', 0)
        self.player = None

        # initialize sprites
        self.game_over_button_sprite = pygame.sprite.GroupSingle()
        self.main_button_sprites = pygame.sprite.Group()
        self.portal_sprite = pygame.sprite.GroupSingle()

        self.player_sprite = pygame.sprite.GroupSingle()
        self.sword_sprite = pygame.sprite.GroupSingle()
        self.animated_sprites = pygame.sprite.Group()
        self.potion_sprites = pygame.sprite.Group()
        self.floor_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.boxes_sprites = pygame.sprite.Group()
        self.side_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group()

        self.tiles = Tiles.return_tiles()

        # special player variables
        self.player_health = 20
        self.player_score = 0

        self.FPS = 60  # const
        self.k = 19  # special variable which need for right room's drawing
        self.bg_color = pygame.Color(29, 16, 70)

    def start(self):
        self.menu()
        return None

    def menu(self):
        """
        Function which show main menu (also start screen)
        """
        self.screen.fill(self.bg_color)
        font = pygame.font.Font(os.path.join('data', 'font.ttf'), 60)
        rendered_text = font.render('The Dungeons', 1, pygame.Color('yellow'))
        header_rect = rendered_text.get_rect()
        header_rect.x = self.window_width // 2 - header_rect.width // 2
        header_rect.y = 70
        self.screen.blit(rendered_text, header_rect)

        # create buttons
        buttons = ['Start Game', 'Record Table', 'Rules']
        button_classes = []

        for i in range(len(buttons)):
            button_center = self.window_width // 2
            button_y = 269 + (16 * (i + 1)) + 64 * i

            button_classes.append(
                Button.Button(
                    (button_center, button_y), self.main_button_sprites,
                    self.screen, buttons[i], type=buttons[i].lower(),
                    website=None
                )
            )

        button_classes.append(
            Button.Button(
                (self.window_width - 112, self.window_height - 96),
                self.main_button_sprites, self.screen, 'Github',
                type='open website', website='https://github.com/sibenshtern'
            )
        )

        while True:
            for menu_event in pygame.event.get():
                if menu_event.type == pygame.QUIT:
                    self.terminate()
                if menu_event.type == pygame.MOUSEBUTTONDOWN:
                    for button in button_classes:
                        if button.rect.collidepoint(menu_event.pos):
                            if button.button_type == 'open website':
                                webbrowser.open(button.website)
                            if button.button_type == 'start game':
                                self.game()
                                return

            self.main_button_sprites.draw(self.screen)
            self.main_button_sprites.update()
            pygame.display.flip()

    def game(self):
        player_x, player_y = self.load_map(generate_field())

        self.player = Player.Player(
            load_image('images', 'idle_anim.png'), player_x, player_y, 1, 4,
            self.player_sprite, self.all_sprites, self.animated_sprites,
            self.player_health, self.player_score
        )
        animate_index = 0

        for index in range(10):
            UI.Heart((32 + index * 24, 32), self.ui_sprites)

        UI.Text(f'Your score: {self.player.score}', self.ui_sprites)

        pygame.mixer.music.load(os.path.join('data', 'soundtrack1.mp3'))
        pygame.mixer.music.play(10)
        pygame.mixer.music.set_volume(0.01)

        # game loop
        while True:
            for game_event in pygame.event.get():
                if game_event.type == pygame.QUIT:
                    self.terminate()
                if game_event.type == pygame.KEYDOWN:
                    if game_event.key == pygame.K_SPACE:
                        self.player.check_enemies(self.enemy_sprites)
                    if game_event.key == pygame.K_RETURN:
                        self.potion_sprites.update(self.player)

            if pygame.key.get_pressed()[pygame.K_UP] == 1:
                self.player.move(3, self.side_sprites, self.boxes_sprites,
                                 up=True)
            if pygame.key.get_pressed()[pygame.K_RIGHT] == 1:
                self.player.move(3, self.side_sprites, self.boxes_sprites,
                                 left=True)
            if pygame.key.get_pressed()[pygame.K_DOWN] == 1:
                self.player.move(3, self.side_sprites, self.boxes_sprites,
                                 down=True)
            if pygame.key.get_pressed()[pygame.K_LEFT] == 1:
                self.player.move(3, self.side_sprites, self.boxes_sprites,
                                 right=True)

            self.screen.fill(self.bg_color)

            self.all_sprites.draw(self.screen)
            self.ui_sprites.draw(self.screen)
            self.ui_sprites.update(f'Your score: {self.player.score}')
            self.portal_sprite.draw(self.screen)
            self.player_sprite.draw(self.screen)
            self.sword_sprite.draw(self.screen)

            self.camera.update(self.player)

            for sprite in self.all_sprites:
                self.camera.apply(sprite)

            if animate_index % 6 == 0:
                self.player_sprite.update()

            if animate_index % 12 == 0:
                self.enemy_sprites.update(self.player)

            if animate_index % 24 == 0:
                self.animated_sprites.update()
                self.portal_sprite.update(self.player)

                for enemy_sprite in self.enemy_sprites:
                    enemy_sprite.check_player(self.player)

            health = self.player.health
            for sprite in self.ui_sprites:
                if isinstance(sprite, UI.Heart):
                    if not health - 2 >= 0:
                        if health - 2 == -1:
                            sprite.image = sprite.half_heart
                        elif health - 2 <= -2:
                            sprite.image = sprite.empty_heart
                    else:
                        sprite.image = sprite.full_heart
                    health -= 2
                print(health)

            animate_index += 1

            if self.player.health <= 0 or self.player.die:
                self.player.die = True
                self.game_over()
                return None

            if self.player.next_level:
                self.player.next_level = True
                self.next_level()
                return None

            self.clock.tick(self.FPS)
            pygame.display.flip()

    def load_map(self, field) -> tuple:
        player_x, player_y = None, None  # player x and player y
        portal_x, portal_y = None, None

        enemies_coordinates = []
        boxes_coordinates = []
        potions_coordinates = []
        for row in range(field.get_width()):
            for column in range(field.get_width()):
                if isinstance(field.get_room(row, column), Room):
                    level = generate_level(field.get_room(row, column))

                    for y in range(len(level)):
                        for x in range(len(level[row])):
                            if isinstance(level[y][x], list):
                                for tile in level[y][x]:
                                    self.load_tile(
                                        tile, x + column * self.k,
                                        y + row * self.k
                                    )
                            else:
                                if level[y][x] == 'player':
                                    player_x = x + column * self.k
                                    player_y = y + row * self.k
                                    self.load_tile(
                                        self.floor, x + column * self.k,
                                        y + row * self.k
                                    )
                                else:
                                    if level[y][x].name == 'portal':
                                        portal_x = x + column * self.k
                                        portal_y = y + row * self.k
                                        self.load_tile(
                                            self.floor, x + column * self.k,
                                            y + row * self.k
                                        )
                                    elif level[y][x].type.startswith('enemy'):
                                        enemies_coordinates.append(
                                            (x + column * self.k,
                                             y + row * self.k)
                                        )
                                        self.load_tile(
                                            self.floor, x + column * self.k,
                                            y + row * self.k
                                        )
                                    elif level[y][x].type.startswith('items'):
                                        if level[y][x].name == 'box':
                                            boxes_coordinates.append(
                                                (x + column * self.k,
                                                 y + row * self.k, level[y][x])
                                            )
                                            self.load_tile(
                                                self.floor,
                                                x + column * self.k,
                                                y + row * self.k
                                            )
                                        elif level[y][x].name == 'potion':
                                            potions_coordinates.append(
                                                (x + column * self.k,
                                                 y + row * self.k)
                                            )
                                            self.load_tile(
                                                self.floor,
                                                x + column * self.k,
                                                y + row * self.k
                                            )
                                    else:
                                        self.load_tile(
                                            level[y][x], x + column * self.k,
                                            y + row * self.k
                                        )

        Portal.Portal(portal_x, portal_y, self.portal_sprite, self.all_sprites)

        for enemy_x, enemy_y in enemies_coordinates:
            Enemy.Enemy(
                self.tiles['enemy']['enemy'], enemy_x, enemy_y,
                self.enemy_sprites, self.all_sprites
            )

        for tile in boxes_coordinates:
            self.load_tile(tile[2], tile[0], tile[1])

        for potion_x, potion_y in potions_coordinates:
            Potion.Potion(
                potion_x, potion_y, self.potion_sprites, self.all_sprites
            )

        return player_x, player_y

    def load_tile(self, tile: namedtuple, x, y):
        if 'sides' in tile.type:
            Tile.Tile(
                tile, self.tiles, self.all_sprites, self.side_sprites, x, y
            )
        elif tile.type.startswith('floor'):
            Tile.Tile(
                tile, self.tiles, self.all_sprites, self.floor_sprites, x, y
            )
        elif tile.type.startswith('animated'):
            if tile.name.startswith('spikes'):
                AnimatedTile.AnimatedTile(
                    self.tiles[tile.type][tile.name], 1, 4, x, y,
                    self.animated_sprites, self.all_sprites
                )
        elif tile.type.startswith('items'):
            Tile.Tile(
                tile, self.tiles, self.all_sprites, self.boxes_sprites, x, y
            )

    def next_level(self):
        self.ui_sprites.empty()
        self.all_sprites.empty()
        self.enemy_sprites.empty()
        self.player_sprite.empty()
        self.sword_sprite.empty()
        self.boxes_sprites.empty()
        self.potion_sprites.empty()
        self.animated_sprites.empty()

        self.player_health = self.player.health
        self.player_score = self.player.score
        self.player = None
        self.game()

    def game_over(self):
        self.ui_sprites.empty()
        self.all_sprites.empty()
        self.enemy_sprites.empty()
        self.player_sprite.empty()
        self.sword_sprite.empty()
        self.boxes_sprites.empty()
        self.potion_sprites.empty()
        self.animated_sprites.empty()

        self.player_health = 20
        self.player = None

        self.screen.fill(self.bg_color)
        text = ['GAME', 'OVER']
        button_classes = []

        for i in range(len(text)):
            line = text[i]
            font = pygame.font.Font(os.path.join('data', 'font.ttf'), 100)

            rendered_line = font.render(line, 1, pygame.Color('yellow'))
            line_rect = rendered_line.get_rect()
            line_rect.x = self.window_width // 2 - line_rect.width // 2
            line_rect.y = i * 130 + 100
            self.screen.blit(rendered_line, line_rect)

        font = pygame.font.Font(os.path.join('data', 'font.ttf'), 24)
        rendered_line = font.render(
            f'Your score: {self.player_score}', 1, pygame.Color('yellow')
        )
        self.player_score = 0
        line_rect = rendered_line.get_rect()
        line_rect.x = self.window_width // 2 - line_rect.width // 2
        line_rect.y = 400
        self.screen.blit(rendered_line, line_rect)

        button_center = self.window_width // 2
        button_y = 450

        button_classes.append(
            Button.Button(
                (button_center, button_y), self.game_over_button_sprite,
                self.screen, 'Return to main screen',
                type='return to main screen', website=None
            )
        )

        while True:
            for game_over_event in pygame.event.get():
                if game_over_event.type == pygame.QUIT:
                    self.terminate()
                if game_over_event.type == pygame.MOUSEBUTTONDOWN:
                    for button in button_classes:
                        if button.rect.collidepoint(game_over_event.pos):
                            if button.button_type == 'return to main screen':
                                self.menu()
                                return None

            self.game_over_button_sprite.draw(self.screen)
            self.game_over_button_sprite.update()
            pygame.display.flip()

    @staticmethod
    def terminate():
        sys.exit(pygame.quit())


game = Game(1280, 680)
game.start()
