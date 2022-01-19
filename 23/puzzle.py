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
        self.last_input_default = False  # last input was default (-1)

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
                if len(self.inputs):
                    operator = lambda: self.inputs.popleft()
                elif not self.last_input_default:
                    operator = lambda: -1  # empty packet queue
                    self.last_input_default = True
                else:
                    # already got default input last time, stop for now
                    self.last_input_default = False  # reset for next execution
                    break
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


computers = [Computer(x, [i]) for i in range(50)]
nat = None
last_nat_y_delivered = None
while True:
    message_sent = False
    for i, comp in enumerate(computers):
        try:
            # get three outputs at once for a full message
            message = [next(computers[i].run()) for _ in range(3)]
            message_sent = True
            if message[0] == 255:
                if nat is None:  # first packet
                    print(f"part 1: {message[2]}")
                nat = [message[1], message[2]]
            else:
                # add message to input queue
                computers[message[0]].inputs += message[1:]
        except StopIteration:
            pass  # no message to send

    # network is idle if no message was sent this round, then NAT sends a message
    if not message_sent:
        computers[0].inputs += nat
        if nat[1] == last_nat_y_delivered:
            print(f"part 2: {nat[1]}")
            break
        last_nat_y_delivered = nat[1]
