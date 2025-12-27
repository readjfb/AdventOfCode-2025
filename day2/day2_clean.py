import math


def check_invalid_v2(n, len_n, split_len):
    if len_n % split_len:
        return False

    divisor = 10**split_len
    n, first = divmod(n, divisor)
    while n:
        n, chunk = divmod(n, divisor)
        if chunk != first:
            return False
    return True


def generate_split_lens_list(len_max_upper_range):
    """
    Builds, for each possible digit length n, a
    pruned list of divisors of n that can be used as candidate split sizes for
    repeating-digit blocks. It iterates over all proper divisors of n,
    keeping only those that are not redundant (i.e., not factors of
    larger divisors). Also ignores values of n//2, since that's checked in part 1

    For upper range 10, returns
    {0: [], 1: [], 2: [], 3: [1], 4: [], 5: [1], 6: [2], 7: [1], 8: [], 9: [3], 10: [2]}
    """
    divisors = {}

    for n in range(len_max_upper_range + 1):
        divisors_list = []

        for divisor in range(n - 1, 0, -1):
            if n % divisor == 0:
                for d in divisors_list:
                    if d % divisor == 0:
                        break
                else:
                    divisors_list.append(divisor)

        if (n % 2 == 0) and (n // 2) in divisors_list:
            divisors_list.remove(n // 2)

        divisors[n] = divisors_list
    return divisors


def fast_len_n(n):
    return int(math.log10(n) + 1)


def day_02_v3(puzzle):
    part_1_solution = 0
    part_2_solution = 0

    ranges = "".join(puzzle).split(",")
    ranges = [r.split("-") for r in ranges if "-" in r]

    max_upper_range = max(ranges, key=lambda x: int(x[1]))[1]
    len_max_upper_range = len(str(max_upper_range))
    split_lens = generate_split_lens_list(len_max_upper_range)

    def find_count_in_range(starting_val, ending_val):
        p1_s, p2_s = 0, 0

        len_n = fast_len_n(starting_val)

        match len_n:
            case 2:
                n = 11
            case 3:
                n = 111
            case 5:
                n = 11_111
            case 7:
                n = 1_111_111
            case _:
                n = None

        if n:
            inc = n
            while n < ending_val:
                if starting_val <= n:
                    p2_s += n
                n += inc
            if len_n % 2 == 0:
                p1_s += p2_s
            return p1_s, p2_s

        for n in range(starting_val, ending_val):
            if check_invalid_v2(n, len_n, split_len=len_n // 2):
                if len_n % 2 == 0:
                    p1_s += n
                p2_s += n
                continue

            for split_len in split_lens[len_n]:
                if check_invalid_v2(n, len_n, split_len=split_len):
                    p2_s += n

        return p1_s, p2_s

    for lower, upper in ranges:
        # We don't need to check values < 10, since they can't repeat
        lower = max(10, int(lower))
        upper = int(upper)

        # A marginally faster way of computing len(n)
        len_lower, len_upper = fast_len_n(lower), fast_len_n(upper)

        # This loop allows checking 2 digit numbers, then 3 digit numbers
        # Avoids recomputing len(n), which is surprisingly expensive
        # Start the range lower than the lower len, since len(50) = 2,
        # but 10^2 = 100
        for candidate_len in range(len_lower - 1, len_upper):
            starting_val = max(lower, 10**candidate_len)
            ending_val = min(upper, 10 ** (candidate_len + 1))

            p1_s, p2_s = find_count_in_range(starting_val, ending_val)
            part_1_solution += p1_s
            part_2_solution += p2_s

    return part_1_solution, part_2_solution


if __name__ == "__main__":
    with open("AdventOfCode-2025/day2/day2_input.txt") as file:
        puzzle_in = [x.strip() for x in file.readlines()]

    basic = day_02_v3(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")
