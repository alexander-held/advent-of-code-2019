width = 25
height = 6
layer_pixels = width*height

# 0: black
# 1: white
# 2: transparent
# color is first non-transparent pixel

def count(layer, char):
    tmp = [c for c in layer if c == char]
    return len(tmp)

def find_best(split_img):
    layer_best = -1
    n_zero = len(split_img)*layer_pixels
    for i, layer in enumerate(split_img):
        cur_count = count(layer, "0")
        if cur_count < n_zero:
            layer_best = i
            n_zero = cur_count
    print("best layer is", i, "with count", n_zero)
    return split_img[layer_best]

def compute_part_1(l):
    n_1 = count(l, "1")
    n_2 = count(l, "2")
    res = n_1 * n_2
    print("solution is", res)

def get_input(path):
    with open(path) as f:
        lines = f.readlines()
    assert(len(lines)) == 1
    img = lines[0].strip()
    assert len(img) % layer_pixels == 0
    nlayers = int(len(img) / layer_pixels)
    print("found", nlayers, "layers")
    split_img = [img[i*layer_pixels:(i+1)*layer_pixels] for i in range(nlayers)]
    return split_img

def stack_image(split_img):
    full = []
    cur_char = "2"
    for j in range(height):
        for i in range(width):
            # loop through image until something other than "2" is found
            for l in split_img:
                candidate = l[i+j*width]
                if cur_char == "2" and candidate != "2":
                    cur_char = candidate
                    #print("found new char to replace at index", i+j*width, ":", candidate)
                    break
            full.append(cur_char)
            cur_char = "2"
    return full

def print_stack(s):
    for j in range(height):
        for i in range(width):
            if s[i+j*width] == "0":
                char = "⬛"
            elif s[i+j*width] == "1":
                char = "⬜"
            else:
                char = " "
            print(char, end="")
        print()

if __name__ == '__main__':
    split_img = get_input("input.txt")
    best_layer = find_best(split_img)
    compute_part_1(best_layer)

    # second part
    stacked = stack_image(split_img)
    print_stack(stacked)
