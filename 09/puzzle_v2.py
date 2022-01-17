import fileinput
import heapq  # heappush / heappop
import re
from collections import Counter, defaultdict, deque
from functools import lru_cache, reduce
from itertools import chain, count, cycle, permutations, product, repeat
from math import inf, isinf, prod
from operator import add, eq, lt, mul

x = [int(c) for c in [line.strip() for line in fileinput.input()][0].split(",")]


class Computer:
    def __init__(self, memory, inputs=None):
        self.mem = defaultdict(int, enumerate(memory))  # defaults to 0
        self.ip = 0  # instruction pointer
        self.rb = 0  # relative base
        self.inputs = deque(inputs) if inputs else deque([])

    def run(self):
        # number of parameters per instruction, keys are opcode
        num_params = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1, 99: 0}

        while True:
            opcode = self.mem[self.ip] % 100
            params = [self.mem[self.ip + i] for i in range(1, num_params[opcode] + 1)]
            # parameter modes which are specified (can be shorted than params)
            par_modes = [int(c) for c in str(self.mem[self.ip])[:-2][::-1]]
            # take parameter mode into account (0: position, 1: immediate, 2: relative),
            # par_modes can be shorted than length of parameters
            values = []
            for i, p in enumerate(params):
                if i > len(par_modes) - 1 or par_modes[i] == 0:
                    values.append(self.mem[p])  # position mode, default
                elif par_modes[i] == 1:
                    values.append(p)  # immediate mode
                else:
                    values.append(self.mem[p + self.rb])  # relative mode
            self.ip += 1 + num_params[opcode]  # update pointer position

            if opcode == 1:  # addition
                operator = add
            elif opcode == 2:  # multiplication
                operator = mul
            elif opcode == 3:  # input saved to address
                # use input instead of reading from memory
                operator = lambda: self.inputs.popleft()
            elif opcode == 4:  # output a value
                operator = None
                yield values[0]
            elif opcode == 5:  # jump-if-true
                operator = None
                if values[0] != 0:
                    self.ip = values[1]
            elif opcode == 6:  # jump-if-false
                operator = None
                if values[0] == 0:
                    self.ip = values[1]
            elif opcode == 7:  # less than
                operator = lt
            elif opcode == 8:  # less than
                operator = eq
            elif opcode == 9:  # relative base update
                operator = None
                self.rb += values[0]
            elif opcode == 99:
                break
            else:
                raise NotImplementedError(f"opcode {opcode} not implemented")

            if operator is not None:  # write result of instruction to memory
                # writing in position or immediate mode, int conversion for lt/eq
                write_idx = params[-1]
                if len(params) == len(par_modes) and par_modes[-1] == 2:
                    write_idx += self.rb
                self.mem[write_idx] = int(operator(*values[:-1]))


c = Computer(x, [1])
print(f"part 1: {next(c.run())}")

c = Computer(x, [2])
print(f"part 2: {next(c.run())}")
