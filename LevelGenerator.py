from __future__ import annotations
from collections import namedtuple
from random import choice, randint

from MapGenerator import Field, generate_field

Cell = namedtuple('Cell', ['sprites'])
Tile = namedtuple('Tile', ['type', 'name'])

tiles = {
    'corners': [
        Tile('corners', 'top_left'), Tile('corners', 'top_right'),
        Tile('corners', 'bottom_right'), Tile('corners', 'bottom_left')
    ],
    'top_sides': [
        Tile("top_sides", 'left'),
        Tile("top_sides", 'mid'),
        Tile("top_sides", 'right')
    ],
    'walls_sides': [
        Tile("walls_sides", 'left'),
        Tile("walls_sides", 'mid'),
        Tile("walls_sides", 'right'),
        Tile("walls_sides", 'right_corner'),
        Tile("walls_sides", 'left_corner')
    ],
    'sides': [
        Tile("sides", 'left'),
        Tile("sides", 'right'),
    ],
    'floor': [
        Tile('floor', 0),
        Tile('floor', 1),
        Tile('floor', 2),
        Tile('floor', 3)
    ],
    'enemy': [Tile('enemy', 'enemy')],
    'items': [Tile("items", 'box'), Tile('items', 'potion')],
    'animated': [Tile("animated", 'spikes'), Tile('animated', 'portal')]
}


def generate_level(room):
    width = 20
    width -= width % 2

    height = width
    height -= height % 2

    level = [[' '] * width for _ in range(height)]

    level[0][0] = tiles['corners'][0]
    level[0][-1] = tiles['corners'][1]
    level[-1][-1] = tiles['walls_sides'][4]
    level[-1][0] = tiles['walls_sides'][3]

    level[0][1] = tiles['top_sides'][0]
    level[-2][1] = [choice(tiles['floor']), tiles['top_sides'][0]]
    level[0][-2] = tiles['top_sides'][2]
    level[-2][-2] = [choice(tiles['floor']), tiles['top_sides'][2]]

    level[1][1] = tiles['walls_sides'][2]
    level[1][-2] = tiles['walls_sides'][0]

    for index in range(2, width - 2):
        level[0][index] = tiles['top_sides'][1]
        level[1][index] = tiles['walls_sides'][1]
        level[-2][index] = [choice(tiles['floor']), tiles['top_sides'][1]]

    for index in range(1, width - 1):
        level[-1][index] = tiles['walls_sides'][1]

    for index in range(1, height - 1):
        level[index][0] = tiles['sides'][0]
        level[index][-1] = tiles['sides'][1]

    print([door.get_direction() for door in room.doors])

    for door in room.doors:

        direction = door.direction
        center = width // 2

        if direction == 'up':
            for i in range(0, 3):
                for j in range(center - 1, center + 1):
                    level[i][j] = choice(tiles['floor'])
        elif direction == 'right':
            for i in range(center - 1, center + 1):
                level[i][-1] = choice(tiles['floor'])
        elif direction == 'down':
            for i in range(width - 2, width):
                for j in range(center - 1, center + 1):
                    level[i][j] = choice(tiles['floor'])
        elif direction == 'left':
            for i in range(center - 1, center + 1):
                level[i][0] = choice(tiles['floor'])

    for row_index in range(height):
        for column_index in range(width):
            if level[row_index][column_index] == ' ':
                level[row_index][column_index] = choice(tiles['floor'])

    if room.description == 'SR':
        level[randint(3, 7)][randint(3, 7)] = 'player'

    if room.description not in ['SR', 'PR', 'CR']:
        for _ in range(7):
            x = randint(4, 14)
            y = randint(4, 14)

            if isinstance(level[x][y], Tile):
                if level[x][y].type == 'floor':
                    level[x][y] = tiles['animated'][0]

        for _ in range(3):
            x = randint(5, 13)
            y = randint(5, 13)

            if isinstance(level[x][y], Tile):
                if level[x][y].type == 'floor':
                    level[x][y] = tiles['enemy'][0]

        for _ in range(5):
            x = randint(3, 15)
            y = randint(3, 15)

            if isinstance(level[x][y], Tile):
                if level[x][y].type == 'floor':
                    level[x][y] = tiles['items'][0]

    if room.description == 'PR':
        level[9][9] = tiles['animated'][1]

    if room.description == 'CR':
        level[8][7] = tiles['items'][1]

    return level
