from __future__ import annotations
from pprint import pprint
from typing import Any
import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

MAP_WIDTH = 7

PREVIOUS_ROOM = 9
END_ROOM = 10
MAIN_ROOM = 11
DOOR_TYPES = [END_ROOM, MAIN_ROOM]


class Room:

    def __init__(self, doors_count: int, row: int, column: int,
                 previous_door=None, description=None):
        self.doors = []

        self.row = row
        self.column = column
        self.doors_count = doors_count

        self.description = description
        self.previous_door = previous_door

    def add_door(self, door: Door) -> None:
        self.doors.append(door)

    def doors_generator(self):
        doors_directions = []

        if self.previous_door is not None:
            if self.previous_door.direction == UP:
                doors_directions.append(DOWN)
            elif self.previous_door.direction == RIGHT:
                doors_directions.append(LEFT)
            elif self.previous_door.direction == DOWN:
                doors_directions.append(UP)
            elif self.previous_door.direction == LEFT:
                doors_directions.append(RIGHT)

        for _ in range(self.doors_count - 1):
            verdict = False
            direction = random.choice(DIRECTIONS)

            while not verdict:
                if direction == UP and self.row - 1 >= 0:
                    if direction not in doors_directions and \
                            field.get_room(self.row - 1, self.column) == 'VD':
                        verdict = True
                    else:
                        direction = random.choice(DIRECTIONS)
                elif direction == RIGHT and self.column + 1 < MAP_WIDTH:
                    if direction not in doors_directions and \
                            field.get_room(self.row, self.column + 1) == 'VD':
                        verdict = True
                    else:
                        direction = random.choice(DIRECTIONS)
                elif direction == DOWN and self.row + 1 < MAP_WIDTH:
                    if direction not in doors_directions and \
                            field.get_room(self.row + 1, self.column) == 'VD':
                        verdict = True
                    else:
                        direction = random.choice(DIRECTIONS)
                elif direction == LEFT and self.column - 1 >= 0:
                    if direction not in doors_directions and \
                            field.get_room(self.row, self.column + 1) == 'VD':
                        verdict = True
                    else:
                        direction = random.choice(DIRECTIONS)
                else:
                    direction = random.choice(DIRECTIONS)

            doors_directions.append(direction)

        doors_count_to_end_room = self.doors_count - 1
        for index in range(len(doors_directions)):
            if index == 0:
                door = Door(doors_directions[index])
                door.set_type(PREVIOUS_ROOM)
                self.doors.append(door)
            else:
                door = Door(doors_directions[index])
                if doors_count_to_end_room > 0:
                    door.set_type(END_ROOM)
                    doors_count_to_end_room -= 1
                else:
                    door.set_type(MAIN_ROOM)
                self.doors.append(door)

    def __repr__(self):
        if self.description is not None:
            return f"'{self.description}'"

    def __str__(self):
        if self.description is not None:
            return self.description
        else:
            return self.__name__


class Door:

    def __init__(self, direction: int):
        self.direction = direction
        self.type = None

    def set_type(self, door_type):
        self.type = door_type


class Field:

    def __init__(self, map_width: int):
        self.rooms = []
        self.width = map_width

        self.field = [['VD'] * self.width for _ in range(self.width)]

    def add_room(self, room) -> None:
        if 0 <= room.row < self.width and 0 <= room.column < self.width:
            self.field[room.row][room.column] = room
            self.rooms.append(room)

    def get_room(self, row: int, column: int) -> Any:
        if 0 <= row < self.width and 0 <= column < self.width:
            return self.field[row][column]


class MainRoom(Room):

    def __init__(self, row: int, column: int, previous_door, description=None):
        super(MainRoom, self).__init__(random.randint(2, 3), row, column,
                                       previous_door, description)
        self.previous_door = previous_door
        self.doors_generator()


class EndRoom(Room):

    def __init__(self, row: int, column: int, previous_door=None,
                 description=None):
        super(EndRoom, self).__init__(1, row, column, previous_door,
                                      description)
        self.doors_generator()

    def doors_generator(self):
        verdict = False
        direction = random.choice(DIRECTIONS)

        if self.previous_door is not None:
            if self.previous_door.direction == UP:
                direction = DOWN
                verdict = True
            elif self.previous_door.direction == RIGHT:
                direction = LEFT
                verdict = True
            elif self.previous_door.direction == DOWN:
                direction = UP
                verdict = True
            elif self.previous_door.direction == LEFT:
                direction = RIGHT
                verdict = True

        door = Door(direction)
        door.set_type(MAIN_ROOM)
        self.doors.append(door)


field = Field(MAP_WIDTH)


def generate_field():
    now_row = random.randint(3, field.width - 4)
    now_column = random.randint(3, field.width - 4)

    field.add_room(EndRoom(now_row, now_column, description='SR'))

    for i in range(9):
        now_room = field.get_room(now_row, now_column)

        for door in now_room.doors:
            if door.type == END_ROOM:
                if door.direction == UP and \
                        field.get_room(now_row - 1, now_column) == 'VD':
                    field.add_room(
                        EndRoom(now_row - 1, now_column, door, 'ER'))
                elif door.direction == RIGHT and \
                        field.get_room(now_row, now_column + 1) == 'VD':
                    field.add_room(
                        EndRoom(now_row, now_column + 1, door, 'ER'))
                elif door.direction == DOWN and \
                        field.get_room(now_row + 1, now_column) == 'VD':
                    field.add_room(
                        EndRoom(now_row + 1, now_column, door, 'ER'))
                elif door.direction == LEFT and \
                        field.get_room(now_row, now_column + 1) == 'VD':
                    field.add_room(
                        EndRoom(now_row, now_column - 1, door, 'ER'))
            elif door.type == MAIN_ROOM:
                if door.direction == UP and \
                        field.get_room(now_row - 1, now_column) == 'VD':
                    field.add_room(
                        MainRoom(now_row - 1, now_column, door, 'MR'))
                    now_row -= 1
                elif door.direction == RIGHT and \
                        field.get_room(now_row, now_column + 1) == 'VD':
                    field.add_room(
                        MainRoom(now_row, now_column + 1, door, 'MR'))
                    now_column += 1
                elif door.direction == DOWN and \
                        field.get_room(now_row + 1, now_column) == 'VD':
                    field.add_room(
                        MainRoom(now_row + 1, now_column, door, 'MR'))
                    now_row += 1
                elif door.direction == LEFT and \
                        field.get_room(now_row, now_column - 1) == 'VD':
                    field.add_room(
                        MainRoom(now_row, now_column - 1, door, 'MR'))
                    now_column -= 1

    return field


# pprint(generate_field().field)
