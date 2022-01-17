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
        self.mem = memory.copy()  # only handle a copy, do not alter original
        self.ip = 0  # instruction pointer
        self.inputs = deque(inputs) if inputs else deque([])

    def run(self):
        # number of parameters per instruction, keys are opcode
        num_params = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 99: 0}

        while True:
            opcode = self.mem[self.ip] % 100
            params = [self.mem[self.ip + i] for i in range(1, num_params[opcode] + 1)]
            # parameter modes: immediate mode if par_modes is 1, else position mode
            par_modes = [int(c) for c in str(self.mem[self.ip])[:-2][::-1]]
            # values take parameter mode into account (0: position, 1: immediate),
            # par_modes can be shorted than length of parameters, then default to 0
            values = [
                p if (i < len(par_modes) and par_modes[i]) else self.mem[p]
                for i, p in enumerate(params)
            ]
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
            elif opcode == 99:
                break
            else:
                raise NotImplementedError(f"opcode {opcode} not implemented")

            if operator is not None:  # write result of instruction to memory
                # position mode for writing, int conversion for lt/eq
                self.mem[params[-1]] = int(operator(*values[:-1]))


max_signal = 0
for pc in permutations([0, 1, 2, 3, 4]):
    amplifiers = [Computer(x, inputs=[p]) for p in pc]
    amplifiers[0].inputs.append(0)  # start with signal 0
    for i_amp, amp in enumerate(amplifiers):
        signal = next(amp.run())
        amplifiers[(i_amp + 1) % 5].inputs.append(signal)
    max_signal = max(max_signal, signal)

print(f"part 1: {max_signal}")

max_signal = 0
for pc in permutations([5, 6, 7, 8, 9]):
    amplifiers = [Computer(x, inputs=[p]) for p in pc]
    amplifiers[0].inputs.append(0)  # start with signal 0
    for i_amp in cycle(range(5)):
        try:
            signal = next(amplifiers[i_amp].run())
            amplifiers[(i_amp + 1) % 5].inputs.append(signal)
        except StopIteration:
            break

    max_signal = max(max_signal, signal)  # last signal sent to thrusters

print(f"part 2: {max_signal}")
