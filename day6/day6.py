def day_06_v1(puzzle):
    part_1, part_2 = 0, 0
    rows = [x.strip().split(" ") for x in puzzle]
    rows = [[x.strip() for x in row if x] for row in rows]

    for i in range(len(rows[0])):
        ops = [int(rows[k][i]) for k in range(len(rows) - 1)]
        operator = rows[-1][i]

        if operator == "*":
            new_num = 1
            for k in ops:
                new_num *= k
            part_1 += new_num
        elif operator == "+":
            part_1 += sum(ops)

    # Part 2
    # Format pad out with spaces, and reverse
    rows = [x.strip("\n") for x in puzzle]
    max_len = max([len(r) for r in rows])
    rows = [r.ljust(max_len, " ") for r in rows]
    rows = [x[::-1] for x in rows]

    nums = []
    i, len_rows_0 = 0, len(rows[0])
    while i < len_rows_0:
        operator = rows[-1][i]

        num = ""
        for n in range(len(rows) - 1):
            num += rows[n][i]
        nums.append(int(num))

        if operator == " ":
            i += 1
            continue

        if operator == "*":
            new_num = 1
            for k in nums:
                new_num *= k
            part_2 += new_num
        elif operator == "+":
            part_2 += sum(nums)

        nums = []
        i += 2

    return part_1, part_2


if __name__ == "__main__":
    with open("AdventOfCode-2025/day6/day6_input.txt") as file:
        # puzzle_in = file.read()
        puzzle_in = [x for x in file.readlines()]
        # puzzle_in = [x.strip() for x in file.readlines()]

    basic = day_06_v1(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")
