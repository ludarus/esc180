import numpy as np

# QUESTION 1. PRINT MATRIX
def print_matrix(M_lol: list[list[float]]) -> None:
    print(np.array(M_lol))


# QUESTION 2. LEADING INDEX
def get_lead_ind(row: list[float]) -> int:
    for i, n in enumerate(row):
        if n != 0:
            return i
    return len(row)


# QUESTION 3. ROW TO SWAP
def get_row_to_swap(M: list[list[float]], start_i: int) -> int:
    final_i = start_i
    pos = len(M[start_i])
    for i, row in enumerate(M[start_i:], start=start_i):
        lead = get_lead_ind(row)
        if lead < pos:
            pos = lead
            final_i = i
    return final_i


# QUESTION 4. ADD ROWS WITH COEFFICIENTS
def add_rows_coefs(
    r1: list[float], c1: float, r2: list[float], c2: float
) -> list[float]:
    c1r1 = [c1 * i for i in r1]
    c2r2 = [c2 * i for i in r2]
    return [i + j for i, j in zip(c1r1, c2r2)]


# QUESTION 5. ELIMINATE
def eliminate(M: list[list[float]], row_to_sub: int, best_lead_ind: int) -> None:
    row = M[row_to_sub]
    val = row[best_lead_ind]
    for i in range(row_to_sub + 1, len(M)):
        num = M[i][best_lead_ind]
        factor = -num / val
        M[i] = add_rows_coefs(M[i], 1, row, factor)
        # zero jic floating point error, unnecessary
        M[i][best_lead_ind] = 0.0


def eliminate_above(M: list[list[float]], row_to_sub: int, best_lead_ind: int) -> None:
    row = M[row_to_sub]
    val = row[best_lead_ind]
    for i in range(row_to_sub):
        num = M[i][best_lead_ind]
        factor = -num / val
        M[i] = add_rows_coefs(M[i], 1, row, factor)
        M[i][best_lead_ind] = 0.0


# QUESTION 6. FORWARD STEP
def forward_step(M: list[list[float]]) -> None:
    print("Starting the forward step:")
    print_matrix(M)
    for i in range(len(M)):
        swap = get_row_to_swap(M, i)
        if swap != i:
            print(f"Swapping rows {i} and {swap}:")
            M[i], M[swap] = M[swap], M[i]
            print_matrix(M)

        pivot_col = get_lead_ind(M[i])
        if pivot_col == len(M[i]):
            # The best remaining row is zero, so all remaining rows are zero.
            break

        print(f"Using row {i} to eliminate entries below it in column {pivot_col}:")
        eliminate(M, i, pivot_col)
        print_matrix(M)
    print("Done with the forward step.")


# QUESTION 7. BACKWARD STEP
def backward_step(M: list[list[float]]) -> None:
    print("Starting the backward step:")
    for i in range(len(M) - 1, -1, -1):
        pivot_col = get_lead_ind(M[i])
        if pivot_col == len(M[i]): # all zeros
            continue

        print(f"Using row {i} to eliminate entries above it in column {pivot_col}:")
        eliminate_above(M, i, pivot_col)
        print_matrix(M)

    print("Dividing each nonzero row by its leading coefficient:")
    for i, row in enumerate(M):
        pivot_col = get_lead_ind(row)
        if pivot_col != len(row):
            pivot = row[pivot_col]
            M[i] = [value / pivot for value in row]
    print_matrix(M)


# QUESTION 8. SOLVING A LINEAR SYSTEM
def solve(M: list[list[float]], b: list[float]) -> list[float]:
    # checks
    if len(M) != len(b):
        raise ValueError("M and b must have the same number of rows.")
    if not M:
        raise ValueError("M must have at least one row.")
    m = len(M[0])
    if any(len(row) != m for row in M):
        raise ValueError("All rows of M must have the same length.")

    Mb = [row + [value] for row, value in zip(M, b)]
    forward_step(Mb)

    # A pivot in the appended column means an equation thats like 0 = c - no sol
    pivot_cols = [get_lead_ind(row) for row in Mb]
    if m in pivot_cols:
        raise ValueError("The system has no solution.")
    # fewever pivots than varables (dont count b)
    if sum(col < m for col in pivot_cols) < m:
        raise ValueError("The system does not have a unique solution.")

    backward_step(Mb)
    return [row[-1] for row in Mb[:m]]


if __name__ == "__main__":
    M = np.array([[1, -2, 3], [3, 10, 1], [1, 5, 3]])
    x = np.array([75, 10, -11])
    b = np.matmul(M, x)
    x_found = solve(M.tolist(), b.tolist())
    print(x_found) # should recover [75, 10, -11]
