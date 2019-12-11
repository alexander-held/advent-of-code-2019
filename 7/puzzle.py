import copy

opcodes = [1, 2, 3, 4, 99]
# 1: read values at the two following indices, save to third index
# 2: same but multiply
# 3: input saved to following position
# 4: output saved to following position
# 99: stop program
# after processing: move forward 4 positions

# inputs to code:
# [0,1,2,3,4] each used exactly once

isFirstInput = [True, True, True, True, True]

global output_value

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

def process_code(code, INPUT, verbose=False, entrypoint=0, amplifier_index=None):
    global output_value
    global isFirstInput
    input_index = 0
    #print("input is", INPUT)
    i = entrypoint # position in code, "instruction pointer"
    #if verbose: print("entrypoint is", i)
    #if verbose: print(code)
    while i < len(code):
        code_str = str(code[i]).zfill(5)
        opcode = int(code_str[-2:])
        len_params = len(code_str) - 2
        modes = [int(code_str[k]) for k in range(len_params)][::-1]
        #print(code)
        #print("opcode", opcode)
        #input()

        if opcode==99:
            if verbose:
                print("end of program, output is", output_value)
            return None, output_value #code

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
            # output
            if modes[0] == 0:
                output_value = code[code[i+1]]
            elif modes[0] == 1:
                output_value = code[i+1]
            if verbose: output_stuff(output_value)
            i += 2
            #print(code, i, code[i])
            #return output_value
            return i, output_value #code

        elif opcode==3:
            # input
            if modes[0] == 0:
                output_index = code[i+1]
            elif modes[0] == 1:
                print("writing location in immediate mode!")
                raise SystemExit
            if amplifier_index == None:
                code = save_input(code, INPUT[input_index], output_index)
                input_index += 1
            else:
                if isFirstInput[amplifier_index]:
                    code = save_input(code, INPUT[0], output_index)
                    isFirstInput[amplifier_index] = False
                else:
                    code = save_input(code, INPUT[1], output_index)
            i += 2

        elif opcode==1:
            # addition
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
            # multiplication
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

def run_in_order(code, input_signal, order, verbose=False):
    len_seq = len(order)
    code = [copy.deepcopy(code) for i in range(len_seq)]
    signal = [None for i in range(len_seq+1)] # 4 inputs + output
    signal[0] = input_signal
    for i in range(len_seq):
        _, signal[i+1] = process_code(code[i], [order[i], signal[i]], verbose=verbose)
    return signal[-1]

def run_feedback(code, order, verbose=False):
    global isFirstInput
    isFirstInput = [True, True, True, True, True]
    len_seq = len(order)
    res = 0
    nRunsMax = 20
    code = [copy.deepcopy(code) for i in range(len_seq)]
    last_pos = [0 for i in range(len_seq)]
    for iRun in range(nRunsMax):
        print("----- run", iRun)
        for i in range(len_seq):
            j, res = process_code(code[i], [order[i], res], entrypoint=last_pos[i],
                                  verbose=verbose, amplifier_index=i)
            last_pos[i] = j
        if j == None:
            break
    print("-> result is", res)
    return res

def get_input(path):
    with open(path) as f:
        lines = f.readlines()
    assert(len(lines)) == 1
    code = lines[0].split(",")
    code = [int(c) for c in code]
    return code

def find_optimal(code, sequence, verbose=False, isPartTwo=False):
    import itertools
    all_permutations = list(itertools.permutations(sequence))
    nPerm = len(all_permutations)
    code_copies = [copy.deepcopy(code) for i in range(nPerm)]
    res = [None for i in range(nPerm)]
    for i in range(nPerm):
        if not isPartTwo:
            res[i] = run_in_order(code_copies[i], 0, list(all_permutations)[i], verbose=verbose)
        else:
            print("now testing", list(list(all_permutations)[i]))
            res[i] = run_feedback(code_copies[i], list(list(all_permutations)[i]), verbose=verbose)
    # find max
    index_max = res.index(max(res))
    print("max is perm", all_permutations[index_max], "with", res[index_max])

if __name__ == '__main__':
    #process_code([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0)
    #process_code([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], )
    #process_code([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,\
    #               1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,\
    #               999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 12)

    # some tests
    input_signal = 0
    order = [4,3,2,1,0]
    code = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    assert run_in_order(code, input_signal, order) == 43210

    order = [0,1,2,3,4]
    code = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    assert run_in_order(code, input_signal, order) == 54321

    order = [1,0,4,3,2]
    code = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    assert run_in_order(code, input_signal, order) == 65210

    # part 1
    code = get_input("input.txt")
    sequence = [0,1,2,3,4]
    find_optimal(code, sequence, verbose=False)

    print("----"*15)

    # checks for part 2
    code = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    order = [9,8,7,6,5]
    #isFirstInput = [True, True, True, True, True]
    assert run_feedback(code, order, verbose=False) == 139629729

    code = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    order = [9,7,8,5,6]
    #isFirstInput = [True, True, True, True, True]
    assert run_feedback(code, order, verbose=False) == 18216

    # part 2
    code = get_input("input.txt")
    order = [5,6,7,8,9]
    #run_feedback(code, order, verbose=True)
    find_optimal(code, order, isPartTwo=True)

