# password rules
# 6 digit
# within input range
# two adjacent digits are same
# left digit <= right

def check_valid(passwd):
    passwd = str(passwd)
    assert len(passwd) == 6
    for i in range(len(passwd)-1):
        if passwd[i] > passwd[i+1]:
            return False
    split = [c for c in passwd]
    if len(list(set(split))) == 6:
        return False
    return True

assert check_valid(111111) == True
assert check_valid(223450) == False
assert check_valid(123789) == False

def check_valid_two(passwd):
    passwd = str(passwd)
    assert len(passwd) == 6
    for i in range(len(passwd)-1):
        if passwd[i] > passwd[i+1]:
            return False
    split = [c for c in passwd]
    last_num = 0
    group_length = 1
    for c in passwd:
        c = int(c)
        if (c != last_num) and group_length == 2:
            return True
        if c == last_num:
            group_length += 1
        else:
            group_length = 1
        last_num = c
    if (group_length == 2):
        return True
    else:
        return False

assert check_valid_two(112233) == True
assert check_valid_two(123444) == False
assert check_valid_two(111122) == True

if __name__ == '__main__':
    puzzle_input = [353096,843212]

    # first part
    is_valid = []
    for i in range(puzzle_input[0], puzzle_input[1]+1):
        is_valid.append(check_valid(i))
    print("sum", sum(is_valid))

    # second part
    is_valid = []
    for i in range(puzzle_input[0], puzzle_input[1]+1):
        is_valid.append(check_valid_two(i))
    print("sum", sum(is_valid))
