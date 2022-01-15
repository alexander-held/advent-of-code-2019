import fileinput
import heapq  # heappush / heappop
import re
from collections import Counter, defaultdict, deque
from functools import lru_cache, reduce
from itertools import count, cycle, permutations, product
from math import inf, isinf, prod

x = [int(c) for c in [line.strip() for line in fileinput.input()][0].split(",")]


def run_program(memory):
    memory = memory.copy()  # only handle a copy, do not alter original
    instruction_pointer = 0  # initialized at address 0
    while True:
        opcode = memory[instruction_pointer]
        if opcode == 1:  # instruction is addition, 3 params
            operator = sum
            num_params = 3
        elif opcode == 2:  # instruction is multiplication, 3 params
            operator = prod
            num_params = 3
        elif opcode == 99:
            break

        # parameters
        params = [memory[instruction_pointer + i] for i in range(1, num_params + 1)]

        memory[params[2]] = operator([memory[params[0]], memory[params[1]]])
        instruction_pointer += 1 + num_params

    return memory


x[1] = 12
x[2] = 2
print(f"part 1: {run_program(x)[0]}")

for noun, verb in product(range(100), repeat=2):
    x[1] = noun
    x[2] = verb
    result = run_program(x)
    if result[0] == 19690720:
        print(f"part 2: {100*noun+ verb}")
