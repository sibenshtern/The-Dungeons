import sys

import pygame


pygame.init()

window_size = WINDOW_WIDTH, WINDOW_HEIGHT = 700, 500
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

FPS = 60
running = True


def terminate():
    sys.exit(pygame.quit())


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

    clock.tick(FPS)
    pygame.display.flip()
