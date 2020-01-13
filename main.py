import os
import sys
import webbrowser
from collections import namedtuple

import pygame

import UI
from Tile import Tile
from Button import Button
from Camera import Camera
from Player import Player
from Tiles import return_tiles
from AnimatedTile import AnimatedTile


from Functions import load_image
from NewLevelGenerator1 import generate_level, field


pygame.init()

window_size = WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 680
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
floor = namedtuple('SecondTile', ['type', 'name'])('floor', 0)

animated_sprites = pygame.sprite.Group()
buttons_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
floor_sprites = pygame.sprite.Group()
side_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
ui_sprites = pygame.sprite.Group()

tiles = return_tiles()
field_map = field
player = None

FPS = 60
k = 19
running = True


def main_menu():
    """
    Function which show main menu (also start screen)
    :return: None
    """

    screen.fill(pygame.Color(29, 16, 70))

    # create header
    header = "The Dungeons"

    font = pygame.font.Font(os.path.join('data', 'font.ttf'), 60)

    rendered_header = font.render(header, 1, pygame.Color('yellow'))
    header_rect = rendered_header.get_rect()
    header_rect.x = WINDOW_WIDTH // 2 - header_rect.width // 2
    header_rect.y = 48

    screen.blit(rendered_header, header_rect)

    # create buttons
    buttons = ['Start Game', 'Settings']
    button_classes = []

    for i in range(len(buttons)):
        button_center = WINDOW_WIDTH // 2
        button_y = 131 + (16 * (i + 1)) + 64 * i

        button = Button((button_center, button_y), buttons_sprites, screen,
                        buttons[i], type=buttons[i].lower(), website=None)
        button_classes.append(button)

    button_center = WINDOW_WIDTH - 112
    button_y = WINDOW_HEIGHT - 96

    button_classes.append(
        Button(
            (button_center, button_y), buttons_sprites, screen, 'Github',
            type='open_website', website='Github'
        )
    )

    # main cycle in function
    while True:
        for menu_event in pygame.event.get():
            if menu_event.type == pygame.QUIT:
                terminate()
            if menu_event.type == pygame.MOUSEBUTTONDOWN:
                for button in button_classes:
                    if button.rect.collidepoint(menu_event.pos):
                        if button.button_type == 'open_website':
                            webbrowser.open('https://github.com/sibenshtern')
                        if button.button_type == 'start game':
                            start_game()
                            return

        buttons_sprites.draw(screen)
        buttons_sprites.update()
        pygame.display.flip()


def start_game():
    load_map(field_map)

    anim_index = 0

    for i in range(10):
        UI.Heart((32 + i * 24, 32), ui_sprites)

    pygame.mixer.music.load(os.path.join('data', 'soundtrack1.mp3'))
    pygame.mixer.music.play(10)
    pygame.mixer.music.set_volume(0.009)

    while True:
        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                terminate()

        if pygame.key.get_pressed()[273] == 1:
            # player.rect.y -= 5
            player.move(2, side_sprites, up=True)
        if pygame.key.get_pressed()[275] == 1:
            # player.rect.x += 5
            player.move(2, side_sprites, left=True)
        if pygame.key.get_pressed()[276] == 1:
            # player.rect.x -= 5
            player.move(2, side_sprites, right=True)
        if pygame.key.get_pressed()[274] == 1:
            # player.rect.y += 5
            player.move(2, side_sprites, down=True)

        screen.fill(pygame.Color(29, 16, 70))

        all_sprites.draw(screen)
        ui_sprites.draw(screen)
        camera.update(player)

        for sprite in all_sprites:
            camera.apply(sprite)

        if anim_index % 6 == 0:
            player_sprites.update()

        if anim_index % 24 == 0:
            animated_sprites.update()

        health = player.health
        for sprite in ui_sprites:
            if not health - 2 >= 0:
                if health - 2 == -1:
                    sprite.image = sprite.half_heart
                elif health - 2 <= -2:
                    sprite.image = sprite.empty_heart

            health -= 2

        anim_index += 1

        clock.tick(FPS)
        pygame.display.flip()


def terminate():
    sys.exit(pygame.quit())


def load_map(level_map):
    global player

    x, y = None, None
    player_x, player_y = None, None
    create_player = False

    for column in range(len(level_map.field)):
        for row in range(len(level_map.field[column])):
            if not field.get_room(row, column) == 'VD':
                level = generate_level(field.get_room(row, column))

                for y in range(len(level)):
                    for x in range(len(level[y])):
                        if isinstance(level[y][x], list):
                            for tile in level[y][x]:
                                if "sides" in tile.type:
                                    Tile(tile, tiles, all_sprites,
                                         side_sprites, x + column * k,
                                         y + row * k)
                                elif "floor" in tile.type:
                                    Tile(tile, tiles, all_sprites,
                                         floor_sprites, x + column * k,
                                         y + row * k)
                        else:
                            if level[y][x] == 'player':
                                create_player = True
                                player_x = x + column * k
                                player_y = y + row * k
                                Tile(floor, tiles, all_sprites,
                                     floor_sprites, x + column * k,
                                     y + row * k)
                            else:
                                if "sides" in level[y][x].type:
                                    Tile(level[y][x], tiles, all_sprites,
                                         side_sprites, x + column * k,
                                         y + row * k)
                                elif "floor" in level[y][x].type:
                                    Tile(level[y][x], tiles, all_sprites,
                                         floor_sprites, x + column * k,
                                         y + row * k)
                                elif "animated" in level[y][x].type:
                                    AnimatedTile(
                                        tiles[level[y][x].type]
                                        [level[y][x].name],
                                        1, 4, x + column * k, y + row * k,
                                        animated_sprites, all_sprites
                                    )

    if create_player:
        player = Player(
            load_image('images', 'idle_anim.png'),
            load_image('images', 'run_anim.png'),
            1, 4, player_x, player_y,
            player_sprites, all_sprites, animated_sprites
        )


main_menu()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

    clock.tick(FPS)
    pygame.display.flip()
