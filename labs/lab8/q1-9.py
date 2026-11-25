# ESC180 Lab 8: Recursion
# Full questions and examples: Lab 8 Handout.pdf
# For each recursive function, find the base case and the recursive step first.
# Implement and test one function at a time.

# QUESTION 1. MULTIPLICATION WITHOUT *
# Part A: Write down the base case and the recursive step for a times b.
# Part C: Write down the call tree for times(2, 3).
# Part D: Write down the worst-case runtime complexity in Big O notation.

# Part B: Return a * b recursively, using only addition. b is a nonnegative
# integer. Do not use loops, the * operator, or the math module.
def times(a, b):
    raise NotImplementedError


# QUESTION 2. SUM OF DIGITS
# Return the sum of the digits of the nonnegative integer n, recursively.
# Example: digit_sum(123) returns 6.
def digit_sum(n):
    raise NotImplementedError


# QUESTION 3. REMAINDER WITHOUT %, //, *, /
# Return a % b for positive integers a and b. Do not use loops, the %, //, *,
# or / operators, or the math module.
def remainder(a, b):
    raise NotImplementedError


# QUESTION 4. LINEAR SEARCH
# Return the index of e in L, recursively. Do not use loops or L.index().
# len() and slicing are allowed. Example: linear_search([5, 8, 2, 9], 2) returns 2.
def linear_search(L, e):
    raise NotImplementedError


# QUESTION 5. INTERLEAVE
# L1 and L2 have the same length. Return [L1[0], L2[0], L1[1], L2[1], ...].
# Do not use loops.
# Example: interleave([1, 2, 3], ["a", "b", "c"]) returns [1, "a", 2, "b", 3, "c"].
def interleave(L1, L2):
    raise NotImplementedError


# QUESTION 6. REVERSING A LIST IN PLACE
# Reverse L in place. Do not use loops or slicing. Return nothing.
# Hint: Write a helper function that calls itself. See the handout.
def reverse_rec(L):
    raise NotImplementedError


# QUESTION 7. PRINTING FROM THE MIDDLE
# len(L) is odd. Print L[n//2] L[n//2-1] L[n//2+1] ... L[0] L[n-1].
# Do not use loops, and do not print a list. Print only single elements.
# Example: for [0, 1, 2, 3, 4, 5, 6], print 3 2 4 1 5 0 6.
# The handout does not give a function name. This name is a placeholder.
def zigzag1(L):
    # Hint from the handout: prints L[0] L[n-1] L[1] L[n-2] ... L[n//2].
    if len(L) == 0:
        print()
    elif len(L) == 1:
        print(L[0])
    else:
        print(L[0], L[-1], end=" ")
        zigzag1(L[1:-1])


def print_from_middle(L):
    raise NotImplementedError


# QUESTION 8. RECURSION PRACTICE WITH LLMS
# Get three recursion problems from an LLM (see the handout for the prompt).
# Solve at least two yourself, test them on the LLM's test cases, and discuss
# the handout questions with a TA. Put your solutions below.


# QUESTION 9. SPLITTING A LIST
# Loops are allowed. Split L into sublists separated by any element of seps.
# Example: split_list([1, 2, 6, 4, 5, 3, 7], [3, 6]) returns [[1, 2], [4, 5], [7]].
# Hint: First write a helper that splits by one separator. See the handout.
def split_list(L, seps):
    raise NotImplementedError


if __name__ == "__main__":
    # Add tests here as you implement each question.
    pass
