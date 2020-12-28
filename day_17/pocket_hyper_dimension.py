__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from itertools import product

################################################################################

class PocketDimension(object):

    CUBE_ACTIVE = '#'
    CUBE_INACTIVE = '.'

################################################################################

    def __init__(self):
        with open("day_17/input.txt", 'r') as f:
            self._dimension = [[[]]]
            lines = [line.strip() for line in f.readlines()]
            [self._dimension[0][0].append(line) for line in lines]
            self._hyper_planes = 1
            self._planes = 1
            self._rows = len(lines)
            self._columns = len(lines[0])

################################################################################

    @property
    def active_cubes_count(self) -> int:
        """

        :return:
        """

        return len([self._dimension[hyper_plane][plane][row][column]
                    for hyper_plane in range(self._hyper_planes)
                    for plane in range(self._planes)
                    for row in range(self._rows)
                    for column in range(self._columns)
                    if self._dimension[hyper_plane][plane][row][column] == self.CUBE_ACTIVE])

################################################################################

    def execute_cycle(self):
        """

        """

        self._enclose()
        new_state = []

        for hyper_plane in range(self._hyper_planes):
            new_hyper_plane = []
            for plane in range(self._planes):
                new_plane = []
                for row in range(self._rows):
                    new_row = ''
                    for column in range(self._columns):
                        active_neighbours = self._get_active_neighbours(hyper_plane, plane, row, column)
                        if self._dimension[hyper_plane][plane][row][column] == self.CUBE_ACTIVE:
                            if 2 <= active_neighbours <= 3:
                                new_row += self.CUBE_ACTIVE
                            else:
                                new_row += self.CUBE_INACTIVE
                        elif self._dimension[hyper_plane][plane][row][column] == self.CUBE_INACTIVE:
                            if active_neighbours == 3:
                                new_row += self.CUBE_ACTIVE
                            else:
                                new_row += self.CUBE_INACTIVE
                    new_plane.append(new_row)
                new_hyper_plane.append(new_plane)
            new_state.append(new_hyper_plane)

        self._dimension = new_state
        self._enclose()

################################################################################

    def _get_cube(self, hyper_plane: int, plane: int, row: int, column: int) -> str:
        """

        :param hyper_plane:
        :param plane:
        :param row:
        :param column:
        :return:
        """

        return self._dimension[hyper_plane][plane][row][column]

################################################################################

    def _enclose(self) -> None:
        """

        :return:
        """

        bottom_plane = ''.join(self._dimension[0])
        if any([cube == self.CUBE_ACTIVE for cube in bottom_plane]):
            empty_plane = list([self.CUBE_INACTIVE * self._columns
                                for row in range(self._rows)])
            self._dimension.insert(0, empty_plane)
            self._planes += 1

        top_plane = ''.join(self._dimension[-1])
        if any([cube == self.CUBE_ACTIVE for cube in top_plane]):
            empty_plane = list([self.CUBE_INACTIVE * self._columns
                                for row in range(self._rows)])
            self._dimension.append(empty_plane)
            self._planes += 1

        top = ''.join([plane[0] for plane in self._dimension])
        if any([cube == self.CUBE_ACTIVE for cube in top]):
            [plane.insert(0, self.CUBE_INACTIVE * self._columns)
             for plane in self._dimension]
            self._rows += 1

        bottom = ''.join([plane[-1] for plane in self._dimension])
        if any([cube == self.CUBE_ACTIVE for cube in bottom]):
            [plane.append(self.CUBE_INACTIVE * self._columns)
             for plane in self._dimension]
            self._rows += 1

        left = ''.join([plane[row][0] for plane in self._dimension
                        for row in range(self._rows)])
        if any([cube == self.CUBE_ACTIVE for cube in left]):
            for plane in range(self._planes):
                for row in range(self._rows):
                    self._dimension[plane][row] \
                        = self.CUBE_INACTIVE + self._dimension[plane][row]
            self._columns += 1

        right = ''.join([plane[row][-1] for plane in self._dimension
                         for row in range(self._rows)])
        if any([cube == self.CUBE_ACTIVE for cube in right]):
            for plane in range(self._planes):
                for row in range(self._rows):
                    self._dimension[plane][row] += self.CUBE_INACTIVE
            self._columns += 1

################################################################################

    def _get_active_neighbours(self, hyper_plane: int, plane: int, row: int, column: int) -> int:
        """

        :param hyper_plane:
        :param plane:
        :param row:
        :param column:
        :return:
        """

        coords = list(product((hyper_plane - 1, hyper_plane, hyper_plane + 1),
                              (plane - 1, plane, plane + 1),
                              (row - 1, row, row + 1),
                              (column - 1, column, column + 1)))
        coords.remove((hyper_plane, plane, row, column))

        count = 0
        for coord in coords:
            try:
                hyper_plane = coord[0]
                plane = coord[1]
                row = coord[2]
                column = coord[3]

                if hyper_plane >= 0 and plane >= 0 and row >= 0 and column >= 0 \
                        and self._get_cube(hyper_plane, plane, row, column) == self.CUBE_ACTIVE:
                    count += 1
            except IndexError:
                pass

        return count

################################################################################
