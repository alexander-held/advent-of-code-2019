import fileinput
from math import atan2, inf, pi

x = [line.strip() for line in fileinput.input()]
asteroids = []
for py, line in enumerate(x):
    asteroids += [(px, py) for px, char in enumerate(line) if char == "#"]


def get_angles(location, asteroids):
    all_angles = []
    for target in asteroids:
        if location == target:
            continue  # skip angle from location to itself (location is in asteroids)
        # calculate angles to y axis, increasing clockwise, from location to each target
        angle = atan2(target[0] - location[0], -target[1] + location[1])
        if angle < 0:
            angle += 2 * pi
        all_angles.append(angle)
    return all_angles


def location_and_num_visible(asteroids):
    num_vis_max = 0
    for station in asteroids:
        all_angles = get_angles(station, asteroids)
        num_vis = len(set(all_angles))  # unique angles => number of visible stations
        if num_vis > num_vis_max:
            best_spot = station
            num_vis_max = num_vis
    return best_spot, num_vis_max


def get_vaporized_order(station, asteroids):
    all_angles = get_angles(station, asteroids)
    asteroids.remove(station)  # remove station position, only keep potential targets

    targets = []
    while len(asteroids):
        for cur_angle in sorted(set(all_angles)):
            # get all asteroids in a line of sight (same angle to station)
            asteroids_in_los = [
                asteroids[i]
                for i, ast_angle in enumerate(all_angles)
                if ast_angle == cur_angle
            ]

            # find closest asteroid in this line of sight
            dist_min_sq = inf
            for ast in asteroids_in_los:
                dist_sq = (ast[0] - station[0]) ** 2 + (ast[1] - station[1]) ** 2
                if dist_sq < dist_min_sq:
                    closest = ast
                    dist_min_sq = dist_sq
            targets.append(closest)
            all_angles.pop(asteroids.index(closest))
            asteroids.pop(asteroids.index(closest))

    return targets


best_spot, num_vis_max = location_and_num_visible(asteroids)
print(f"part 1: {num_vis_max}")

target_order = get_vaporized_order(best_spot, asteroids)
print(f"part 2: {target_order[199][0] * 100 + target_order[199][1]}")
