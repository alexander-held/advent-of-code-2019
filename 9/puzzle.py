import copy

opcodes = [1, 2, 3, 4, 99]
# 1: read values at the two following indices, save to third index
# 2: same but multiply
# 3: input saved to following position
# 4: output saved to following position
# 99: stop program
# after processing: move forward 4 positions

def output_stuff(value):
    print("output is", value)

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

def process_code(code, INPUT):
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
    process_code([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99],0)
    assert len(str(process_code([1102,34915192,34915192,7,4,7,99,0], 0))) == 16
    assert process_code([104,1125899906842624,99], 0) == 1125899906842624

    # part 1
    code = get_input("input.txt")
    INPUT = 1
    process_code(code, INPUT)

    # part 2
    code = get_input("input.txt")
    INPUT = 2
    process_code(code, INPUT)
