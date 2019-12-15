import copy
import time
import numpy as np

opcodes = [1, 2, 3, 4, 99]
# 1: read values at the two following indices, save to third index
# 2: same but multiply
# 3: input saved to following position
# 4: output saved to following position
# 99: stop program
# after processing: move forward 4 positions

INPUT = 4 #[4,4,4, G
INPUT_INDEX = 0
ITERATION = 0


gridsize_x = 101
gridsize_y = 51
GRID = np.zeros(shape=(gridsize_y,gridsize_x))
GRID -= 1
WAS_PAINTED = np.zeros(shape=(gridsize_y,gridsize_x))
offset = 30 #int((gridsize-1)*0.5)

class Robot:
    def __init__(self, offset):
        self.pos_x = offset
        self.pos_y = offset
    def move(self, direction):
        if direction==1:
            self.pos_y += 1 #north
        elif direction==2:
            self.pos_y -= 1 #south
        elif direction==3:
            self.pos_x -= 1 #west
        elif direction==4:
            self.pos_x += 1 #east
    def get_new_pos(self, direction):
        if direction==1:
            return (self.pos_x, self.pos_y+1)
        elif direction==2:
            return (self.pos_x, self.pos_y-1)
        elif direction==3:
            return (self.pos_x-1, self.pos_y)
            self.pos_x -= 1 #west
        elif direction==4:
            return (self.pos_x+1, self.pos_y)

def print_grid(robot):
    # 0: wall, 1: grid
    strings = []
    for i in range(len(GRID)):
        string = ""
        for j in range(len(GRID[0])):
            if robot.pos_x == i and robot.pos_y == j:
                string += "r"
            elif GRID[i,j] == -1:
                string += " "
            elif GRID[i,j] == 0:
                string += "#"
            elif GRID[i,j] == 1:
                string += "."
            elif GRID[i,j] == 2:
                string += "@"
        strings.append(string)
        #print(string)
    #    string += "\n"
    with open("maze.txt", "w") as f:
        for string in strings:
            f.write(string + "\n")

def output_stuff(value):
    #print("output is", value)
    pass

def save_input(code, what, where):
    code[where] = what
    return code

def add(code, input_1, input_2, output_index):
    code[output_index] = input_1 + input_2
    return code

def multiply(code, input_1, input_2, output_index):
    code[output_index] = input_1 * input_2
    return code

def position_mode(code, index, relative_base):
    res = code[code[index] + relative_base]
    #print("pos mode returning", res)
    return res

def position_mode_index(code, index, relative_base):
    res = code[index] + relative_base
    #print("pos index returning", res)
    return res

