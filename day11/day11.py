from scipy import sparse
import numpy as np


def day11_v1(puzzle):
    part_1, part_2 = 0, 0

    connections = {}

    for row in puzzle:
        first, second = row.split(":")
        connections[first] = second.strip().split(" ")

    all_nodes = list(connections.keys()) + ["out"]

    adjacency_mat = np.zeros((len(all_nodes), len(all_nodes)))

    element_to_index = {v: i for i, v in enumerate(all_nodes)}

    for key, row in connections.items():
        key_index = element_to_index[key]
        row_inds = [element_to_index[x] for x in row]
        adjacency_mat[key_index, row_inds] = 1

    # Find the number of ways to get from
    summed_matrix = np.zeros(adjacency_mat.shape)

    matrix_to_power = adjacency_mat
    i = 0
    while matrix_to_power.any(axis=None) and i < len(all_nodes):
        summed_matrix += matrix_to_power
        matrix_to_power = matrix_to_power @ adjacency_mat
        i += 1

    you = element_to_index["you"]
    svr = element_to_index["svr"]
    fft = element_to_index["fft"]
    dac = element_to_index["dac"]
    out = element_to_index["out"]

    part_1 = summed_matrix[you, out]

    # svr --> dac --> fft --> out
    # svr --> fft --> dac --> out
    part_2 = summed_matrix[svr, dac] * summed_matrix[dac, fft] * summed_matrix[fft, out]
    part_2 += (
        summed_matrix[svr, fft] * summed_matrix[fft, dac] * summed_matrix[dac, out]
    )

    return int(part_1), int(part_2)


def day11_v2(puzzle):
    connections = {}
    for row in puzzle:
        first, second = row.split(":")
        connections[first] = second.strip().split(" ")

    all_nodes = list(connections.keys()) + ["out"]
    element_to_index = {v: i for i, v in enumerate(all_nodes)}

    data, rows, cols = [], [], []
    for key, row in connections.items():
        key_index = element_to_index[key]
        for x in row:
            rows.append(key_index)
            cols.append(element_to_index[x])
            data.append(1)

    coo_adj_mat = sparse.coo_matrix(
        (data, (rows, cols)), shape=(len(all_nodes), len(all_nodes))
    )
    adjacency_mat = coo_adj_mat.tocsr()

    # Find the number of ways to get from
    summed_matrix = sparse.csr_matrix(adjacency_mat.shape)

    matrix_to_power = adjacency_mat
    i = 0
    while matrix_to_power.nnz > 0 and i < len(all_nodes):
        summed_matrix += matrix_to_power
        matrix_to_power = matrix_to_power @ adjacency_mat
        i += 1

    you = element_to_index["you"]
    svr = element_to_index["svr"]
    fft = element_to_index["fft"]
    dac = element_to_index["dac"]
    out = element_to_index["out"]

    # you --> out
    part_1 = summed_matrix[you, out]

    # svr --> dac --> fft --> out
    # svr --> fft --> dac --> out
    part_2 = summed_matrix[svr, dac] * summed_matrix[dac, fft] * summed_matrix[fft, out]
    part_2 += (
        summed_matrix[svr, fft] * summed_matrix[fft, dac] * summed_matrix[dac, out]
    )

    return int(part_1), int(part_2)


def day11_v3(puzzle):
    connections = {}
    for row in puzzle:
        first, second = row.split(":")
        connections[first] = second.strip().split(" ")

    all_nodes = list(connections.keys()) + ["out"]
    element_to_index = {v: i for i, v in enumerate(all_nodes)}
    N = len(all_nodes)

    data, rows, cols = [], [], []
    for key, row in connections.items():
        key_index = element_to_index[key]
        for x in row:
            rows.append(key_index)
            cols.append(element_to_index[x])
            data.append(1)

    coo_adj_mat = sparse.coo_matrix((data, (rows, cols)), shape=(N, N))
    adjacency_mat = coo_adj_mat.tocsr()

    you = element_to_index["you"]
    svr = element_to_index["svr"]
    fft = element_to_index["fft"]
    dac = element_to_index["dac"]
    out = element_to_index["out"]

    def summed_paths_from(adj_mat, start, max_len):
        n = adj_mat.shape[0]
        v = np.zeros(n)
        v[start] = 1

        total = np.zeros(n)

        # matrix*vector is faster than vector * matrix
        adj_mat_t = adj_mat.T
        for _ in range(max_len):
            v = adj_mat_t * v
            if not v.any():
                break
            total += v

        return total

    paths_you = summed_paths_from(adjacency_mat, you, N)
    paths_svr = summed_paths_from(adjacency_mat, svr, N)
    paths_fft = summed_paths_from(adjacency_mat, fft, N)
    paths_dac = summed_paths_from(adjacency_mat, dac, N)

    # you --> out
    part_1 = paths_you[out]

    # svr --> dac --> fft --> out
    # svr --> fft --> dac --> out
    part_2 = paths_svr[dac] * paths_dac[fft] * paths_fft[out]
    part_2 += paths_svr[fft] * paths_fft[dac] * paths_dac[out]

    return int(part_1), int(part_2)


if __name__ == "__main__":
    with open("AdventOfCode-2025/day11/day11_input.txt") as file:
        # puzzle_in = file.read()
        # puzzle_in = [x for x in file.readlines()]
        puzzle_in = [x.strip() for x in file.readlines()]

    basic = day11_v3(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")
