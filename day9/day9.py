import numpy as np


def day_09_v1(puzzle):
    from shapely.geometry import Polygon

    part_1, part_2 = 0, 0

    coords = [x.split(",") for x in puzzle]
    coords = np.array([[int(y) for y in x] for x in coords])

    diffs = np.abs(coords[:, None, :] - coords[None, :, :]) + 1
    sizes = diffs[:, :, 0] * diffs[:, :, 1]

    part_1 = np.max(sizes)

    sizes = np.triu(sizes, 0)

    # Go through each max; see if any points are inside the box
    indices = np.unravel_index(np.argsort(sizes, axis=None)[::-1], shape=sizes.shape)

    main_polygon = Polygon(shell=coords)

    for ind_a, ind_b in zip(*indices):
        x1, y1 = coords[ind_a]
        x2, y2 = coords[ind_b]

        x_min, x_max = (x1, x2) if x1 < x2 else (x2, x1)
        y_min, y_max = (y1, y2) if y1 < y2 else (y2, y1)

        if x_min == x_max or y_min == y_max:
            continue

        inside_mask = (
            (coords[:, 0] > x_min)
            & (coords[:, 0] < x_max)
            & (coords[:, 1] > y_min)
            & (coords[:, 1] < y_max)
        )
        if inside_mask.any():
            continue

        rectangle_corners = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]

        rectangle = Polygon(rectangle_corners)

        if rectangle.within(main_polygon):
            print(tuple(coords[ind_a]), tuple(coords[ind_b]))
            part_2 = sizes[ind_a, ind_b]
            break

    return part_1, part_2


if __name__ == "__main__":
    with open("AdventOfCode-2025/day9/day9_input.txt") as file:
        # puzzle_in = file.read()
        # puzzle_in = [x for x in file.readlines()]
        puzzle_in = [x.strip() for x in file.readlines()]

    basic = day_09_v1(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")