def process_code(code, robot, isPartTwo=False):
    global INPUT
    global INPUT_INDEX
    global GRID
    global ITERATION
    extension_size = 1000
    code = code + [0 for i in range(extension_size)]
    i = 0 # position in code, "instruction pointer"
    relative_base = 0
    while i < len(code):
        code_str = str(code[i]).zfill(5)
        opcode = int(code_str[-2:])
        len_params = len(code_str) - 2
        modes = [int(code_str[k]) for k in range(len_params)][::-1]
        #print(code)
        #print("opcode", opcode, "modes", modes)
        #input()

        if opcode==99:
            print("quitting now")
            return output_value

        if opcode==5:
            # jump if true
            if modes[0] == 0:
                input_1 = code[code[i+1]]
            elif modes[0] == 1:
                input_1 = code[i+1]
            elif modes[0] == 2:
                input_1 = position_mode(code, i+1, relative_base)
            if modes[1] == 0:
                input_2 = code[code[i+2]]
            elif modes[1] == 1:
                input_2 = code[i+2]
            elif modes[1] == 2:
                input_2 = position_mode(code, i+2, relative_base)
            if input_1 != 0:
                i = input_2
                #print("seting pointer to", i)
                continue
            else:
                i += 3

        if opcode==6:
            # jump if false
            if modes[0] == 0:
                input_1 = code[code[i+1]]
            elif modes[0] == 1:
                input_1 = code[i+1]
            elif modes[0] == 2:
                input_1 = position_mode(code, i+1, relative_base)
            if modes[1] == 0:
                input_2 = code[code[i+2]]
            elif modes[1] == 1:
                input_2 = code[i+2]
            elif modes[1] == 2:
                input_2 = position_mode(code, i+2, relative_base)
            if input_1 == 0:
                i = input_2
                #print("seting pointer to", i)
                continue
            else:
                i += 3

        if opcode==7:
            # less than
            if modes[0] == 0:
                input_1 = code[code[i+1]]
            elif modes[0] == 1:
                input_1 = code[i+1]
            elif modes[0] == 2:
                input_1 = position_mode(code, i+1, relative_base)
            if modes[1] == 0:
                input_2 = code[code[i+2]]
            elif modes[1] == 1:
                input_2 = code[i+2]
            elif modes[1] == 2:
                input_2 = position_mode(code, i+2, relative_base)
            if modes[2] == 0:
                output_index = code[i+3]
            elif modes[2] == 1:
                print("writing location in immediate mode!")
                raise SystemExit
            elif modes[2] == 2:
                output_index = position_mode_index(code, i+3, relative_base)
            if input_1 < input_2:
                code[output_index] = 1
            else:
                code[output_index] = 0
            i += 4

        if opcode==8:
            # equal
            if modes[0] == 0:
                input_1 = code[code[i+1]]
            elif modes[0] == 1:
                input_1 = code[i+1]
            elif modes[0] == 2:
                input_1 = position_mode(code, i+1, relative_base)
            if modes[1] == 0:
                input_2 = code[code[i+2]]
            elif modes[1] == 1:
                input_2 = code[i+2]
            elif modes[1] == 2:
                input_2 = position_mode(code, i+2, relative_base)
            if modes[2] == 0:
                output_index = code[i+3]
            elif modes[2] == 1:
                print("writing location in immediate mode!")
                raise SystemExit
            elif modes[2] == 2:
                output_index = position_mode_index(code, i+3, relative_base)
            if input_1 == input_2:
                code[output_index] = 1
            else:
                code[output_index] = 0
            i += 4

        elif opcode==9:
            # adjust relative base
            if modes[0] == 0:
                adjust_value = code[code[i+1]]
            elif modes[0] == 1:
                adjust_value = code[i+1]
            elif modes[0] == 2:
                adjust_value = position_mode(code, i+1, relative_base)
            relative_base += adjust_value
            #print("adjusting base, now base is", relative_base)
            i += 2

        elif opcode==4:
            # output
            if modes[0] == 0:
                output_value = code[code[i+1]]
            elif modes[0] == 1:
                output_value = code[i+1]
            elif modes[0] == 2:
                output_value = position_mode(code, i+1, relative_base)
            output_stuff(output_value)
            #current_input = INPUT[INPUT_INDEX]
            if output_value == 0:
                # hit wall, position unchanged
                GRID[robot.get_new_pos(INPUT)] = 0
                #INPUT = int(input("enter new dir [1-4]: "))
            elif output_value == 1:
                # move successful
                GRID[robot.get_new_pos(INPUT)] = 1
                robot.move(INPUT)
            elif output_value == 2:
                print("found oxygen system at", robot.pos_x, robot.pos_y)
                print_grid(robot)
                if not isPartTwo:
                    raise SystemExit
                else:
                    GRID[robot.get_new_pos(INPUT)] = 2
                    robot.move(INPUT)
            INPUT = np.random.randint(4)+1
            if ITERATION % 10000 == 0 and ITERATION > 0:
                print_grid(robot)
            ITERATION += 1
            i += 2

        elif opcode==3:
            # input
            if modes[0] == 0:
                output_index = code[i+1]
            elif modes[0] == 1:
                print("writing location in immediate mode!")
                raise SystemExit
            elif modes[0] == 2:
                output_index = position_mode_index(code, i+1, relative_base)
            code = save_input(code, INPUT, output_index)
            i += 2

        elif opcode==1:
            if modes[0] == 0:
                input_1 = code[code[i+1]]
            elif modes[0] == 1:
                input_1 = code[i+1]
            elif modes[0] == 2:
                input_1 = position_mode(code, i+1, relative_base)
            if modes[1] == 0:
                input_2 = code[code[i+2]]
            elif modes[1] == 1:
                input_2 = code[i+2]
            elif modes[1] == 2:
                input_2 = position_mode(code, i+2, relative_base)
            if modes[2] == 0:
                output_index = code[i+3]
            elif modes[2] == 1:
                print("writing location in immediate mode!")
                raise SystemExit
            elif modes[2] == 2:
                output_index = position_mode_index(code, i+3, relative_base)
            code = add(code, input_1, input_2, output_index)
            i += 4

        elif opcode==2:
            if modes[0] == 0:
                input_1 = code[code[i+1]]
            elif modes[0] == 1:
                input_1 = code[i+1]
            elif modes[0] == 2:
                input_1 = position_mode(code, i+1, relative_base)
            if modes[1] == 0:
                input_2 = code[code[i+2]]
            elif modes[1] == 1:
                input_2 = code[i+2]
            elif modes[1] == 2:
                input_2 = position_mode(code, i+2, relative_base)
            if modes[2] == 0:
                output_index = code[i+3]
            elif modes[2] == 1:
                print("writing location in immediate mode!")
                raise SystemExit
            elif modes[2] == 2:
                output_index = position_mode_index(code, i+3, relative_base)
            code = multiply(code, input_1, input_2, output_index)
            i += 4

        #else:
        #    print("stuck at position", i, "with value", code[i])


def get_input(path):
    with open(path) as f:
        lines = f.readlines()
    assert(len(lines)) == 1
    code = lines[0].split(",")
    code = [int(c) for c in code]
    return code

if __name__ == '__main__':
    # part 1
    code = get_input("input.txt")
    robot = Robot(offset)
    process_code(code, robot, isPartTwo=False)

    # for part 2, run this instead of the processing above
    process_code(code, robot, isPartTwo=True)

    # the solution requires a manual step afterwards, reading
    # the maze by hand, cutting off small branches and counting
    # the path length by looking for instances of "."
    # I expected this to be faster for me to implement than to count
    # the path length automatically
