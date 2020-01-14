from Functions import load_image
from collections import namedtuple


def return_tiles():
    tiles = {
        'corners': {
            'top_left': load_image('Tiles\\Sides', 'side_top_left.png'),
            'top_right': load_image('Tiles\\Sides', 'side_top_right.png'),
            'bottom_right': load_image('Tiles\\Sides', 'side_bottom_left.png'),
            'bottom_left': load_image('Tiles\\Sides', 'side_bottom_right.png')
        },
        'top_sides': {
            'left': load_image('Tiles\\Sides', 'top_left.png'),
            'mid': load_image('Tiles\\Sides', 'top_mid.png'),
            'right': load_image('Tiles\\Sides', 'top_right.png')
        },
        'walls_sides': {
            'left': load_image('Tiles\\Sides', 'left.png'),
            'mid': load_image('Tiles\\Sides', 'mid.png'),
            'right': load_image('Tiles\\Sides', 'right.png'),
            'right_corner': load_image('Tiles\\Sides', 'side_front_left.png'),
            'left_corner': load_image('Tiles\\Sides', 'side_front_right.png')
        },
        'sides': {
            'left': load_image('Tiles\\Sides', 'side_mid_left.png'),
            'right': load_image('Tiles\\Sides', 'side_mid_right.png')
        },
        'items': {
            'box': load_image('Tiles\\Items', 'crate.png')
        },
        'floor': [
            load_image('Tiles\\Floor', '1.png'),
            load_image('Tiles\\Floor', '2.png'),
            load_image('Tiles\\Floor', '3.png'),
            load_image('Tiles\\Floor', '5.png'),
        ],
        'animated': {
            'spikes': load_image('Tiles\\Animated', 'spikes_anim.png'),
            'portal': load_image('Tiles\\Animated', 'portal.png')
        },
        'enemy': {
            'wogol': load_image('images', 'wogol_idle_anim.png')
        }
    }

    return tiles
