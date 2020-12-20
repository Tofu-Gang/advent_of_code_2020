__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from typing import Dict, List
from numpy import prod

"""
--- Day 16: Ticket Translation ---

As you're walking to yet another connecting flight, you realize that one of the 
legs of your re-routed trip coming up is on a high-speed train. However, the 
train ticket you were given is in a language you don't understand. You should 
probably figure out what it says before you get to the train station after the 
next flight.
"""

################################################################################

RULES_DELIMITER = ':'
INTERVALS_DELIMITER = "or"
INTERVAL_DELIMITER = '-'
KEY_FROM = "FROM"
KEY_TO = "TO"
TICKET_FIELD_DELIMITER = ','
GOAL_FIELDS_START = "departure"

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    Unfortunately, you can't actually read the words on the ticket. You can,
    however, read the numbers, and so you figure out the fields these tickets
    must have and the valid ranges for values in those fields.

    You collect the rules for ticket fields, the numbers on your ticket, and the
    numbers on other nearby tickets for the same train service (via the airport
    security cameras) together into a single document you can reference (your
    puzzle input).

    The rules for ticket fields specify a list of fields that exist somewhere on
    the ticket and the valid ranges of values for each field. For example, a
    rule like class: 1-3 or 5-7 means that one of the fields in every ticket is
    named class and can be any value in the ranges 1-3 or 5-7 (inclusive, such
    that 3 and 5 are both valid in this field, but 4 is not).

    Each ticket is represented by a single line of comma-separated values. The
    values are the numbers on the ticket in the order they appear; every ticket
    has the same format. For example, consider this ticket:

    .--------------------------------------------------------.
    | ????: 101    ?????: 102   ??????????: 103     ???: 104 |
    |                                                        |
    | ??: 301  ??: 302             ???????: 303      ??????? |
    | ??: 401  ??: 402           ???? ????: 403    ????????? |
    '--------------------------------------------------------'

    Here, ? represents text in a language you don't understand. This ticket
    might be represented as 101,102,103,104,301,302,303,401,402,403; of course,
    the actual train tickets you're looking at are much more complicated. In any
    case, you've extracted just the numbers in such a way that the first number
    is always the same specific field, the second number is always a different
    specific field, and so on - you just don't know what each position actually
    means!

    Start by determining which tickets are completely invalid; these are tickets
    that contain values which aren't valid for any field. Ignore your ticket for
    now.

    For example, suppose you have the following notes:

    class: 1-3 or 5-7
    row: 6-11 or 33-44
    seat: 13-40 or 45-50

    your ticket:
    7,1,14

    nearby tickets:
    7,3,47
    40,4,50
    55,2,20
    38,6,12

    It doesn't matter which position corresponds to which field; you can
    identify invalid nearby tickets by considering only whether tickets contain
    values that are not valid for any field. In this example, the values on the
    first nearby ticket are all valid for at least one field. This is not true
    of the other three nearby tickets: the values 4, 55, and 12 are are not
    valid for any field. Adding together all of the invalid values produces your
    ticket scanning error rate: 4 + 55 + 12 = 71.

    Consider the validity of the nearby tickets you scanned. What is your ticket
    scanning error rate?

    The answer should be 25972.
    """

    with open("day_16/input.txt", 'r') as f:
        rules = _create_rules()
        nearby_tickets = _create_nearby_tickets()

        print(sum([
            field
            for ticket in nearby_tickets
            for field in ticket
            if not any([
                rule[KEY_FROM] <= field <= rule[KEY_TO]
                for key in rules
                for rule in rules[key]])]))

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    Now that you've identified which tickets contain invalid values, discard
    those tickets entirely. Use the remaining valid tickets to determine which
    field is which.

    Using the valid ranges for each field, determine what order the fields
    appear on the tickets. The order is consistent between all tickets: if seat
    is the third field, it is the third field on every ticket, including your
    ticket.

    For example, suppose you have the following notes:

    class: 0-1 or 4-19
    row: 0-5 or 8-19
    seat: 0-13 or 16-19

    your ticket:
    11,12,13

    nearby tickets:
    3,9,18
    15,1,5
    5,14,9

    Based on the nearby tickets in the above example, the first position must be
    row, the second position must be class, and the third position must be seat;
    you can conclude that in your ticket, class is 12, row is 11, and seat is
    13.

    Once you work out which field is which, look for the six fields on your
    ticket that start with the word departure. What do you get if you multiply
    those six values together?

    The answer should be 622670335901.
    """

    with open("day_16/input.txt", 'r') as f:
        rules = _create_rules()
        my_ticket = _create_my_ticket()
        nearby_tickets = _create_nearby_tickets()
        valid_tickets = [ticket
                         for ticket in nearby_tickets
                         if _is_ticket_valid(rules, ticket)]

        valid_fields = {}
        [valid_fields.__setitem__(i, []) for i in range(len(my_ticket))]
        [valid_fields[i].append(key)
         for i in range(len(my_ticket))
         for key in rules if all([any([
            rule[KEY_FROM] <= field <= rule[KEY_TO]
            for rule in rules[key]])
            for field in [
                ticket[i]
                for ticket in valid_tickets]])]

        while any([len(valid_fields[key]) > 1 for key in valid_fields]):
            resolved_fields = [
                valid_fields[key][0]
                for key in valid_fields
                if len(valid_fields[key]) == 1]

            for key in valid_fields:
                if len(valid_fields[key]) > 1:
                    for resolved_field in resolved_fields:
                        try:
                            valid_fields[key].remove(resolved_field)
                        except ValueError:
                            pass

        print(prod([
            my_ticket[key]
            for key in valid_fields
            if valid_fields[key][0].startswith(GOAL_FIELDS_START)]))

