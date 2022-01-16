import fileinput
import heapq  # heappush / heappop
import re
from collections import Counter, defaultdict, deque
from functools import lru_cache, reduce
from itertools import count, cycle, permutations, product
from math import inf, isinf, prod
from operator import add, eq, lt, mul

x = [int(c) for c in [line.strip() for line in fileinput.input()][0].split(",")]


def run_program(memory, input, verbose=False):
    memory = memory.copy()  # only handle a copy, do not alter original
    instruction_pointer = 0  # initialized at address 0
    output = []

    while True:
        opcode = memory[instruction_pointer] % 100

        if opcode == 1:  # addition
            operator = add
            num_params = 3
        elif opcode == 2:  # multiplication
            operator = mul
            num_params = 3
        elif opcode == 3:  # input saved to address
            operator = lambda: input  # return input instead of reading from memory
            num_params = 1
        elif opcode == 4:  # output a value
            operator = None
            num_params = 1
        elif opcode == 5:  # jump-if-true
            operator = None
            num_params = 2
        elif opcode == 6:  # jump-if-false
            operator = None
            num_params = 2
        elif opcode == 7:  # less than
            operator = lt
            num_params = 3
        elif opcode == 8:  # less than
            operator = eq
            num_params = 3
        elif opcode == 99:
            break
        else:
            raise NotImplementedError(f"opcode {opcode} not implemented")

        params = [memory[instruction_pointer + i] for i in range(1, num_params + 1)]
        # parameter modes: position mode if par_modes is 0, else immediate mode
        par_modes = [int(c) for c in str(memory[instruction_pointer])[:-2][::-1]]
        # values take parameter mode into account, and use position mode by default
        # (par_modes can be shorter than length of parameters)
        values = [
            p if (i < len(par_modes) and par_modes[i]) else memory[p]
            for i, p in enumerate(params)
        ]

        if operator is not None:  # write result of instruction to memory
            memory[params[-1]] = operator(*values[:-1])  # position mode for writing
        elif opcode == 4:  # handle output (always single value)
            if verbose:
                print(f"output: {values[0]}")
            output.append(values[0])
        elif opcode in (5, 6):  # jump instructions
            if (opcode == 5 and values[0] != 0) or (opcode == 6 and values[0] == 0):
                instruction_pointer = values[1]
                continue
        else:
            raise NotImplementedError(f"opcode is {opcode}, operator is {operator}")

        instruction_pointer += 1 + num_params

    return memory, output


print(f"part 1: {run_program(x, 1)[1][-1]}")
print(f"part 2: {run_program(x, 5)[1][-1]}")
