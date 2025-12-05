def day_05_v1(puzzle):
    part_1, part_2 = 0, 0

    parts = puzzle.split("\n\n")

    ranges = parts[0].split("\n")
    ingredients = parts[1].split("\n")

    ranges = [x.split('-') for x in ranges]
    ranges = [(int(x[0]), int(x[1])) for x in ranges]
    ingredients = [int(x) for x in ingredients]

    for ing in ingredients:
        for r in ranges:
            if r[0] <= ing <= r[1]:
                part_1 += 1
                break

    # Part 2
    ranges_sorted = sorted(ranges, key=lambda x: x[0])

    range_bottom = -float('inf')
    while ranges_sorted:
        bot, top = ranges_sorted.pop(0)

        if range_bottom >= bot:
            bot = range_bottom + 1

        if top < bot:
            continue

        part_2 += (top - bot) + 1

        range_bottom = max(bot, top, range_bottom)

    return part_1, part_2


if __name__ == "__main__":
    with open("AdventOfCode-2025/day5/day5_input.txt") as file:
        puzzle_in = file.read()
        # puzzle_in = [x.strip() for x in file.readlines()]

    basic = day_05_v1(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")
