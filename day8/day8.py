import numpy as np
from scipy.sparse.csgraph import connected_components


def day_08_v1(puzzle):
    part_1, part_2 = 0, 0
    coordinates = [[int(y) for y in x.split(",")] for x in puzzle]
    distances_matrix = np.array(
        [
            np.linalg.norm(
                (item * np.ones((len(coordinates), len(item)))) - coordinates, axis=1
            )
            for item in coordinates
        ]
    )

    np.fill_diagonal(distances_matrix, np.inf)
    blank_distances_mat = distances_matrix.copy()

    distances_matrix = np.triu(distances_matrix)

    distances_matrix[distances_matrix == 0] = np.inf

    adj_mat = np.zeros(distances_matrix.shape)

    for _ in range(1000):
        min_index = np.unravel_index(
            np.argmin(distances_matrix, keepdims=True), shape=distances_matrix.shape
        )
        adj_mat[min_index] = 1

        distances_matrix[min_index] = np.inf

    _, labels = connected_components(
        csgraph=adj_mat, directed=False, return_labels=True
    )

    _, counts = np.unique(labels, return_counts=True)

    counts = sorted(counts, reverse=True)[:3]

    part_1 = np.multiply.reduce(counts)

    # Part 2

    # Which row has the highest minimum element?
    min_elements = np.min(blank_distances_mat, axis=0)
    max_element_of_mins = np.argmax(min_elements)
    row_of_meom = blank_distances_mat[max_element_of_mins, :]

    min_element_of_meom = np.argmin(row_of_meom)

    x1 = coordinates[max_element_of_mins][0]
    x2 = coordinates[min_element_of_meom][0]

    part_2 = x1 * x2
    return part_1, part_2


def day_08_v2(puzzle):
    part_1, part_2 = 0, 0
    coords = np.array([[int(y) for y in x.split(",")] for x in puzzle], dtype=float)

    diffs = coords[:, None, :] - coords[None, :, :]
    distances_matrix = np.einsum("ijk,ijk->ij", diffs, diffs)

    np.fill_diagonal(distances_matrix, np.inf)

    pt_1_dist_mat = np.triu(distances_matrix)
    pt_1_dist_mat[pt_1_dist_mat == 0] = np.inf

    adj_mat = np.zeros(pt_1_dist_mat.shape)

    full_ranking = np.unravel_index(
        np.argpartition(pt_1_dist_mat, 1000, axis=None)[:1000],
        shape=pt_1_dist_mat.shape,
    )

    adj_mat[full_ranking] = 1

    _, labels = connected_components(
        csgraph=adj_mat, directed=False, return_labels=True
    )
    _, counts = np.unique(labels, return_counts=True)

    part_1 = np.multiply.reduce(np.partition(counts, -3)[-3:])

    # Part 2

    # Which row has the highest minimum element, and in that row, which is it's lowest column?
    farthest_nearest_index = np.argmax(np.min(distances_matrix, axis=0))
    nearest_in_farthest = np.argmin(distances_matrix[farthest_nearest_index, :])

    x1 = coords[farthest_nearest_index][0]
    x2 = coords[nearest_in_farthest][0]

    part_2 = x1 * x2
    return int(part_1), int(part_2)


if __name__ == "__main__":
    with open("AdventOfCode-2025/day8/day8_input.txt") as file:
        # puzzle_in = file.read()
        # puzzle_in = [x for x in file.readlines()]
        puzzle_in = [x.strip() for x in file.readlines()]

    basic = day_08_v2(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")
