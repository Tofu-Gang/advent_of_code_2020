__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

################################################################################

class SeatLayout(object):
    SEAT_EMPTY = 'L'
    SEAT_OCCUPIED = '#'
    FLOOR = '.'

    KEY_UP_LEFT = "UP_LEFT"
    KEY_UP = "UP"
    KEY_UP_RIGHT = "UP_RIGHT"
    KEY_LEFT = "LEFT"
    KEY_RIGHT = "RIGHT"
    KEY_DOWN_LEFT = "DOWN_LEFT"
    KEY_DOWN = "DOWN"
    KEY_DOWN_RIGHT = "DOWN_RIGHT"

    KEY_ROW_INCREMENT = "ROW_INCREMENT"
    KEY_COLUMN_INCREMENT = "COLUMN_INCREMENT"

    VISIBLE_DIRECTIONS = {
        KEY_UP_LEFT: {
            KEY_ROW_INCREMENT: -1,
            KEY_COLUMN_INCREMENT: -1,
        },
        KEY_UP: {
            KEY_ROW_INCREMENT: -1,
            KEY_COLUMN_INCREMENT: 0
        },
        KEY_UP_RIGHT: {
            KEY_ROW_INCREMENT: -1,
            KEY_COLUMN_INCREMENT: 1
        },
        KEY_LEFT: {
            KEY_ROW_INCREMENT: 0,
            KEY_COLUMN_INCREMENT: -1
        },
        KEY_RIGHT: {
            KEY_ROW_INCREMENT: 0,
            KEY_COLUMN_INCREMENT: 1
        },
        KEY_DOWN_LEFT: {
            KEY_ROW_INCREMENT: 1,
            KEY_COLUMN_INCREMENT: -1
        },
        KEY_DOWN: {
            KEY_ROW_INCREMENT: 1,
            KEY_COLUMN_INCREMENT: 0
        },
        KEY_DOWN_RIGHT: {
            KEY_ROW_INCREMENT: 1,
            KEY_COLUMN_INCREMENT: 1
        }
    }

################################################################################

    def __init__(self):
        with open("day_11/input.txt", 'r') as f:
            self._seat_layout = [line.strip() for line in f.readlines()]
            self._is_stable = False

################################################################################

    def change_layout_1(self) -> None:
        """
        Apply the rules which make people sit down or leave their seat.
        Applicable for puzzle 1.
        """

        self._is_stable = True
        new_layout = []
        for i in range(len(self._seat_layout)):
            row = self._seat_layout[i]
            new_layout.append([])
            for j in range(len(row)):
                seat = row[j]

                if seat == self.FLOOR:
                    new_layout[i].append(self.FLOOR)
                else:
                    occupied_adjacent_seat_count \
                        = self._occupied_adjacent_seats_count(i, j)
                    if seat == self.SEAT_EMPTY:
                        if occupied_adjacent_seat_count == 0:
                            new_layout[i].append(self.SEAT_OCCUPIED)
                            self._is_stable = False
                        else:
                            new_layout[i].append(self.SEAT_EMPTY)
                    elif seat == self.SEAT_OCCUPIED:
                        if occupied_adjacent_seat_count >= 4:
                            new_layout[i].append(self.SEAT_EMPTY)
                            self._is_stable = False
                        else:
                            new_layout[i].append(self.SEAT_OCCUPIED)

        self._seat_layout = new_layout

################################################################################

    def change_layout_2(self) -> None:
        """
        Apply the rules which make people sit down or leave their seat.
        Applicable for puzzle 2.
        """

        self._is_stable = True
        new_layout = []
        for i in range(len(self._seat_layout)):
            row = self._seat_layout[i]
            new_layout.append([])
            for j in range(len(row)):
                seat = row[j]

                if seat == self.FLOOR:
                    new_layout[i].append(self.FLOOR)
                else:
                    occupied_visible_adjacent_seats_count = self._occupied_visible_seats_count(i, j)
                    if seat == self.SEAT_EMPTY:
                        if occupied_visible_adjacent_seats_count == 0:
                            new_layout[i].append(self.SEAT_OCCUPIED)
                            self._is_stable = False
                        else:
                            new_layout[i].append(self.SEAT_EMPTY)
                    elif seat == self.SEAT_OCCUPIED:
                        if occupied_visible_adjacent_seats_count >= 5:
                            new_layout[i].append(self.SEAT_EMPTY)
                            self._is_stable = False
                        else:
                            new_layout[i].append(self.SEAT_OCCUPIED)

        self._seat_layout = new_layout

################################################################################

    def is_stable(self) -> bool:
        """
        :return: True if the equilibrium was reached, False otherwise.
        """

        return self._is_stable

################################################################################

    def occupied_seats_count(self) -> int:
        """
        :return: Current number of occupied seats.
        """

        return len([
            seat
            for row in self._seat_layout
            for seat in row
            if seat == self.SEAT_OCCUPIED])

################################################################################

    def _occupied_adjacent_seats_count(self, row: int, column: int) -> int:
        """
        :param row: seat row
        :param column: seat column
        :return: number of occupied adjacent seats around the specified one
        """

        width = len(self._seat_layout[row])
        height = len(self._seat_layout)
        adjacent_seats = []

        for key in self.VISIBLE_DIRECTIONS:
            direction = self.VISIBLE_DIRECTIONS[key]
            i = row
            j = column
            i += direction[self.KEY_ROW_INCREMENT]
            j += direction[self.KEY_COLUMN_INCREMENT]

            if 0 <= i < height and 0 <= j < width:
                adjacent_seats.append(self._seat_layout[i][j])

        return len([
            seat
            for seat in adjacent_seats
            if seat == self.SEAT_OCCUPIED])

################################################################################

    def _occupied_visible_seats_count(self, row: int, column: int) -> int:
        """
        :param row: seat row
        :param column: seat column
        :return: number of occupied visible seats around the specified one
        """

        width = len(self._seat_layout[row])
        height = len(self._seat_layout)
        visible_seats = []

        for key in self.VISIBLE_DIRECTIONS:
            direction = self.VISIBLE_DIRECTIONS[key]
            i = row
            j = column

            while True:
                i += direction[self.KEY_ROW_INCREMENT]
                j += direction[self.KEY_COLUMN_INCREMENT]

                if i < 0 or i >= height or j < 0 or j >= width:
                    break
                elif self._seat_layout[i][j] != self.FLOOR:
                    visible_seats.append(self._seat_layout[i][j])
                    break

        return len([seat
                    for seat in visible_seats
                    if seat == self.SEAT_OCCUPIED])

################################################################################
