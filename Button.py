import os
import pygame
from Functions import load_image


class Button(pygame.sprite.Sprite):

    def __init__(self, coordinates, group, screen, label=None, **kwargs):
        super(Button, self).__init__(group)

        # Main attributes
        self.width = 256
        self.height = 64
        self.coordinates = self.center, self.y = coordinates

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.button_type = kwargs['type']
        self.website = kwargs['website']

        # Text settings
        text = label
        font = pygame.font.Font(os.path.join('data', 'font.ttf'), 24)

        # Text when the cursor is not above the button
        self.unpressed_text = font.render(text, 1, (37, 37, 39))
        self.unpressed_text_rect = self.unpressed_text.get_rect()

        upt_width = self.unpressed_text_rect.width
        upt_height = self.unpressed_text_rect.height

        self.unpressed_text_rect.x = self.center - upt_width / 2
        self.unpressed_text_rect.y = self.y + self.height / 2 - upt_height / 2

        # Text, when the cursor is above the button
        self.pressed_text = font.render(text, 1, (109, 98, 92))
        self.pressed_text_rect = self.pressed_text.get_rect()

        pt_width = self.pressed_text_rect.width
        pt_height = self.pressed_text_rect.height

        self.pressed_text_rect.x = self.center - pt_width / 2
        self.pressed_text_rect.y = self.y + self.height / 2 - pt_height / 2

        # Image settings
        self.image = load_image('images', 'button.png')
        self.image = pygame.transform.scale(self.image, (upt_width + 30, 64))

        self.rect = self.image.get_rect()
        self.rect.x = self.center - upt_width // 2 - 15
        self.rect.y = self.y

    def update(self, *args):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.pressed_text, self.pressed_text_rect)
        else:
            self.screen.blit(self.unpressed_text, self.unpressed_text_rect)
