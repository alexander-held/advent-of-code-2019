def ():
    return

def get_input(path):
    with open(path) as f:
        lines = f.readlines()
    return lines

if __name__ == '__main__':
    get_input("input.txt")
    print()
