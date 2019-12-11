"""
A module of mass 14 requires 2 fuel. This fuel requires no further fuel (2 divided by 3 and rounded down is 0, which would call for a negative fuel), so the total fuel required is still just 2.
At first, a module of mass 1969 requires 654 fuel. Then, this fuel requires 216 more fuel (654 / 3 - 2). 216 then requires 70 more fuel, which requires 21 fuel, which requires 5 fuel, which requires no further fuel. So, the total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
The fuel required by a module of mass 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
What is the sum of the fuel requirements for all of the modules on your spacecraft when also taking into account the mass of the added fuel? (Calculate the fuel requirements for each module separately, then add them all up at the end.)
"""

import math

def fuel_for_module(mass):
    return max(0, math.floor(mass/3.0) - 2)

assert fuel_for_module(12) == 2
assert fuel_for_module(14) == 2
assert fuel_for_module(1969) == 654
assert fuel_for_module(100756) == 33583

def get_input(path):
    with open(path) as f:
        lines = f.readlines()
    masses = [float(l) for l in lines]
    return masses

def fuel_for_module_and_fuel(mass):
    fuel_per_mass = []
    current_mass = mass
    while current_mass > 0:
        more_mass = fuel_for_module(current_mass)
        current_mass = more_mass
        fuel_per_mass.append(current_mass)
    return sum(fuel_per_mass)

assert fuel_for_module_and_fuel(14) == 2
assert fuel_for_module_and_fuel(1969) == 966
assert fuel_for_module_and_fuel(100756) == 50346

if __name__ == "__main__":
    masses = get_input("input.txt")

    # first part of the problem
    fuel_for_modules = [fuel_for_module(m) for m in masses]
    print("fuel for all modules:", sum(fuel_for_modules))

    # second part of the problem
    fuel_for_all = [fuel_for_module_and_fuel(m) for m in masses]
    print("fuel for all modules and fuel:", sum(fuel_for_all))
