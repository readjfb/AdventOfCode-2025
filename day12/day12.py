def day12_v1(puzzle):
    part_1, part_2 = 0, 0
    parts = puzzle.split("\n\n")

    blocks = parts[:-1]

    blocks_dict = {}

    for block in blocks:
        rows = block.split("\n")
        row = rows[0].strip(':')

        blocks_dict[row] = rows[1:]

    area_dict = {}

    for i, v in blocks_dict.items():
        area_dict[i] = "".join(v).count("#")

    spaces = parts[-1]
    spaces = [x.strip() for x in spaces.split("\n")]

    for part in spaces:
        total_area, counts = part.split(': ')
        total_area = [int(x) for x in total_area.split("x")]
        total_area = total_area[0] * total_area[1]

        counts = [area_dict[str(i)]*int(k) for i,k in enumerate(counts.split(" "))]
        total_shape_area = sum(counts)

        if total_area >= total_shape_area:
            part_1 += 1

    return part_1, part_2

if __name__ == "__main__":
    with open("AdventOfCode-2025/day12/day12_input.txt") as file:
        puzzle_in = file.read()
        # puzzle_in = [x for x in file.readlines()]
        # puzzle_in = [x.strip() for x in file.readlines()]

    basic = day12_v1(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")

