__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from typing import List
from pyparsing import Word, nums, nestedExpr

"""
--- Day 18: Operation Order ---

As you look out the window and notice a heavily-forested continent slowly appear 
over the horizon, you are interrupted by the child sitting next to you. They're 
curious if you could help them with their math homework.

Unfortunately, it seems like this "math" follows different rules than you 
remember.
"""

################################################################################

ADDITION = '+'
MULTIPLICATION = '*'
OPEN_BRACKET = '('
CLOSE_BRACKET = ')'

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    The homework (your puzzle input) consists of a series of expressions that
    consist of addition (+), multiplication (*), and parentheses ((...)). Just
    like normal math, parentheses indicate that the expression inside must be
    evaluated before it can be used by the surrounding expression. Addition
    still finds the sum of the numbers on both sides of the operator, and
    multiplication still finds the product.

    However, the rules of operator precedence have changed. Rather than
    evaluating multiplication before addition, the operators have the same
    precedence, and are evaluated left-to-right regardless of the order in which
    they appear.

    For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are
    as follows:

    1 + 2 * 3 + 4 * 5 + 6
      3   * 3 + 4 * 5 + 6
          9   + 4 * 5 + 6
             13   * 5 + 6
                 65   + 6
                     71

    Parentheses can override this order; for example, here is what happens if
    parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

    1 + (2 * 3) + (4 * (5 + 6))
    1 +    6    + (4 * (5 + 6))
         7      + (4 * (5 + 6))
         7      + (4 *   11   )
         7      +     44
                51

    Here are a few more examples:

    2 * 3 + (4 * 5) becomes 26.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.

    Before you can help with the homework, you need to understand it yourself.
    Evaluate the expression on each line of the homework; what is the sum of the
    resulting values?

    The answer should be 3647606140187.
    """

    with open("day_18/input.txt", 'r') as f:
        lines = ['(' + line.strip() + ')' for line in f.readlines()]
        content = Word(nums) | '+' | '*'
        parentheses = nestedExpr('(', ')', content=content)
        print(sum([_evaluate_1(parentheses.parseString(line))
                   for line in lines]))

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    You manage to answer the child's questions and they finish part 1 of their
    homework, but get stuck when they reach the next section: advanced math.

    Now, addition and multiplication have different precedence levels, but
    they're not the ones you're familiar with. Instead, addition is evaluated
    before multiplication.

    For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are
    now as follows:

    1 + 2 * 3 + 4 * 5 + 6
      3   * 3 + 4 * 5 + 6
      3   *   7   * 5 + 6
      3   *   7   *  11
         21       *  11
             231

    Here are the other examples from above:

    1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
    2 * 3 + (4 * 5) becomes 46.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.

    What do you get if you add up the results of evaluating the homework
    problems using these new rules?

    The answer should be 323802071857594.
    """

    with open("day_18/input.txt", 'r') as f:
        lines = ['(' + line.strip() + ')' for line in f.readlines()]
        content = Word(nums) | '+' | '*'
        parentheses = nestedExpr('(', ')', content=content)
        print(sum([_evaluate_2(parentheses.parseString(line))
                   for line in lines]))

################################################################################

def _evaluate_1(line: List) -> int:
    """
    Returns the result of the mathematical expression from the input. To be used
    in puzzle 1; operators have the same precedence.

    :param line: mathematical expression to be evaluated; parsed to list of
    lists by pyparsing library
    :return: result of the mathematical expression from the input
    """

    stack = []

    for element in line:
        try:
            if element.isnumeric():
                stack.append(int(element))
            elif element == ADDITION or element == MULTIPLICATION:
                stack.append(element)
            else:
                # shouldn't happen
                stack = None
        except TypeError:
            # subexpression in parentheses
            stack.append(_evaluate_1(element))

    while len(stack) > 1:
        operand_1 = stack.pop(0)
        operator = stack.pop(0)
        operand_2 = stack.pop(0)

        if operator == ADDITION:
            stack.insert(0, operand_1 + operand_2)
        elif operator == MULTIPLICATION:
            stack.insert(0, operand_1 * operand_2)
        else:
            # should not happen
            stack = None

    return stack.pop()

################################################################################

def _evaluate_2(line: List) -> int:
    """
    Returns the result of the mathematical expression from the input. To be used
    in puzzle 2; addition is evaluated before multiplication.

    :param line: mathematical expression to be evaluated; parsed to list of
    lists by pyparsing library
    :return: result of the mathematical expression from the input
    """

    stack = []

    for element in line:
        try:
            if element.isnumeric():
                stack.append(int(element))
            elif element == ADDITION or element == MULTIPLICATION:
                stack.append(element)
            else:
                # shouldn't happen
                stack = None
        except TypeError:
            # subexpression in parentheses
            stack.append(_evaluate_2(element))

    # solve additions first
    while ADDITION in stack:
        index = stack.index(ADDITION) - 1
        operand_1 = stack.pop(index)
        operator = stack.pop(index)
        operand_2 = stack.pop(index)
        stack.insert(index, operand_1 + operand_2)

    # solve the rest of the expression
    while len(stack) > 1:
        operand_1 = stack.pop(0)
        operator = stack.pop(0)
        operand_2 = stack.pop(0)

        if operator == MULTIPLICATION:
            stack.insert(0, operand_1 * operand_2)
        else:
            # should not happen
            stack = None

    return stack.pop()

################################################################################
