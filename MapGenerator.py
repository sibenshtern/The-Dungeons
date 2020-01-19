from __future__ import annotations
from pprint import pprint
from typing import Union
import random

UP = 'up'
RIGHT = 'right'
DOWN = 'down'
LEFT = 'left'
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

MAP_WIDTH = 7

PREVIOUS_ROOM = 'previous_room'
END_ROOM = 'end_room'
MAIN_ROOM = 'main_room'
DOOR_TYPES = [END_ROOM, MAIN_ROOM]


class Room:

    def __init__(self, doors_count: int, row: int, column: int, field: Field,
                 description, previous_door):
        self.doors = []

        self.row = row
        self.column = column
        self.doors_count = doors_count

        self.description = description
        self.previous_door: Door = previous_door

        self.field: Field = field

    def get_row(self) -> int:
        return self.row

    def get_column(self) -> int:
        return self.column

    def get_doors(self) -> list:
        return self.doors

    def get_doors_count(self) -> int:
        return self.doors_count

    def get_description(self) -> str:
        return self.description

    def get_previous_door(self) -> Door:
        return self.previous_door

    def set_description(self, description):
        self.description = description

    def generate_doors(self):
        doors_directions = []

        if self.get_previous_door() is not None:
            previous_door = self.get_previous_door()

            if previous_door.get_direction() == UP:
                doors_directions.append(DOWN)
            elif previous_door.get_direction() == RIGHT:
                doors_directions.append(LEFT)
            elif previous_door.get_direction() == DOWN:
                doors_directions.append(UP)
            elif previous_door.get_direction() == LEFT:
                doors_directions.append(RIGHT)

        for _ in range(self.doors_count - 1):
            verdict = False
            direction = random.choice(DIRECTIONS)

            count = 0
            while not verdict:
                if direction == UP and self.get_row() - 1 >= 0:
                    if direction not in doors_directions and \
                            self.field.check(
                                self.get_row() - 1,
                                self.get_column()
                            ):
                        verdict = True
                    else:
                        direction = random.choice(DIRECTIONS)
                elif direction == RIGHT and self.column + 1 < MAP_WIDTH:
                    if direction not in doors_directions and \
                            self.field.check(
                                self.get_row(),
                                self.get_column() + 1
                            ):
                        verdict = True
                    else:
                        direction = random.choice(DIRECTIONS)
                elif direction == DOWN and self.row + 1 < MAP_WIDTH:
                    if direction not in doors_directions and \
                            self.field.check(
                                self.get_row(),
                                self.get_column()
                            ):
                        verdict = True
                    else:
                        direction = random.choice(DIRECTIONS)
                elif direction == LEFT and self.column - 1 >= 0:
                    if direction not in doors_directions and \
                            self.field.check(
                                self.get_row(),
                                self.get_column()
                            ):
                        verdict = True
                    else:
                        direction = random.choice(DIRECTIONS)

                if count > 999:
                    verdict = False
                    break
                count += 1

            if verdict:
                doors_directions.append(direction)

        self.doors_count = len(doors_directions)

        doors_count_to_end_room = self.get_doors_count() - random.randint(1, 2)
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
        return f"'{self.description}'"

    def __str__(self):
        return f"'{self.description}'"


class MainRoom(Room):

    def __init__(self, row: int, column: int, field: Field, previous_door):
        super(MainRoom, self).__init__(random.randint(2, 4), row, column, field,
                                       'MR', previous_door)
        self.generate_doors()


class EndRoom(Room):

    def __init__(self, row: int, column: int, field: Field, description,
                 previous_door: Union[None, Door] = None):
        super(EndRoom, self).__init__(1, row, column, field, description,
                                      previous_door)
        self.generate_doors()

    def generate_doors(self):
        direction = random.choice(DIRECTIONS)

        if self.previous_door is not None:
            if self.previous_door.get_direction() == UP:
                direction = DOWN
            elif self.previous_door.get_direction() == RIGHT:
                direction = LEFT
            elif self.previous_door.get_direction() == DOWN:
                direction = UP
            elif self.previous_door.get_direction() == LEFT:
                direction = RIGHT

            door = Door(direction)
            door.set_type(PREVIOUS_ROOM)
            self.doors.append(door)
        else:
            door = Door(random.choice(DIRECTIONS))
            door.set_type(MAIN_ROOM)
            self.doors.append(door)


