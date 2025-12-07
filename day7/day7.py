from collections import defaultdict, deque

def day_07_v1(puzzle):
    part_1, part_2 = 0, 0

    starting_index = puzzle[0].index("S")

    stack = deque([(starting_index, 1)])
    processed = set((starting_index, 1))

    num_ways = defaultdict(int)
    num_ways[(starting_index, 1)] = 1

    len_x, len_y = len(puzzle[0]), len(puzzle)

    while stack:
        curr_x, curr_y = stack.popleft()

        if not (0<=curr_x < len_x and 0<=curr_y<len_y-1):
            continue

        num_ways_at_spot = num_ways[(curr_x, curr_y)]

        # Try moving downward
        if puzzle[curr_y+1][curr_x] == '.':
            if (curr_x, curr_y+1) not in processed:
                stack.append((curr_x, curr_y+1))
                processed.add((curr_x, curr_y+1))
            num_ways[(curr_x, curr_y+1)] += num_ways_at_spot
            continue

        if puzzle[curr_y+1][curr_x] == '^':
            part_1 += 1

            num_ways[(curr_x+1, curr_y+1)] += num_ways_at_spot
            if (curr_x+1, curr_y+1) not in processed:
                stack.append((curr_x+1, curr_y+1))
                processed.add((curr_x+1, curr_y+1))

            num_ways[(curr_x-1, curr_y+1)] += num_ways_at_spot
            if (curr_x-1, curr_y+1) not in processed:
                stack.append((curr_x-1, curr_y+1))
                processed.add((curr_x-1, curr_y+1))
            continue
        print("Unreachable State Reached")

    for i in range(len_x):
        part_2 += num_ways[(i, len_y - 1)]

    return part_1, part_2


if __name__ == "__main__":
    with open("AdventOfCode-2025/day7/day7_input.txt") as file:
        # puzzle_in = file.read()
        # puzzle_in = [x for x in file.readlines()]
        puzzle_in = [x.strip() for x in file.readlines()]

    basic = day_07_v1(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")
