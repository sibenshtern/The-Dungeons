import os
import sys
import webbrowser

import pygame

from Button import Button
from Tiles import return_tiles


pygame.init()

window_size = WINDOW_WIDTH, WINDOW_HEIGHT = 700, 500
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
buttons_sprites = pygame.sprite.Group()
tiles = return_tiles()

FPS = 60
running = True


def main_menu():
    """
    Function which show main menu (also start screen)
    :return: None
    """

    screen.fill(pygame.Color('white'))

    # create header
    header = "The Dungeons"

    font = pygame.font.Font(os.path.join('data', 'font.ttf'), 60)

    rendered_header = font.render(header, 1, pygame.Color('yellow'))
    header_rect = rendered_header.get_rect()
    header_rect.x = WINDOW_WIDTH // 2 - header_rect.width // 2
    header_rect.y = 48

    screen.blit(rendered_header, header_rect)

    # create buttons
    buttons = ['Start Game', 'Record Table', 'Settings']
    button_classes = []

    for i in range(len(buttons)):
        button_center = WINDOW_WIDTH // 2
        button_y = 131 + (16 * (i + 1)) + 64 * i

        button = Button((button_center, button_y), buttons_sprites, screen,
                        buttons[i], type=None, website=None)
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

        buttons_sprites.draw(screen)
        buttons_sprites.update()
        pygame.display.flip()


def terminate():
    sys.exit(pygame.quit())


main_menu()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

    clock.tick(FPS)
    pygame.display.flip()
