__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from re import finditer
from typing import Dict, List, Union, Set

"""
--- Day 7: Handy Haversacks ---

You land at the regional airport in time for your next flight. In fact, it looks 
like you'll even have time to grab some food: all flights are currently delayed 
due to issues in luggage processing.
"""

################################################################################

SEPARATOR = "bags contain"
MY_BAG = "shiny gold"

KEY_BAG = "BAG"
KEY_BAGS_COUNT = "BAGS_COUNT"

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    Due to recent aviation regulations, many rules (your puzzle input) are being
    enforced about bags and their contents; bags must be color-coded and must
    contain specific quantities of other color-coded bags. Apparently, nobody
    responsible for these regulations considered how long they would take to
    enforce!

    For example, consider the following rules:

    light red bags contain 1 bright white bag, 2 muted yellow bags.
    dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    bright white bags contain 1 shiny gold bag.
    muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    faded blue bags contain no other bags.
    dotted black bags contain no other bags.

    These rules specify the required contents for 9 bag types. In this example,
    every faded blue bag is empty, every vibrant plum bag contains 11 bags (5
    faded blue and 6 dotted black), and so on.

    You have a shiny gold bag. If you wanted to carry it in at least one other
    bag, how many different bag colors would be valid for the outermost bag? (In
    other words: how many colors can, eventually, contain at least one shiny
    gold bag?)

    In the above rules, the following options would be available to you:

    -A bright white bag, which can hold your shiny gold bag directly.
    -A muted yellow bag, which can hold your shiny gold bag directly, plus some
     other bags.
    -A dark orange bag, which can hold bright white and muted yellow bags,
     either of which could then hold your shiny gold bag.
    -A light red bag, which can hold bright white and muted yellow bags, either
     of which could then hold your shiny gold bag.

    So, in this example, the number of bag colors that can eventually contain at
    least one shiny gold bag is 4.

    How many bag colors can eventually contain at least one shiny gold bag? (The
    list of rules is quite long; make sure you get all of it.)

    The answer should be 226.
    """

    bags_rules = _get_bags_rules()
    print(len(_get_possible_bag_containers(MY_BAG, bags_rules)))

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---
    It's getting pretty expensive to fly these days - not because of ticket
    prices, but because of the ridiculous number of bags you need to buy!

    Consider again your shiny gold bag and the rules from the above example:

    faded blue bags contain 0 other bags.
    dotted black bags contain 0 other bags.
    vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted
    black bags.
    dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black
    bags.

    So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags
    within it) plus 2 vibrant plum bags (and the 11 bags within each of those):
    1 + 1*7 + 2 + 2*11 = 32 bags!

    Of course, the actual rules have a small chance of going several levels
    deeper than this example; be sure to count all of the bags, even if the
    nesting becomes topologically impractical!

    Here's another example:

    shiny gold bags contain 2 dark red bags.
    dark red bags contain 2 dark orange bags.
    dark orange bags contain 2 dark yellow bags.
    dark yellow bags contain 2 dark green bags.
    dark green bags contain 2 dark blue bags.
    dark blue bags contain 2 dark violet bags.
    dark violet bags contain no other bags.

    In this example, a single shiny gold bag must contain 126 other bags.

    How many individual bags are required inside your single shiny gold bag?

    The answer should be 9569.
    """

    bags_rules = _get_bags_rules()
    print(_get_required_count(MY_BAG, bags_rules))

################################################################################

def _get_bags_rules() -> Dict[str, List[Dict[str, Union[int, str]]]]:
    """
    Load bag contents rules into a dict structure like so:
    bag_container [{
        content_color_code
        count
    },...]

    :return: bag contents rules
    """

    with open("day_07/input.txt", 'r') as f:
        bags = {}
        for line in [line.strip() for line in f.readlines()]:
            bag_container = line.split(SEPARATOR)[0].strip()
            bag_contents = line.split(SEPARATOR)[1].strip()

            color_codes = [
                contents.group(0).strip()
                for contents in finditer(r"(?<=[0-9]).*?(?=bag)", bag_contents)]

            counts = [
                int(contents.group(0).strip())
                for color_code in color_codes
                for contents in finditer(
                    r'[0-9]+ (?={})'.format(color_code), bag_contents)]

            bags[bag_container] = [{
                KEY_BAGS_COUNT: counts[i],
                KEY_BAG: color_codes[i]
            } for i in range(len(counts))]

        return bags

################################################################################

def _get_possible_bag_containers(
        color_code: str,
        bags_rules: Dict[str, List[Dict[str, Union[int, str]]]]) -> Set[str]:
    """
    Recursively finds out which bag colors can eventually contain the bag color
    specified by the param.

    :param color_code: bag color contained in other bags
    :param bags_rules: bag contents rules
    :return: all bag colors that can eventually contain the bag color specified
    by the param
    """

    possible_containers = [
        bag_container
        for bag_container in bags_rules
        if color_code in [
            contents[KEY_BAG]
            for contents in bags_rules[bag_container]]]
    return set(
        possible_containers + [
            possible_container
            for container in possible_containers
            for possible_container in _get_possible_bag_containers(
                container, bags_rules)])

################################################################################

def _get_required_count(
        color_code: str,
        bags_rules: Dict[str, List[Dict[str, Union[int, str]]]]) -> int:
    """
    Recursively finds out how many individual bags are required inside one bag
    specified by the param.

    :param color_code: bag color code
    :param bags_rules: bag contents rules
    :return: how many individual bags are required inside one bag specified by
    the param
    """

    return sum(
        contents[KEY_BAGS_COUNT]
        for contents in bags_rules[color_code]) \
           + sum(
        contents[KEY_BAGS_COUNT]
        * _get_required_count(contents[KEY_BAG], bags_rules)
        for contents in bags_rules[color_code])

################################################################################