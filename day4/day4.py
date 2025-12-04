def day_04_v1(puzzle):
    part_1, part_2 = 0, 0

    grid = [[x for x in y] for y in puzzle]

    adjacent = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    len_x, len_y = len(grid[0]), len(grid)

    possible_positions = [(x, y) for x in range(len_x) for y in range(len_y)]

    for x, y in possible_positions:
        if grid[y][x] != "@":
            continue

        count = 0
        for dir in adjacent:
            nx = x + dir[0]
            ny = y + dir[1]

            if 0 <= nx < len_x and 0 <= ny < len_y and grid[ny][nx] == "@":
                count += 1

        part_1 += count < 4

    done = False
    while not done:
        done = True
        for x, y in possible_positions:
            if grid[y][x] != "@":
                continue

            count = 0
            for dir in adjacent:
                nx = x + dir[0]
                ny = y + dir[1]

                if 0 <= nx < len_x and 0 <= ny < len_y and grid[ny][nx] == "@":
                    count += 1

            if count < 4:
                grid[y][x] = "_"
                part_2 += 1
                done = False

    return part_1, part_2


if __name__ == "__main__":
    with open("AdventOfCode-2025/day4/day4_input.txt") as file:
        puzzle_in = [x.strip() for x in file.readlines()]

    basic = day_04_v1(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")
