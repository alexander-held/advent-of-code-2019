class orbit:
    def __init__(self, input_str):
        input_str = input_str.strip()
        self.center = input_str.split(")")[0]
        self.satellite = input_str.split(")")[1]

class planet:
    def __init__(self, name, orbits):
        self.name = name
        self.center = ""
        for o in orbits:
            if o.satellite == self.name:
                self.center = o.center
        if self.center=="":
            print("could not find center for planet", self.name)

def get_center(planet, orbits):
    #print("finding center for", planet)
    for o in orbits:
        if o.satellite == planet:
            return o.center
    return False

def count_orbits(planets, orbits):
    orbits_total = 0
    for p in planets:
        #print("planet is", p)
        num_orbits = 0
        planet_in_chain = p
        while True:
            # current_center is planet_in_chain.center
            candidates = [p for p in planets if p.name == planet_in_chain.center]
            if len(candidates) == 0:
                break
            else:
                assert len(candidates) == 1
                planet_in_chain = candidates[0]
                num_orbits += 1
        #print("found", num_orbits, "orbits for", p)
        orbits_total += num_orbits
    return orbits_total

def get_roots(planets, orbits, name):
    base = [p for p in planets if p.name == name]
    assert len(base) == 1
    base = base[0]
    #print("starting from planet", base.name)
    centers = []
    while True:
        next_center = base.center
        candidates = [p for p in planets if p.name == next_center]
        if len(candidates) == 0:
            break
        else:
            assert len(candidates) == 1
            base = candidates[0]
            centers.append(base.name)
    #print("list of centers is", centers)
    return centers

def find_distance(planets, orbits):
    santas_roots = get_roots(planets, orbits, "SAN")
    my_roots = get_roots(planets, orbits, "YOU")
    #print(santas_roots)
    #print(my_roots)
    for r in my_roots:
        if r in santas_roots:
            break
    print("found shared root", r)
    my_distance_to_r = my_roots.index(r)
    santa_distance_to_r = santas_roots.index(r)
    total_dist = my_distance_to_r + santa_distance_to_r
    print("total distance is", total_dist)
    return total_dist

def get_planets(orbits):
    planets = []
    for o in orbits:
        planets.append(o.center)
        planets.append(o.satellite)
    planets = list(set(planets))
    print(" # found", len(planets), "planets")
    planets = [planet(p, orbits) for p in planets]
    return planets

def get_input(path):
    with open(path) as f:
        lines = f.readlines()
    orbits = []
    for line in lines:
        orbits.append(orbit(line))
    # find all roots
    return orbits

if __name__ == '__main__':
    # part 1 validation
    orbits = get_input("ex_in.txt")
    planets = get_planets(orbits)
    assert count_orbits(planets, orbits) == 42

    # part 2 validation
    orbits = get_input("ex_in_2.txt")
    planets = get_planets(orbits)
    assert find_distance(planets, orbits) == 4

    # part 1
    orbits = get_input("input.txt")
    planets = get_planets(orbits)
    print("found", count_orbits(planets, orbits), "orbits")


    # parts 2
    # find all roots of santa
    # keep going up until common root is found
    find_distance(planets, orbits)

