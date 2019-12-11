import copy

opcodes = [1, 2, 99]
# 1: read values at the two following indices, save to third index
# 2: same but multiply
# 99: stop program
# after processing: move forward 4 positions

def process_code(code):
    i = 0 # position in code, "instruction pointer"
    while i < len(code):
        if code[i] == 1:
            code = add(code, code[i+1], code[i+2], code[i+3])
            i += 4
        elif code[i] == 2:
            code = multiply(code, code[i+1], code[i+2], code[i+3])
            i += 4
        elif code[i] == 99:
            return code
        else:
            print("stuck at position", i, "with value", code[i])

def add(code, index_in_1, index_in_2, index_out):
    # index_in_1 is position of "noun"
    # index_in_2 is position of "verb"
    code[index_out] = code[index_in_1] + code[index_in_2]
    return code

def multiply(code, index_in_1, index_in_2, index_out):
    # index_in_1 is position of "noun"
    # index_in_2 is position of "verb"
    code[index_out] = code[index_in_1] * code[index_in_2]
    return code

assert process_code([1,9,10,3,2,3,11,0,99,30,40,50]) ==\
                    [3500,9,10,70,2,3,11,0,99,30,40,50]
assert process_code([1,0,0,0,99]) == [2,0,0,0,99]
assert process_code([2,3,0,3,99]) == [2,3,0,6,99]
assert process_code([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
assert process_code([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

def get_input(path):
    with open(path) as f:
        lines = f.readlines()
    assert(len(lines)) == 1
    code = lines[0].split(",")
    code = [int(c) for c in code]
    return code

def preprocess(code, noun, verb):
    code[1] = noun
    code[2] = verb
    return code

def first_part(code):
    print("input", code)
    code = preprocess(code, 12, 2)
    print("after preprocessing", code)
    code = process_code(code)
    print("after processing", code)
    print("solution", code[0])

def scan(code):
    maxval = 99
    for noun in range(0, maxval+1):
        for verb in range(0, maxval+1):
            code_copy = copy.deepcopy(code)
            code_copy = preprocess(code_copy, noun, verb)
            code_copy = process_code(code_copy)
            if code_copy[0] == 19690720:
                return noun, verb
    return 0, 0

def second_part(code):
    noun, verb = scan(code)
    print("noun and verb are", noun, verb)
    print("solution is", 100*noun+verb)

if __name__ == '__main__':
    code = get_input("input.txt")

    # first part of problem
    code_copy = copy.deepcopy(code)
    first_part(code_copy)

    # second part
    second_part(code)
