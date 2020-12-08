__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from typing import List, Dict, Union, Tuple

"""
--- Day 8: Handheld Halting ---

Your flight to the major airline hub reaches cruising altitude without incident. 
While you consider checking the in-flight menu for one of those drinks that come 
with a little umbrella, you are interrupted by the kid sitting next to you.

Their handheld game console won't turn on! They ask if you can take a look.
"""

################################################################################

KEY_OPERATION = "OPERATION"
KEY_ARGUMENT = "ARGUMENT"
KEY_MODIFIED = "MODIFIED"

MODIFY_ACCUMULATOR_OPERATION = "acc"
JUMP_OPERATION = "jmp"
NOP_OPERATION = "nop"

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    You narrow the problem down to a strange infinite loop in the boot code
    (your puzzle input) of the device. You should be able to fix it, but first
    you need to be able to run the code in isolation.

    The boot code is represented as a text file with one instruction per line of
    text. Each instruction consists of an operation (acc, jmp, or nop) and an
    argument (a signed number like +4 or -20).

    -acc increases or decreases a single global value called the accumulator by
     the value given in the argument. For example, acc +7 would increase the
     accumulator by 7. The accumulator starts at 0. After an acc instruction,
     the instruction immediately below it is executed next.
    -jmp jumps to a new instruction relative to itself. The next instruction to
     execute is found using the argument as an offset from the jmp instruction;
     for example, jmp +2 would skip the next instruction, jmp +1 would continue
     to the instruction immediately below it, and jmp -20 would cause the
     instruction 20 lines above to be executed next.
    -nop stands for No OPeration - it does nothing. The instruction immediately
     below it is executed next.

    For example, consider the following program:

    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6

    These instructions are visited in this order:

    nop +0  | 1
    acc +1  | 2, 8(!)
    jmp +4  | 3
    acc +3  | 6
    jmp -3  | 7
    acc -99 |
    acc +1  | 4
    jmp -4  | 5
    acc +6  |

    First, the nop +0 does nothing. Then, the accumulator is increased from 0 to
    1 (acc +1) and jmp +4 sets the next instruction to the other acc +1 near the
    bottom. After it increases the accumulator from 1 to 2, jmp -4 executes,
    setting the next instruction to the only acc +3. It sets the accumulator to
    5, and jmp -3 causes the program to continue back at the first acc +1.

    This is an infinite loop: with this sequence of jumps, the program will run
    forever. The moment the program tries to run any instruction a second time,
    you know it will never terminate.

    Immediately before the program would run an instruction a second time, the
    value in the accumulator is 5.

    Run your copy of the boot code. Immediately before any instruction is
    executed a second time, what value is in the accumulator?

    The answer should be 1801.
    """

    program = _load_program()
    result = _run_program(program)
    accumulator = result[0]
    print(accumulator)

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    After some careful analysis, you believe that exactly one instruction is
    corrupted.

    Somewhere in the program, either a jmp is supposed to be a nop, or a nop is
    supposed to be a jmp. (No acc instructions were harmed in the corruption of
    this boot code.)

    The program is supposed to terminate by attempting to execute an instruction
    immediately after the last instruction in the file. By changing exactly one
    jmp or nop, you can repair the boot code and make it terminate correctly.

    For example, consider the same program from above:

    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6

    If you change the first instruction from nop +0 to jmp +0, it would create a
    single-instruction infinite loop, never leaving that instruction. If you
    change almost any of the jmp instructions, the program will still eventually
    find another jmp instruction and loop forever.

    However, if you change the second-to-last instruction (from jmp -4 to nop
    -4), the program terminates! The instructions are visited in this order:

    nop +0  | 1
    acc +1  | 2
    jmp +4  | 3
    acc +3  |
    jmp -3  |
    acc -99 |
    acc +1  | 4
    nop -4  | 5
    acc +6  | 6

    After the last instruction (acc +6), the program terminates by attempting to
    run the instruction below the last instruction in the file. With this
    change, after the program terminates, the accumulator contains the value 8
    (acc +1, acc +1, acc +6).

    Fix the program so that it terminates normally by changing exactly one jmp
    (to nop) or nop (to jmp). What is the value of the accumulator after the
    program terminates?

    The answer should be 2060.
    """

    program = _load_program()

    while True:
        result = _run_program(program)
        if result[1] is True:
            # a loop was found while running the program, change it
            _modify_program(program)
        else:
            # program terminated normally
            print(result[0])
            break

################################################################################

def _load_program() -> List[Dict[str, Union[str, int, bool]]]:
    """
    :return: list of instructions
    """

    with open("day_08/input.txt", 'r') as f:
        return [{
            KEY_OPERATION: line.split(' ')[0].strip(),
            KEY_ARGUMENT: int(line.split(' ')[1].strip()),
            KEY_MODIFIED: False
        } for line in [line.strip() for line in f.readlines()]]

################################################################################

def _run_program(
        program: List[Dict[str, Union[str, int, bool]]]) \
        -> Tuple[int, bool]:
    """
    Runs the program specified by the param.

    :param program: program to be run
    :return: tuple of accumulator value and True if loop was found during the
    program run, False otherwise
    """

    accumulator = 0
    i = 0
    instruction = program[i]
    visited = []

    while True:
        visited.append(i)
        if instruction[KEY_OPERATION] == MODIFY_ACCUMULATOR_OPERATION:
            accumulator += instruction[KEY_ARGUMENT]
            i += 1
        elif instruction[KEY_OPERATION] == JUMP_OPERATION:
            i += instruction[KEY_ARGUMENT]
        elif instruction[KEY_OPERATION] == NOP_OPERATION:
            i += 1

        try:
            instruction = program[i]
        except IndexError:
            # this was the end of the program, no loop was found
            return accumulator, False

        if i in visited:
            # loop was found
            return accumulator, True

################################################################################

def _modify_program(program: List[Dict[str, Union[str, int, bool]]]) -> None:
    """
    Change one nop instruction to jmp or vice versa.

    :param program: program to be modified
    """

    try:
        # find the last modified instruction and change it back
        modified_instruction_index = [
            i
            for i in range(len(program))
            if program[i][KEY_MODIFIED] is True][0]
        modified_instruction = program[modified_instruction_index]
        modified_instruction[KEY_OPERATION] = NOP_OPERATION \
            if modified_instruction[KEY_OPERATION] == JUMP_OPERATION \
            else JUMP_OPERATION
        modified_instruction[KEY_MODIFIED] = False
    except IndexError:
        # there is no changed instruction on the first run
        modified_instruction_index = -1

    # find next instruction to modify
    i = min([
        i
        for i in range(modified_instruction_index + 1, len(program))
        if program[i][KEY_OPERATION] == JUMP_OPERATION
           or program[i][KEY_OPERATION] == NOP_OPERATION])
    # and modify it
    program[i][KEY_OPERATION] = NOP_OPERATION \
        if program[i][KEY_OPERATION] == JUMP_OPERATION \
        else JUMP_OPERATION
    program[i][KEY_MODIFIED] = True

################################################################################
