def get_max_index_v0(list_vals):
    return max(range(len(list_vals)), key=lambda i: list_vals[i])


def get_max_index(list_vals):
    return max(range(len(list_vals)), key=list_vals.__getitem__)


def day_03_v1(puzzle):
    part_1, part_2 = 0, 0

    puzzle = [[int(s) for s in row] for row in puzzle]

    for batteries in puzzle:
        max_index = get_max_index(batteries[:-1])
        second_index = get_max_index(batteries[max_index + 1 :]) + max_index + 1

        value = (10 * batteries[max_index]) + batteries[second_index]

        part_1 += value

    # Part 2
    for batteries in puzzle:
        final_value = 0
        current_index = 0
        for end_range in range(-12 + 1, 0 + 1):
            # learned something- if you do [:-0] in python, it actually returns nothing
            if end_range == 0:
                end_range = None

            index = get_max_index(batteries[current_index:end_range]) + current_index

            final_value += batteries[index]
            final_value *= 10

            current_index = index + 1

        final_value /= 10
        part_2 += int(final_value)

    return (part_1, part_2)


if __name__ == "__main__":
    with open("AdventOfCode-2025/day3/day3_input.txt") as file:
        puzzle_in = [x.strip() for x in file.readlines()]

    basic = day_03_v1(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")
