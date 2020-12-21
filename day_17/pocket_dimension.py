__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from typing import Tuple, List
from itertools import product

################################################################################

class PocketDimension(object):

    CUBE_ACTIVE = '#'
    CUBE_INACTIVE = '.'

################################################################################

    def __init__(self):
        with open("day_17/input.txt", 'r') as f:
            self._cubes = []
            lines = [line.strip() for line in f.readlines()]
            [self._cubes.append(Cube(i, j, 0, lines[i][j] == self.CUBE_ACTIVE))
             for i in range(len(lines))
             for j in range(len(lines[i]))]
            print("prdel", len(self._cubes))
            self._enclose()
            print("prdel", len(self._cubes))

################################################################################

    def execute_cycle(self):
        """

        """

        pass

################################################################################

    def contains_cube(self, x, y, z):
        """

        """

        return any([cube.x == x and cube.y == y and cube.z == z
                    for cube in self._cubes])

################################################################################

    def get_cube(self, x, y, z):
        """

        """

        try:
            return [cube for cube in self._cubes if cube.x == x and cube.y == y and cube.z == z][0]
        except IndexError:
            return None

################################################################################

    def _enclose(self):
        """

        """

        while True:
            cubes_to_enclose = [
                cube
                for cube in self._cubes
                for neighbour in cube.neighbours
                if not self.contains_cube(neighbour[0], neighbour[1],
                                          neighbour[2])]
            try:
                cube = cubes_to_enclose[0]
                [self._cubes.append(
                    Cube(neighbour[0], neighbour[1], neighbour[2], False))
                    for neighbour in cube.neighbours
                    if not self.contains_cube(
                    neighbour[0], neighbour[1], neighbour[2])]
            except IndexError:
                break

################################################################################

class Cube(object):

    def __init__(self, x, y, z, is_active):
        """

        """

        self._x = x
        self._y = y
        self._z = z
        self._is_active = is_active
        self._is_about_to_change = False

################################################################################

    @property
    def is_active(self):
        return self._is_active

################################################################################

    @property
    def x(self):
        return self._x

################################################################################

    @property
    def y(self):
        return self._y

################################################################################

    @property
    def z(self):
        return self._z

################################################################################

    @property
    def neighbours(self): # -> Tuple[Tuple[int]]:
        """

        """

        result = list(product((self._x - 1, self._x, self._x + 1),
                              (self._y - 1, self._y, self._y + 1),
                              (self._z - 1, self._z, self._z + 1)))
        result.remove((self._x, self._y, self._z))
        return tuple(result)

################################################################################

    def set_to_change(self):
        self._is_about_to_change = True

################################################################################

    def apply_change(self):
        self._is_active = not self._is_active
        self._is_about_to_change = False

################################################################################
