def day_01_v1(puzzle):
    D = 50

    part_1_found = 0
    part_2_found = 0

    for k in puzzle:
        direction = k[0]

        dist = int(k[1:])

        for _ in range(dist):
            if direction == "L":
                D = (D - 1) % 100
            elif direction == "R":
                D = (D + 1) % 100

            if D == 0:
                part_2_found += 1

        if D == 0:
            part_1_found += 1

    return (part_1_found, part_2_found)


def day_01_v2(puzzle):
    D = 50

    part_1_found, part_2_found = 0, 0

    for k in puzzle:
        direction, dist = k[0], int(k[1:])

        positivity = 1
        if direction == "L":
            positivity = -1

        while dist != 0:
            step_size = min(99, dist)
            dist -= step_size

            offset = D + (positivity * step_size)

            rounded_offset = offset % 100

            if (D != 0) and ((offset == 0) or (offset != rounded_offset)):
                part_2_found += 1

            D = rounded_offset

        part_1_found += D == 0

    return part_1_found, part_2_found


if __name__ == "__main__":
    with open("AdventOfCode-2025/day1/day1_input.txt") as file:
        puzzle_in = [x.strip() for x in file.readlines()]

    # basic = day_01_v1(puzzle_in)
    # print(f"Part 1: {basic[0]}")
    # print(f"Part 2: {basic[1]}")

    basic = day_01_v2(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")

    # n_runs = 100
    # time_taken_v1 = timeit.timeit(lambda: day_01_v1(puzzle_in), number=n_runs)
    # time_taken_v1 = time_taken_v1 / n_runs
    # print(time_taken_v1)

    # time_taken_v2 = timeit.timeit(lambda: day_01_v2(puzzle_in), number=n_runs)
    # time_taken_v2 = time_taken_v2 / n_runs
    # print(time_taken_v2)

    # cProfile.run(
    #     "timeit.timeit(lambda: day_01_v2(puzzle_in), number=n_runs)",
    #     filename="day1.profile",
    #     sort="cumtime",
    # )
