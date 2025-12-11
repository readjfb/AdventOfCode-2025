import numpy as np
import itertools

import pyomo.environ as pyo

def lp_solve(toggles_matrix: np.ndarray, target: np.ndarray):
    n_buttons, n_dims = toggles_matrix.shape

    model = pyo.ConcreteModel()

    # param for buttons
    model.I = pyo.RangeSet(0, n_buttons - 1)
    # param for the number of dimensions/lights
    model.J = pyo.RangeSet(0, n_dims - 1)

    # Parameters
    matrix_data = {
        (i, j): int(toggles_matrix[i, j])
        for i in range(n_buttons)
        for j in range(n_dims)
    }
    target_data = {j: int(v) for j, v in enumerate(target)}

    model.A = pyo.Param(
        model.I, model.J, initialize=matrix_data, within=pyo.NonNegativeIntegers
    )
    model.b = pyo.Param(model.J, initialize=target_data, within=pyo.NonNegativeIntegers)

    model.x = pyo.Var(model.I, domain=pyo.NonNegativeIntegers)

    def sum_constraint_rule(m, j):
        return pyo.quicksum(m.A[i, j] * m.x[i] for i in m.I) == m.b[j]

    model.sum_constraints = pyo.Constraint(model.J, rule=sum_constraint_rule)

    model.obj = pyo.Objective(
        expr=pyo.quicksum(model.x[i] for i in model.I), sense=pyo.minimize
    )

    solver = pyo.SolverFactory("gurobi")
    # solver = pyo.SolverFactory("cplex_direct")
    result = solver.solve(model, tee=False)

    status = result.solver.status
    termination = result.solver.termination_condition

    if (status != pyo.SolverStatus.ok) or termination != "optimal":
        print(status, termination)
        return None

    x_sol = np.array([int(pyo.value(model.x[i]) + 0.5) for i in model.I], dtype=int)
    return x_sol, (status, termination)


def day10_v1(puzzle):
    part_1, part_2 = 0, 0

    puzzle = [x.split(" ") for x in puzzle]

    puzzle_rows = []
    for row in puzzle:
        row_info = {"lights": None, "buttons": [], "xors": [], "jolt": None}

        for i in row:
            if i[0] == "[":
                row_info["lights"] = np.array(
                    [True if x == "#" else False for x in i[1:-1]]
                )
            elif i[0] == "(":
                toggles = [int(x) for x in i[1:-1].split(",")]
                xor_map = np.array(
                    [k in toggles for k in range(len(row_info["lights"]))]
                )
                row_info["buttons"].append(toggles)
                row_info["xors"].append(xor_map)
            elif i[0] == "{":
                stripped = i[1:-1]
                row_info["jolt"] = np.array([int(x) for x in stripped.split(",")])

        puzzle_rows.append(row_info)

    for i, row_info in enumerate(puzzle_rows):
        toggle_matrix = np.array(row_info["xors"], dtype=int)
        lights = row_info["lights"]

        num_switches = len(row_info["xors"])

        solved = False

        for N in range(1, num_switches + 1):
            comb = np.array(
                list(itertools.combinations(np.arange(num_switches), N)), dtype=int
            )
            n_rows = comb.shape[0]

            possibilities = np.zeros((n_rows, num_switches), dtype=int)

            rows = np.arange(n_rows)[:, None]  # shape (n_rows, 1)
            possibilities[rows, comb] = 1

            for row in possibilities:
                if all(((row @ toggle_matrix) % 2) == lights):
                    part_1 += N
                    solved = True
                    break
            if solved:
                break

        # Part 2
        jolt = row_info["jolt"]
        sol, status = lp_solve(toggle_matrix, jolt)

        if not all(sol @ toggle_matrix == jolt):
            print(status)
            print("asdfsdf")
        try:
            part_2 += sum(sol)
        except:
            print("An Error Occured")
            pass

    return part_1, part_2


if __name__ == "__main__":
    with open("AdventOfCode-2025/day10/day10_input.txt") as file:
        # puzzle_in = file.read()
        # puzzle_in = [x for x in file.readlines()]
        puzzle_in = [x.strip() for x in file.readlines()]

    basic = day10_v1(puzzle_in)
    print(f"Part 1: {basic[0]}")
    print(f"Part 2: {basic[1]}")
