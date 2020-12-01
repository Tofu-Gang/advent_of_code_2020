__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from itertools import combinations
from functools import reduce

"""
--- Day 1: Report Repair ---

After saving Christmas five years in a row, you've decided to take a vacation at 
a nice resort on a tropical island. Surely, Christmas will go on without you.

The tropical island has its own currency and is entirely cash-only. The gold 
coins used there have a little picture of a starfish; the locals just call them 
stars. None of the currency exchanges seem to have heard of them, but somehow, 
you'll need to find fifty of these coins by the time you arrive so you can pay 
the deposit on your room.

To save your vacation, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day 
in the Advent calendar; the second puzzle is unlocked when you complete the 
first. Each puzzle grants one star. Good luck!
"""

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    Before you leave, the Elves in accounting just need you to fix your expense
    report (your puzzle input); apparently, something isn't quite adding up.

    Specifically, they need you to find the two entries that sum to 2020 and
    then multiply those two numbers together.

    For example, suppose your expense report contained the following:

    1721
    979
    366
    299
    675
    1456

    In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying
    them together produces 1721 * 299 = 514579, so the correct answer is 514579.

    Of course, your expense report is much larger. Find the two entries that sum
    to 2020; what do you get if you multiply them together?

    The answer should be 444019.
    """

    print(_get_product("day_01/input.txt", 2))

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    The Elves in accounting are thankful for your help; one of them even offers
    you a starfish coin they had left over from a past vacation. They offer you
    a second one if you can find three numbers in your expense report that meet
    the same criteria.

    Using the above example again, the three entries that sum to 2020 are 979,
    366, and 675. Multiplying them together produces the answer, 241861950.

    In your expense report, what is the product of the three entries that sum to
    2020?

    The answer should be 29212176.
    """

    print(_get_product("day_01/input.txt", 3))

################################################################################

def _get_product(file_path: str, count: int) -> int:
    """
    Loads numbers from the input file, then finds specified count of numbers
    which sum is 2020. Returns their product.

    :param file_path: input file path
    :param count: count of the numbers to make the resulting product
    :return: puzzle solution
    """

    with open(file_path, 'r') as f:
        return reduce(
            lambda x, y: x * y,
            [combination
             for combination in combinations(
                [int(line.strip())
                 for line in f.readlines()], count)
             if sum(combination) == 2020][0])

################################################################################
