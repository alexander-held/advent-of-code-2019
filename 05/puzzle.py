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

def process_code(code, INPUT):
    i = 0 # position in code, "instruction pointer"
    while i < len(code):
        code_str = str(code[i]).zfill(5)
        opcode = int(code_str[-2:])
        len_params = len(code_str) - 2
        modes = [int(code_str[k]) for k in range(len_params)][::-1]
        #print(code)
        #print("opcode", opcode)
        #input()

        if opcode==99:
            return code

        if opcode==5:
            # jump if true
            if modes[0] == 0:
                input_1 = code[code[i+1]]
            elif modes[0] == 1:
                input_1 = code[i+1]
            if modes[1] == 0:
                input_2 = code[code[i+2]]
            elif modes[1] == 1:
                input_2 = code[i+2]
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
            if modes[1] == 0:
                input_2 = code[code[i+2]]
            elif modes[1] == 1:
                input_2 = code[i+2]
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
            if modes[1] == 0:
                input_2 = code[code[i+2]]
            elif modes[1] == 1:
                input_2 = code[i+2]
            if modes[2] == 0:
                output_index = code[i+3]
            elif modes[2] == 1:
                print("writing location in immediate mode!")
                raise SystemExit
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
            if modes[1] == 0:
                input_2 = code[code[i+2]]
            elif modes[1] == 1:
                input_2 = code[i+2]
            if modes[2] == 0:
                output_index = code[i+3]
            elif modes[2] == 1:
                print("writing location in immediate mode!")
                raise SystemExit
            if input_1 == input_2:
                code[output_index] = 1
            else:
                code[output_index] = 0
            i += 4

        elif opcode==4:
            if modes[0] == 0:
                output_value = code[code[i+1]]
            elif modes[0] == 1:
                output_value = code[i+1]
            output_stuff(output_value)
            i += 2

        elif opcode==3:
            if modes[0] == 0:
                output_index = code[i+1]
            elif modes[0] == 1:
                print("writing location in immediate mode!")
                raise SystemExit
            code = save_input(code, INPUT, output_index)
            i += 2

        elif opcode==1:
            if modes[0] == 0:
                input_1 = code[code[i+1]]
            elif modes[0] == 1:
                input_1 = code[i+1]
            if modes[1] == 0:
                input_2 = code[code[i+2]]
            elif modes[1] == 1:
                input_2 = code[i+2]
            if modes[2] == 0:
                output_index = code[i+3]
            elif modes[2] == 1:
                print("writing location in immediate mode!")
                raise SystemExit
            code = add(code, input_1, input_2, output_index)
            i += 4

        elif opcode==2:
            if modes[0] == 0:
                input_1 = code[code[i+1]]
            elif modes[0] == 1:
                input_1 = code[i+1]
            if modes[1] == 0:
                input_2 = code[code[i+2]]
            elif modes[1] == 1:
                input_2 = code[i+2]
            if modes[2] == 0:
                output_index = code[i+3]
            elif modes[2] == 1:
                print("writing location in immediate mode!")
                raise SystemExit
            code = multiply(code, input_1, input_2, output_index)
            i += 4

        #else:
        #    print("stuck at position", i, "with value", code[i])


#assert process_code([1,9,10,3,2,3,11,0,99,30,40,50]) ==\
#                    [3500,9,10,70,2,3,11,0,99,30,40,50]
#assert process_code([1,0,0,0,99]) == [2,0,0,0,99]
#assert process_code([2,3,0,3,99]) == [2,3,0,6,99]
#assert process_code([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
#assert process_code([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

#assert process_code([1002,4,3,4,33], 77) == [1002,4,3,4,99]

def get_input(path):
    with open(path) as f:
        lines = f.readlines()
    assert(len(lines)) == 1
    code = lines[0].split(",")
    code = [int(c) for c in code]
    return code

if __name__ == '__main__':
    code = get_input("input.txt")
    #process_code([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0)
    #process_code([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], )
    #process_code([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,\
    #               1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,\
    #               999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 12)

    # part 1
    INPUT = 1
    process_code(code, INPUT)

    # part 2
    INPUT = 5
    process_code(code, INPUT)


