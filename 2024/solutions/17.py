import os
import re
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test1: str = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
test2: str = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""
pt1_ans: str = '4,6,3,5,6,3,5,2,1,0'
pt2_ans: int = 117440


def parse_input(string: str):
    registers_str, program_str = string.split('\n\n')

    # extract the register name(.) and value(\d+) for each register string (A, B, C, etc.)
    registers = {}
    for register in registers_str.splitlines():
        reg_info, = re.findall(r'Register (.): (\d+)', register)
        registers[reg_info[0]] = int(reg_info[1])

    # extract all digits from the program string
    program = [int(x) for x in re.findall(r'(\d+)', program_str)]
    return registers, program


def pt1(reg, prog):
    def combo(operand):
        assert 0 <= operand <= 6  # can't be 7

        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return reg['A']
        if operand == 5:
            return reg['B']
        if operand == 6:
            return reg['C']

    output = []
    i = 0  # instruction pointer
    while i+1 < len(prog):
        jump = False
        opcode, operand = prog[i], prog[i+1]
        if opcode == 0:
            reg['A'] = reg['A'] // (2**combo(operand))
        elif opcode == 1:
            reg['B'] = reg['B'] ^ operand
        elif opcode == 2:
            reg['B'] = combo(operand) % 8
        elif opcode == 3 and reg['A']:
            jump = True
            i = operand
        elif opcode == 4:
            reg['B'] ^= reg['C']
        elif opcode == 5:
            output.append(str(combo(operand) % 8))
        elif opcode == 6:
            reg['B'] = reg['A'] // (2**combo(operand))
        elif opcode == 7:
            reg['C'] = reg['A'] // (2**combo(operand))

        if not jump:
            i += 2

    return ','.join(output)


def pt2(reg: dict, prog):
    def find(input, ans):
        # recursion base case
        # assumptions:
        # last instruction is (3, 0) which is a jump instruction which causes our program to act like a while loop
        # only one output per loop (5, 5)
        # a is only modified in one instruction (a >> 3)
        if input == []:
            return ans

        for t in range(8):
            a = ans << 3 | t
            output = None
            b, c = 0, 0
            adv3 = False

            def combo(operand):
                assert 0 <= operand <= 6  # can't be 7
                if 0 <= operand <= 3:
                    return operand
                if operand == 4:
                    return a
                if operand == 5:
                    return b
                if operand == 6:
                    return c

            for pointer in range(0, len(prog) - 2, 2):
                ins = prog[pointer]
                operand = prog[pointer+1]
                if ins == 0:
                    assert operand == 3
                    adv3 = True
                elif ins == 1:
                    b = b ^ operand
                elif ins == 2:
                    b = combo(operand) % 8
                elif ins == 4:
                    b = b ^ c
                elif ins == 5:
                    assert output is None
                    output = combo(operand) % 8
                elif ins == 6:
                    b = a >> combo(operand)
                elif ins == 7:
                    c = a >> combo(operand)
                if output == input[-1]:
                    sub = find(input[:-1], a)
                    if sub is None:
                        continue
                    return sub

    return find(prog, 0)


def main(puzzle: str):
    # TODO parse input and test
    test_reg, test_prog = parse_input(test1)
    reg, prog = parse_input(puzzle)

    assert pt1_ans == pt1(test_reg, test_prog)
    print(f"Part 1: {pt1(reg.copy(), prog)}")

    test_reg, test_prog = parse_input(test2)
    assert pt2_ans == pt2(test_reg, test_prog)
    print(f"Part 2: {pt2(reg.copy(), prog)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)
