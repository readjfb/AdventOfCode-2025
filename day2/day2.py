import math


def check_invalid(s, n_splits=2):
    if len(s) % n_splits != 0:
        return False

    split_len = len(s) // n_splits

    first = s[:split_len]

    for i in range(n_splits):
        start = i * split_len
        end = (i + 1) * split_len

        if first != s[start:end]:
            return False

    return True


def day_02_v1(puzzle):
    part_1_solution = 0
    part_2_solution = 0

    ranges = "".join(puzzle).split(",")

    ranges = [r.split("-") for r in ranges if "-" in r]

    for lower, upper in ranges:
        for n in range(int(lower), int(upper) + 1):
            sn = str(n)

            if check_invalid(sn, n_splits=2):
                part_1_solution += n
                part_2_solution += n
                continue

            for lensplit in range(3, len(sn) + 1):
                if len(sn) % lensplit != 0:
                    continue

                if check_invalid(sn, n_splits=lensplit):
                    part_2_solution += n
                    break

    return (part_1_solution, part_2_solution)


def check_invalid_v2(n, len_n, split_len):
    if len_n % split_len != 0:
        return False

    if len_n == 2:
        return n % 11 == 0

    if len_n == 3:
        return n % 111 == 0

    divisor = 10**split_len

    first = n % divisor

    n //= divisor

    while n > 0:
        next_d = n % divisor

        if next_d != first:
            return False

        n //= divisor

    return True


def generate_divisor_list(len_max_upper_range):
    divisors = {}

    for n in range(len_max_upper_range + 1):
        divisors_list = []
        for divisor in range(n - 1, 0, -1):
            if n % divisor == 0:
                flag = True
                for d in divisors_list:
                    if d % divisor == 0:
                        flag = False
                        break
                if flag:
                    divisors_list.append(divisor)

        if (n % 2 == 0) and (n // 2) in divisors_list:
            divisors_list.remove(n // 2)

        divisors[n] = divisors_list
    return divisors


def day_02_v2(puzzle):
    part_1_solution = 0
    part_2_solution = 0

    ranges = "".join(puzzle).split(",")

    ranges = [r.split("-") for r in ranges if "-" in r]

    max_upper_range = max(ranges, key=lambda x: int(x[1]))[1]

    len_max_upper_range = len(str(max_upper_range))

    divisors = generate_divisor_list(len_max_upper_range)

    for lower, upper in ranges:
        lower = max(10, int(lower))
        upper = int(upper)

        len_lower = int(math.log10(lower) + 1)
        len_upper = int(math.log10(upper) + 1)

        for base_range in range(len_lower - 1, len_upper - 1 + 1):
            starting_val = max(lower, 10**base_range)
            ending_val = min(upper, 10 ** (base_range + 1))

            len_n = int(math.log10(starting_val) + 1)

            for n in range(starting_val, ending_val):
                if check_invalid_v2(n, len_n, split_len=len_n // 2):
                    if len_n % 2 == 0:
                        part_1_solution += n
                    part_2_solution += n
                    continue

                for split_len in divisors[len_n]:
                    if check_invalid_v2(n, len_n, split_len=split_len):
                        part_2_solution += n
                        continue

    return part_1_solution, part_2_solution


if __name__ == "__main__":
    with open("AdventOfCode-2025/day2/day2_input.txt") as file:
        puzzle_in = [x.strip() for x in file.readlines()]

    # basic = day_02_v1(puzzle_in)
    # print(f"Part 1: {basic[0]}")
    # print(f"Part 2: {basic[1]}")

    basic = day_02_v2(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")
