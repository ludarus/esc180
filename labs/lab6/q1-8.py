# ESC180 Lab 6: Gaussian elimination
# Full questions and examples: Lab 6 Handout.pdf
# Step-by-step examples: Lab 6 Sample Run.pdf

# QUESTION 1. PRINT MATRIX
# Print the nested list M_lol as a matrix. See use_numpy.py, lines 1–11.
def print_matrix(M_lol):
    raise NotImplementedError


# QUESTION 2. LEADING INDEX
# Return the index of the first nonzero element, or len(row) for a zero row.
def get_lead_ind(row):
    raise NotImplementedError


# QUESTION 3. ROW TO SWAP
# Among rows at or below start_i, return the index of the row whose leading
# nonzero element is furthest left. See the handout for an example.
def get_row_to_swap(M, start_i):
    raise NotImplementedError


# QUESTION 4. ADD ROWS WITH COEFFICIENTS
# Return a new row containing c1*r1 + c2*r2; r1 and r2 have equal lengths.
def add_rows_coefs(r1, c1, r2, c2):
    raise NotImplementedError


# QUESTION 5. ELIMINATE
# Modify M to eliminate the coefficient at best_lead_ind from rows below
# row_to_sub. See the handout for the input and resulting matrix.
def eliminate(M, row_to_sub, best_lead_ind):
    raise NotImplementedError


# QUESTION 6. FORWARD STEP
# Modify M using the forward step of Gaussian elimination. Print the matrix
# transformation and explain each step, as in sample run Example 1.
def forward_step(M):
    raise NotImplementedError


# QUESTION 7. BACKWARD STEP
# Apply the backward step of Gaussian elimination to M. See sample run Example 2.
def backward_step(M):
    raise NotImplementedError


# QUESTION 8. SOLVING A LINEAR SYSTEM
# Solve Mx = b by building the augmented matrix, applying Gaussian elimination,
# and solving for x. Test using the matrix multiplication example in use_numpy.py.
def solve(M, b):
    raise NotImplementedError


if __name__ == "__main__":
    # Add tests here as you implement each question.
    pass
