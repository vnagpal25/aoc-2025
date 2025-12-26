import os
import pdb
from tqdm import tqdm
from collections import deque
from functools import cache
import re
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""
pt1_ans: int = 2024
pt2_ans: int = 0


def parse_input(string: str):
    # split input on blank line
    initial_bits, gates = string.strip().split('\n\n')

    # get initial bit values
    bits = {name: int(value)
            for bit in initial_bits.splitlines()
            for name, value in [bit.split(': ')]}

    # regex for matching gate strings
    pattern = r'(...) (XOR|OR|AND) (...) -> (...)'

    # array for holding gate information that can't be solved yet
    waiting = []
    for gate in gates.splitlines():
        # append inputs, operation, and resulting value
        (i1, op, i2, res),  = re.findall(pattern, gate)
        waiting.append((i1, i2, op, res))

    # return initial bits/values as well as all information about gates
    return bits, waiting


def pt1(bits, waiting):
    # while there are gates that still need to be resolved
    while waiting:
        # iterate over the gates
        for index, (i1, i2, op, res) in enumerate(waiting):
            # we need the values of both i1 and i2, otherwise we continue
            if i1 not in bits or i2 not in bits:
                continue

            # calculate and store the result
            if op == 'XOR':
                bits[res] = bits[i1] ^ bits[i2]
            elif op == 'AND':
                bits[res] = bits[i1] & bits[i2]
            elif op == 'OR':
                bits[res] = bits[i1] | bits[i2]

            # remove the element from the array
            waiting.pop(index)

    # reverse sort all of the z bit names from most significant to least significant
    z_bits = sorted([bit for bit in bits if bit.startswith('z')], reverse=True)

    # get all of the z bit values, cast to string, and join them
    # convert from binary to decimal and return
    return int(''.join([str(bits[bit]) for bit in z_bits]), 2)


def pt2(bits, waiting):
    # Solution adapted from hyperneutrino's video: https://www.youtube.com/watch?v=SU6lp6wyd3I
    formulas = {res: (op, x, y) for x, y, op, res in waiting}

    def pp(wire, depth=0):
        if wire[0] in 'xy':
            return "  " * depth + wire
        op, x, y = formulas[wire]
        return "  " * depth + op + " (" + wire + ")\n" + pp(x, depth+1) + "\n" + pp(y, depth+1)
    # print(pp('z00'))

    def make_wire(char, num):
        return char + str(num).rjust(2, '0')

    def verify_z(wire, num):
        print('vz', wire, num)
        op, x, y = formulas[wire]
        if op != 'XOR':
            return False
        if num == 0:
            return sorted([x, y]) == ["x00", "y00"]

        return (verify_intermediate_xor(x, num) and verify_carry_bit(y, num)) or (verify_intermediate_xor(y, num) and verify_carry_bit(x, num))

    def verify_intermediate_xor(wire, num):
        print('vx', wire, num)
        op, x, y = formulas[wire]
        if op != 'XOR':
            return False
        return sorted([x, y]) == [make_wire("x", num), make_wire('y', num)]

    def verify_carry_bit(wire, num):
        print('vc', wire, num)
        op, x, y = formulas[wire]
        if num == 1:
            return op == 'AND' and sorted([x, y]) == ['x00', 'y00']
        if op != 'OR':
            return False
        return (verify_direct_carry(x, num - 1) and verify_recarry(y, num - 1)) or (verify_direct_carry(y, num - 1) and verify_recarry(x, num - 1))

    def verify_direct_carry(wire, num):
        print('vd', wire, num)
        op, x, y = formulas[wire]
        if op != 'AND':
            return False

        return sorted([x, y]) == [make_wire('x', num), make_wire('y', num)]

    def verify_recarry(wire, num):
        print('vr', wire, num)
        op, x, y = formulas[wire]
        if op != 'AND':
            return False

        return (verify_intermediate_xor(x, num) and verify_carry_bit(y, num)) or (verify_intermediate_xor(y, num) and verify_carry_bit(x, num))

    def verify(num):
        return verify_z(make_wire("z", num), num)

    i = 0
    while True:
        if not verify(i):
            break
        i += 1
    print(f'failed on {make_wire("z", i)}')
    # z06 <-> dhg,
    # dpd <-> brk,
    # bhd <-> z23,
    # nbf <-> z38
    return "bhd,brk,dhg,dpd,nbf,z06,z23,z38"


def main(puzzle: str):
    assert pt1_ans == pt1(*parse_input(test))
    print(f"Part 1: {pt1(*parse_input(puzzle))}")

    # assert pt2_ans == pt2(*parse_input(test))
    print(f"Part 2: {pt2(*parse_input(puzzle))}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)
