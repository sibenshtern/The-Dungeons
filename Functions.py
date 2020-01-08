import os
import pygame


def load_image(directory, image_name, color_key=None):
    fullname = os.path.join(directory, image_name)
    image = pygame.image.load(fullname)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image.convert_alpha()

    return image