################################################################################

def _create_rules() -> Dict[str, List[Dict[str, int]]]:
    """
    :return: validation rules from the input
    """

    with open("day_16/input.txt", 'r') as f:
        rules = {}

        # [0] is the number of "rules" segment in the input
        for line in f.read().split('\n\n')[0].split('\n'):
            line_split = line.split(RULES_DELIMITER)
            rule_name = line_split[0].strip()
            intervals = [
                interval.strip()
                for interval in line_split[1].split(INTERVALS_DELIMITER)]
            rules[rule_name] = []

            for interval in intervals:
                interval_split = interval.split(INTERVAL_DELIMITER)
                rules[rule_name].append({
                    KEY_FROM: int(interval_split[0].strip()),
                    KEY_TO: int(interval_split[1].strip())
                })

        return rules

################################################################################

def _create_my_ticket() -> List[int]:
    """
    :return: my ticket from the input
    """

    with open("day_16/input.txt", 'r') as f:
        # the first [1] is the number of "my ticket" segment in the input
        # the second [1] means the second line of the "my ticket" segment
        return [
            int(field.strip())
            for field in f.read().strip().split('\n\n')[1] \
                .split('\n')[1].split(TICKET_FIELD_DELIMITER)]

################################################################################

def _create_nearby_tickets() -> List[List[int]]:
    """
    :return: list of nearby tickets from the input
    """

    with open("day_16/input.txt", 'r') as f:
        # the [2] is the number of "nearby tickets" segment in the input
        # the [1:] omits the first line, which is a heading and not a ticket
        return [[
            int(field.strip())
            for field in line.split(TICKET_FIELD_DELIMITER)]
            for line in f.read().strip().split('\n\n')[2].split('\n')[1:]]

################################################################################

def _is_ticket_valid(
        rules: Dict[str, List[Dict[str, int]]],
        ticket: List[int]) -> bool:
    """
    :param rules: rules to validate the ticket with
    :param ticket: ticket to be validated
    :return: True when the ticket is valid, False otherwise
    """

    return all([any([rule[KEY_FROM] <= field <= rule[KEY_TO]
                     for key in rules
                     for rule in rules[key]])
                for field in ticket])

################################################################################
