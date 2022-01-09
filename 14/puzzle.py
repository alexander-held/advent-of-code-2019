import fileinput
from collections import defaultdict
from math import ceil

x = [line.strip() for line in fileinput.input()]

recipes = {}  # product: requirements
for line in x:
    inp, outp = line.split(" => ")
    material = dict((mat.split()[1], int(mat.split()[0])) for mat in inp.split(", "))
    num_out = int(outp.split()[0])
    mat_out = outp.split()[1]
    recipes.update({mat_out: {"num_produced": num_out, "material": material}})


def ore_required(num_fuel=1):
    required = defaultdict(int)  # things still required
    required.update({"FUEL": num_fuel})

    ore_required = 0
    while any([v > 0 for v in required.values()]):
        # process first material of which positive amount is still needed
        mat, amount = next((k, v) for k, v in required.items() if v > 0)
        num_produced = recipes[mat]["num_produced"]
        num_crafts_needed = ceil(amount / num_produced)

        # record requirements to craft material (scaled by required # of crafts)
        ingredients = recipes[mat]["material"]
        for ing, ing_amount in ingredients.items():
            # if ingredient is ore, don't add it to dict (fundamental ingredient)
            if ing == "ORE":
                ore_required += ing_amount * num_crafts_needed
                continue
            else:
                required[ing] += ing_amount * num_crafts_needed

        # record material that was just replaced by its ingredients
        required[mat] -= num_produced * num_crafts_needed  # can be negative with excess

    return ore_required


ore_for_1_fuel = ore_required()
print(f"part 1: {ore_for_1_fuel}")

# part 2: lower bound for # crafts is 10**12 // ore for single piece of fuel
lower_bound = 10 ** 12 // ore_for_1_fuel
bounds = [lower_bound, int(lower_bound * 1.5)]  # use 50% larger value as upper bound

# bisect until convergence
while (bounds[1] - bounds[0]) > 1:
    num_fuel = (bounds[1] + bounds[0]) // 2
    num_ore = ore_required(num_fuel=num_fuel)
    if num_ore > 10 ** 12:
        bounds = [bounds[0], num_fuel]  # update upper bound
    else:
        bounds = [num_fuel, bounds[1]]  # update upper bound

# solution is lower bound, upper bound is too large by definition
print(f"part 2: {bounds[0]}")
