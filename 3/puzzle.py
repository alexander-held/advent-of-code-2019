import math
import numpy as np
np.set_printoptions(linewidth=150)

gridsize = 25001
center = [int(0.5*(gridsize-1)), int(0.5*(gridsize-1))]
oned = np.zeros(gridsize)
grid_1 = np.array([[oned for i in range(gridsize)]], dtype=int)[0]
grid_2 = np.array([[oned for i in range(gridsize)]], dtype=int)[0]
#grid[center[0],center[1]] = 3

def abs_corrd_to_index(x, y):
    size_in_one_direction = math.floor(gridsize/2.0)
    if abs(x) > size_in_one_direction:
        print("grid not large enough, need to go to", x)
    elif abs(y) > size_in_one_direction:
        print("grid not large enough, need to go to", y)
    return x+center[0], y+center[1]

def get_input(path):
    with open(path) as f:
        lines = f.readlines()
    assert len(lines) == 2
    path_1 = lines[0]
    path_2 = lines[1]
    return path_1, path_2

def go_path(path, grid):
    cur_pos = [0, 0]
    path = path.split(",")
    for p in path:
        d = p[0]
        l = int(p[1:])
        if p[0] == "R":
            for i in range(1, l):
                if grid[abs_corrd_to_index(cur_pos[0], cur_pos[1]+i)] != 1:
                  grid[abs_corrd_to_index(cur_pos[0], cur_pos[1]+i)] += 1
            cur_pos[1] += l
        elif p[0] == "L":
            for i in range(1, l):
                if grid[abs_corrd_to_index(cur_pos[0], cur_pos[1]-i)] != 1:
                  grid[abs_corrd_to_index(cur_pos[0], cur_pos[1]-i)] += 1
            cur_pos[1] -= l
        elif p[0] == "U":
            for i in range(1, l):
                if grid[abs_corrd_to_index(cur_pos[0]-i, cur_pos[1])] != 1:
                  grid[abs_corrd_to_index(cur_pos[0]-i, cur_pos[1])] += 1
            cur_pos[0] -= l
        elif p[0] == "D":
            for i in range(1, l):
                if grid[abs_corrd_to_index(cur_pos[0]+i, cur_pos[1])] != 1:
                  grid[abs_corrd_to_index(cur_pos[0]+i, cur_pos[1])] += 1
                #print("U", cur_pos[0], cur_pos[1]+i)
            cur_pos[0] += l
        else:
            print("parse error")
        grid[abs_corrd_to_index(cur_pos[0], cur_pos[1])] += 1

def get_cross(g1, g2):
    g = g1+g2
    w = np.where(g==2)
    closest_distance = 9999999999
    f = open("crossings.txt", "w")
    for i in range(len(w[0])):
        x = w[0][i] - center[0]
        y = w[1][i] - center[1]
        f.write(str(x) + "," + str(y) + "\n")
        print(x,y)
        if (abs(x) + abs(y) <= closest_distance):
            closest_distance = abs(x) + abs(y)
    print("closest distance is", closest_distance)
    f.close()
    return closest_distance

# some tests
#assert calc(0) == 0

def get_crossings(fpath):
    with open(fpath) as f:
        lines = f.readlines()
    c = []
    for line in lines:
        s = line.split(",")
        c.append([int(s[0]), int(s[1])])
    return c

def get_steps(path, crossing):
    #print("want to get to", crossing)
    path = path.split(",")
    steps = 0
    cur_pos = [0, 0]
    for p in path:
        #print(p)
        d = p[0]
        l = int(p[1:])
        if p[0] == "R":
            for i in range(1, l+1):
                cur_pos[1] += 1
                steps += 1
                if crossing[0] == cur_pos[0] and crossing[1] == cur_pos[1]:
                    return steps
        elif p[0] == "L":
            for i in range(1, l+1):
                cur_pos[1] -= 1
                steps += 1
                if crossing[0] == cur_pos[0] and crossing[1] == cur_pos[1]:
                    return steps
        elif p[0] == "U":
            for i in range(1, l+1):
                cur_pos[0] -= 1
                steps += 1
                if crossing[0] == cur_pos[0] and crossing[1] == cur_pos[1]:
                    return steps
        elif p[0] == "D":
            for i in range(1, l+1):
                cur_pos[0] += 1
                steps += 1
                if crossing[0] == cur_pos[0] and crossing[1] == cur_pos[1]:
                    return steps
        else:
            print("parse error")


if __name__ == '__main__':
    path_1, path_2 = get_input("input.txt")
    crossings = get_crossings("crossings.txt")

    #path_1 = "R8,U5,L5,D3"
    #path_2 = "U7,R6,D4,L4"
    # -> 6

    #path_1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    #path_2 = "U62,R66,U55,R34,D71,R55,D58,R83"
    # -> 159

    steps_per_c_1 = []
    steps_per_c_2 = []
    for c in crossings:
        steps_per_c_1.append(get_steps(path_1, c))
        steps_per_c_2.append(get_steps(path_2, c))
    print(steps_per_c_1)
    print(steps_per_c_2)
    sum_steps = np.asarray(steps_per_c_1) + np.asarray(steps_per_c_2)
    print("min steps", min(sum_steps))

    raise SystemExit

    #path_1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
    #path_2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
    # -> 135

    #path_1, path_2 = get_input("input.txt")
    # -> not 117

    go_path(path_1, grid_1)
    print(grid_1)
    go_path(path_2, grid_2)
    print(grid_2)
    print(get_cross(grid_1, grid_2))

