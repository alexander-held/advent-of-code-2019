import numpy as np
import time

opcodes = [1, 2, 3, 4, 99]
# 1: read values at the two following indices, save to third index
# 2: same but multiply
# 3: input saved to following position
# 4: output saved to following position
# 99: stop program
# after processing: move forward 4 positions

huge_list = []
output_buffer = []


def output_stuff(value):
    global huge_list

    # figure out whether position already exists within list
    nTiles = int(len(huge_list) / 3)
    newX = value[0]
    newY = value[1]
    updated = False
    for i in range(nTiles):
        posX = huge_list[i*3+0]
        posY = huge_list[i*3+1]
        # print(posX, posY, newX, newY)
        if newX == posX and newY == posY:
            if newX == -1 and newY == 0 and value[2] == 0:
                print("game over, new score would be 0, will not update score")
            else:
                huge_list[i*3+2] = value[2]
            # print("overwriting", value)
            updated = True
            return True

    # otherwise append
    if not updated:
        # print("appending", value)
        huge_list += value
        return False


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
    return res


def position_mode_index(code, index, relative_base):
    res = code[index] + relative_base
    return res


def process_code(code):
    INPUT = 0
    extension_size = 1000
    code = code + [0 for i in range(extension_size)]
    i = 0  # position in code, "instruction pointer"
    relative_base = 0
    global output_buffer
    while i < len(code):
        code_str = str(code[i]).zfill(5)
        opcode = int(code_str[-2:])
        len_params = len(code_str) - 2
        modes = [int(code_str[k]) for k in range(len_params)][::-1]

        if opcode == 99:
            # print("quitting now")
            return output_value

        if opcode == 5:
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
                # print("seting pointer to", i)
                continue
            else:
                i += 3

        if opcode == 6:
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
                # print("seting pointer to", i)
                continue
            else:
                i += 3

        if opcode == 7:
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

        if opcode == 8:
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

        elif opcode == 9:
            # adjust relative base
            if modes[0] == 0:
                adjust_value = code[code[i+1]]
            elif modes[0] == 1:
                adjust_value = code[i+1]
            elif modes[0] == 2:
                adjust_value = position_mode(code, i+1, relative_base)
            relative_base += adjust_value
            # print("adjusting base, now base is", relative_base)
            i += 2

        elif opcode == 4:
            # output
            if modes[0] == 0:
                output_value = code[code[i+1]]
            elif modes[0] == 1:
                output_value = code[i+1]
            elif modes[0] == 2:
                output_value = position_mode(code, i+1, relative_base)
            output_buffer.append(output_value)
            if len(output_buffer) == 3:
                if output_stuff(output_buffer):
                    draw()
                    time.sleep(0.01)
                output_buffer = []
            i += 2

        elif opcode == 3:
            # input

            # figure out where to tile stick to
            cur_x = find_paddle()
            ball_x = find_ball()
            if cur_x < ball_x:
                INPUT = 1
            elif cur_x > ball_x:
                INPUT = -1
            else:
                INPUT = 0

            if modes[0] == 0:
                output_index = code[i+1]
            elif modes[0] == 1:
                print("writing location in immediate mode!")
                raise SystemExit
            elif modes[0] == 2:
                output_index = position_mode_index(code, i+1, relative_base)
            code = save_input(code, INPUT, output_index)
            i += 2

        elif opcode == 1:
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

        elif opcode == 2:
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

        # else:
        #     print("stuck at position", i, "with value", code[i])


def get_input(path):
    with open(path) as f:
        lines = f.readlines()
    assert(len(lines)) == 1
    code = lines[0].split(",")
    code = [int(c) for c in code]
    return code


def find_paddle():
    global huge_list
    nTiles = int(len(huge_list) / 3)
    for i in range(nTiles):
        if huge_list[i*3+2] == 3:
            paddle_x = huge_list[i*3+0]
    return paddle_x


def find_ball():
    global huge_list
    nTiles = int(len(huge_list) / 3)
    ball_x = -99
    for i in range(nTiles):
        if huge_list[i*3+2] == 4:
            ball_x = huge_list[i*3+0]
    if ball_x == -99:
        print("could not find ball")
        raise SystemExit
    return ball_x


def draw():
    global huge_list
    nTiles = int(len(huge_list) / 3)
    gridsize_x = 40
    gridsize_y = 22
    grid = np.empty((gridsize_y, gridsize_x), dtype=np.dtype('U1'))
    grid[:] = " "  # initialize everything as blank space
    # x: distance from left
    # y: distance from right

    for i in range(nTiles):
        tileX = huge_list[i*3+0]
        tileY = huge_list[i*3+1]
        if tileX == -1 and tileY == 0:
            print("score is", huge_list[i*3+2])
            continue  # score
        tileKind = huge_list[i*3+2]
        if tileKind == 0:
            grid[tileY, tileX] = " "
        elif tileKind == 1:
            grid[tileY, tileX] = "█"
        elif tileKind == 2:
            grid[tileY, tileX] = "x"
        elif tileKind == 3:
            grid[tileY, tileX] = "_"
        elif tileKind == 4:
            grid[tileY, tileX] = "*"

    # draw the grid
    for g in grid:
        print("".join(g))

    for _ in range(8):
        print("\n")


if __name__ == '__main__':
    # part 1
    code = get_input("input.txt")
    process_code(code)
    draw()

    # part 2
    code = get_input("input.txt")
    code[0] = 2  # play for free
    process_code(code)
    draw()
