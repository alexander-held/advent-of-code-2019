import copy
import numpy as np


class Moon():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vel_x = 0
        self.vel_y = 0
        self.vel_z = 0

    def __repr__(self):
        return "pos x=" + str(self.x) + ", y=" + str(self.y) +\
               ", z=" + str(self.z) + " -- v_x=" + str(self.vel_x) +\
               ", v_y=" + str(self.vel_y) + ", v_z=" + str(self.vel_z)

    def update_velocity(self, other_moons):
        for moon in other_moons:
            if self.x != moon.x:
                self.vel_x += 1 if self.x < moon.x else -1
            if self.y != moon.y:
                self.vel_y += 1 if self.y < moon.y else -1
            if self.z != moon.z:
                self.vel_z += 1 if self.z < moon.z else -1

    def get_potential(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def get_kinetic(self):
        return abs(self.vel_x) + abs(self.vel_y) + abs(self.vel_z)

    def total_energy(self):
        return self.get_potential() * self.get_kinetic()

    def update_position(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.z += self.vel_z


def print_moons(moons, newline=False):
    for m in moons: print(m)
    if newline: print()


def simulate(moons, nSteps):
    print("At start:")
    print_moons(moons, newline=True)
    for step in range(1, nSteps+1):
        for moon in moons:
            other_moons = [m for m in moons if m != moon]
            moon.update_velocity(other_moons)
        for moon in moons:
            moon.update_position()
        # print("After", step, "steps:")
        # print_moons(moons, newline=True)

    # get the total energy
    tot_e = sum([m.total_energy() for m in moons])
    print("total energy is", tot_e)
    return tot_e


def check_equal(moons_1, moons_2, dim="A"):
    if dim == "A":
        for m1, m2 in zip(moons_1, moons_2):
            if (m1.x != m2.x) or (m1.y != m2.y) or (m1.z != m2.z):
                return False
            if (m1.vel_x != m2.vel_x) or (m1.vel_y != m2.vel_y) or (m1.vel_z != m2.vel_z):
                return False
        return True
    elif dim == "x":
        for m1, m2 in zip(moons_1, moons_2):
            if (m1.x != m2.x):
                return False
            if (m1.vel_x != m2.vel_x):
                return False
        return True
    elif dim == "y":
        for m1, m2 in zip(moons_1, moons_2):
            if (m1.y != m2.y):
                return False
            if (m1.vel_y != m2.vel_y):
                return False
        return True
    elif dim == "z":
        for m1, m2 in zip(moons_1, moons_2):
            if (m1.z != m2.z):
                return False
            if (m1.vel_z != m2.vel_z):
                return False
        return True


def run_until_same_state(moons, dim="A"):
    original_state = copy.deepcopy(moons)
    stepsMax = 1000000
    for step in range(1, stepsMax+1):
        for moon in moons:
            other_moons = [m for m in moons if m != moon]
            moon.update_velocity(other_moons)
        for moon in moons:
            moon.update_position()
        if check_equal(moons, original_state, dim=dim) and step > 1:
            break
    print("same state after", step, "steps")
    return step


def simulate_per_dim(moons):
    moons_x = copy.deepcopy(moons)
    moons_y = copy.deepcopy(moons)
    moons_z = copy.deepcopy(moons)

    steps_x = run_until_same_state(moons_x, dim="x")
    steps_y = run_until_same_state(moons_y, dim="y")
    steps_z = run_until_same_state(moons_z, dim="z")

    # find least common multiple
    lcm = np.lcm.reduce([steps_x, steps_y, steps_z])
    print("lcm is", lcm)
    return lcm


def get_input(path):
    with open(path) as f:
        lines = f.readlines()
    moon_list = []
    for line in lines:
        split = line.replace(">", "").replace("<", "").strip().split(",")
        coords = [float(s.split("=")[-1]) for s in split]
        new_coord = Moon(*coords)
        moon_list.append(new_coord)
    return moon_list


if __name__ == '__main__':
    # example 1
    moons = get_input("example_1.txt")
    assert simulate(moons, 10) == 179

    moons = get_input("example_2.txt")
    assert simulate(moons, 100) == 1940

    # part 1
    moons = get_input("input.txt")
    simulate(moons, 1000)

    # part 2
    # example 4686774924 factorizes:
    # 2^2
    # 3
    # 13^2
    # 983
    # 2351
    moons = get_input("example_1.txt")
    assert simulate_per_dim(moons) == 2772

    moons = get_input("example_2.txt")
    assert simulate_per_dim(moons) == 4686774924

    moons = get_input("input.txt")
    simulate_per_dim(moons)