class Door:

    def __init__(self, direction: str):
        self.direction = direction
        self.type = None

    def get_direction(self) -> str:
        return self.direction

    def get_type(self) -> Union[None, str]:
        return self.type

    def set_type(self, door_type) -> None:
        self.type = door_type


class Field:

    def __init__(self, map_width: int):
        self.rooms = []
        self.width = map_width

        self.field = [['VD'] * self.width for _ in range(self.width)]

    def get_room(self, row, column) -> Union[Room, str]:
        if self.in_range(row, column):
            return self.field[row][column]

    def get_rooms(self) -> list:
        return self.rooms

    def get_width(self) -> int:
        return self.width

    def get_field(self) -> list:
        return self.field

    def add_room(self, room: Room) -> None:
        if self.in_range(room.get_row(), room.get_column()):
            self.field[room.get_row()][room.get_column()] = room
            self.rooms.append(room)

    def in_range(self, row, column):
        return 0 <= row < self.width and 0 <= column < self.width

    def check(self, row, column):
        return self.get_room(row, column) == 'VD'


def generate_field():
    field = Field(MAP_WIDTH)
    row = random.randint(3, 4)
    column = random.randint(3, 4)

    sx = row
    sy = column

    field.add_room(EndRoom(row, column, field, 'SR'))

    for i in range(20):
        room = field.get_room(row, column)

        door: Door
        for door in room.get_doors():
            if door.get_type() == END_ROOM:
                if door.get_direction() == UP and field.check(row - 1, column):
                    field.add_room(EndRoom(row - 1, column, field, 'ER', door))
                elif door.get_direction() == RIGHT and field.check(row,
                                                                   column + 1):
                    field.add_room(EndRoom(row, column + 1, field, 'ER', door))
                elif door.get_direction() == DOWN and field.check(row + 1,
                                                                  column):
                    field.add_room(EndRoom(row + 1, column, field, 'ER', door))
                elif door.get_direction() == LEFT and field.check(row,
                                                                  column - 1):
                    field.add_room(EndRoom(row, column - 1, field, 'ER', door))
            elif door.get_type() == MAIN_ROOM:
                if door.get_direction() == UP and field.check(row - 1, column):
                    field.add_room(MainRoom(row - 1, column, field, door))
                    row -= 1
                elif door.get_direction() == RIGHT and field.check(row,
                                                                   column + 1):
                    field.add_room(MainRoom(row, column + 1, field, door))
                    column += 1
                elif door.get_direction() == DOWN and field.check(row + 1,
                                                                  column):
                    field.add_room(MainRoom(row + 1, column, field, door))
                    row += 1
                elif door.get_direction() == LEFT and field.check(row,
                                                                  column - 1):
                    field.add_room(MainRoom(row, column - 1, field, door))
                    column -= 1

    k = -1
    need_x = 0
    need_y = 0
    verdict = False

    for row in range(len(field.field)):
        for column in range(len(field.field[row])):
            if isinstance(field.get_room(row, column), EndRoom):
                x = abs(row - sx)
                y = abs(column - sy)
                if (x + y) ** 2 > k:
                    k = (x + y) ** 2
                    need_x = row
                    need_y = column
                    verdict = True

    if verdict:
        field.field[need_x][need_y].description = 'PR'

    for room in field.get_rooms():
        if isinstance(room, EndRoom) and room.description not in ['SR', 'PR']:
            room.set_description('CR')

    return field


if __name__ == '__main__':
    new_field = generate_field()
    print_field = new_field.field
    rooms = new_field.get_rooms()
    pprint(new_field)
    pprint(print_field)
    pprint(rooms)
