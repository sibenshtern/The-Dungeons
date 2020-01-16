from __future__ import annotations
import os
import sys
import webbrowser
from collections import namedtuple

import pygame

# import classes from other files
import UI
import Tile
import Enemy
import Tiles
import Portal
import Button
import Camera
import Player
import AnimatedTile

from Functions import load_image
from LevelGenerator import generate_level
from MapGenerator import generate_field, Room


pygame.init()

# usual pygame's variables
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 680
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

camera = Camera.Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
floor = namedtuple('Floor', ['type', 'name'])('floor', 0)

# sprites
gameover_button_sprites = pygame.sprite.GroupSingle()
portal_sprites = pygame.sprite.GroupSingle()
main_button_sprites = pygame.sprite.Group()
animated_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
floor_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
side_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
ui_sprites = pygame.sprite.Group()
# seem's funny, but it's scaring

tiles = Tiles.return_tiles()
game_map = generate_field()
player_health = 20
player_score = 0
player = None


FPS = 60
k = 19  # need for right room's drawing
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
    header_rect.y = 70
    screen.blit(rendered_header, header_rect)

    # create buttons
    buttons = ['Start Game', 'Record table']
    button_classes = []

    for i in range(len(buttons)):
        button_center = WINDOW_WIDTH // 2
        button_y = 269 + (16 * (i + 1)) + 64 * i

        button = Button.Button(
            (button_center, button_y), main_button_sprites, screen, buttons[i],
            type=buttons[i].lower(), website=None
        )
        button_classes.append(button)

    button_center = WINDOW_WIDTH - 112
    button_y = WINDOW_HEIGHT - 96

    button_classes.append(
        Button.Button(
            (button_center, button_y), main_button_sprites, screen, 'Github',
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
                            game()
                            return

        main_button_sprites.draw(screen)
        main_button_sprites.update()
        pygame.display.flip()


def terminate():
    sys.exit(pygame.quit())


def load_map(field):
    player_x, player_y = None, None
    portal_x, portal_y = None, None

    enemies_coordinates = []
    for row in range(field.get_width()):
        for column in range(field.get_width()):
            if isinstance(field.get_room(row, column), Room):
                level = generate_level(field.get_room(row, column))
                for y in range(len(level)):
                    for x in range(len(level[y])):
                        if isinstance(level[y][x], list):
                            for tile in level[y][x]:
                                if 'sides' in tile.type:
                                    Tile.Tile(tile, tiles, all_sprites,
                                              side_sprites,
                                              x + column * k, y + row * k)
                                elif 'floor' in tile.type:
                                    Tile.Tile(tile, tiles, all_sprites,
                                              floor_sprites,
                                              x + column * k, y + row * k)
                        else:
                            if level[y][x] == 'player':
                                player_x = x + column * k
                                player_y = y + row * k
                                Tile.Tile(floor, tiles, all_sprites,
                                          floor_sprites,
                                          x + column * k, y + row * k)
                            else:
                                if 'sides' in level[y][x].type:
                                    Tile.Tile(
                                        level[y][x], tiles, all_sprites,
                                        side_sprites,
                                        x + column * k, y + row * k
                                    )
                                elif 'floor' in level[y][x].type:
                                    Tile.Tile(
                                        level[y][x], tiles, all_sprites,
                                        floor_sprites,
                                        x + column * k, y + row * k
                                    )
                                elif 'animated' in level[y][x].type:
                                    if 'spikes' in level[y][x].name:
                                        tile_type = level[y][x].type
                                        tile_name = level[y][x].name
                                        AnimatedTile.AnimatedTile(
                                            tiles[tile_type][tile_name],
                                            1, 4, x + column * k, y + row * k,
                                            animated_sprites, all_sprites
                                        )
                                    elif level[y][x].name.startswith('portal'):
                                        portal_x = x + column * k
                                        portal_y = y + row * k
                                        Tile.Tile(
                                            floor, tiles, all_sprites,
                                            floor_sprites, x + column * k,
                                            y + row * k
                                        )
                                elif 'enemy' in level[y][x].type:
                                    enemies_coordinates.append(
                                        (x + (column * k), y + (row * k))
                                    )
                                    Tile.Tile(
                                        floor, tiles, all_sprites,
                                        floor_sprites, x + column * k,
                                        y + row * k
                                    )

    Portal.Portal(portal_x, portal_y, portal_sprites, all_sprites)

    for enemy_x, enemy_y in enemies_coordinates:
        Enemy.Enemy(
            tiles['enemy']['enemy'], enemy_x, enemy_y,
            enemy_sprites, all_sprites
        )

    return player_x, player_y


def game():
    global player

    player_x, player_y = load_map(game_map)
    player = Player.Player(
        load_image('images', 'idle_anim.png'), player_x, player_y, 1, 4,
        player_sprites, all_sprites, animated_sprites, player_health,
        player_score
    )
    anim_index = 0

    for index in range(10):
        UI.Heart((32 + index * 24, 32), ui_sprites)

    UI.Text(f'Your score: {player.score}', ui_sprites)

    pygame.mixer.music.load(os.path.join('data', 'soundtrack1.mp3'))
    pygame.mixer.music.play(10)
    pygame.mixer.music.set_volume(0.009)

    while True:
        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                terminate()

        if pygame.key.get_pressed()[pygame.K_UP] == 1:
            player.move(3, side_sprites, up=True)
        if pygame.key.get_pressed()[pygame.K_RIGHT] == 1:
            player.move(3, side_sprites, left=True)
        if pygame.key.get_pressed()[pygame.K_LEFT] == 1:
            player.move(3, side_sprites, right=True)
        if pygame.key.get_pressed()[pygame.K_DOWN] == 1:
            player.move(3, side_sprites, down=True)

        screen.fill(pygame.Color(29, 16, 70))

        all_sprites.draw(screen)
        ui_sprites.draw(screen)
        ui_sprites.update(f'Your score: {player.score}')
        portal_sprites.draw(screen)
        player_sprites.draw(screen)
        camera.update(player)

        for sprite in all_sprites:
            camera.apply(sprite)

        if anim_index % 6 == 0:
            player_sprites.update()
            enemy_sprites.update(player)

        if anim_index % 24 == 0:
            animated_sprites.update()
            portal_sprites.update(player)

        health = player.health
        for sprite in ui_sprites:
            if isinstance(sprite, UI.Heart):
                if not health - 2 >= 0:
                    if health - 2 == -1:
                        sprite.image = sprite.half_heart
                    elif health - 2 <= -2:
                        sprite.image = sprite.empty_heart
                    else:
                        sprite.image = sprite.full_heart

                health -= 2

        anim_index += 1

        if player.health <= 0 or player.die:
            player.die = True
            game_over()
            return

        if player.next_level:
            player.next_level = False
            next_level()
            return

        clock.tick(FPS)
        pygame.display.flip()


def next_level():
    global player, game_map, player_health, player_score

    all_sprites.empty()
    player_sprites.empty()
    animated_sprites.empty()
    ui_sprites.empty()
    enemy_sprites.empty()
    game_map = generate_field()
    player_health = player.health
    player_score = player.score
    player = None
    game()


def game_over():
    global player, game_map, player_health, player_score

    all_sprites.empty()
    player_sprites.empty()
    animated_sprites.empty()
    ui_sprites.empty()
    enemy_sprites.empty()
    game_map = generate_field()
    player_health = 20
    player = None

    screen.fill(pygame.Color(29, 16, 70))
    text = ['GAME', 'OVER']
    button_classes = []

    for i in range(len(text)):
        line = text[i]
        font = pygame.font.Font(os.path.join('data', 'font.ttf'), 100)

        rendered_line = font.render(line, 1, pygame.Color('yellow'))
        line = rendered_line.get_rect()
        line.x = WINDOW_WIDTH // 2 - line.width // 2
        line.y = i * 130 + 100
        screen.blit(rendered_line, line)

    font = pygame.font.Font(os.path.join('data', 'font.ttf'), 24)
    rendered_line = font.render(f'Your score: {player_score}', 1,
                                pygame.Color('yellow'))
    player_score = 0
    line = rendered_line.get_rect()
    line.x = WINDOW_WIDTH // 2 - line.width // 2
    line.y = 400
    screen.blit(rendered_line, line)

    button_center = WINDOW_WIDTH // 2
    button_y = 450

    button_classes.append(
        Button.Button(
            (button_center, button_y), gameover_button_sprites, screen,
            'Return to main screen',
            type='return to main screen', website=None
        )
    )

    while True:
        for menu_event in pygame.event.get():
            if menu_event.type == pygame.QUIT:
                terminate()
            if menu_event.type == pygame.MOUSEBUTTONDOWN:
                for button in button_classes:
                    if button.rect.collidepoint(menu_event.pos):
                        if button.button_type == 'return to main screen':
                            main_menu()
                            return

        gameover_button_sprites.draw(screen)
        gameover_button_sprites.update()
        pygame.display.flip()


main_menu()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pass

    clock.tick(FPS)
    pygame.display.flip()
