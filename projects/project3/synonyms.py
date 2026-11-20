'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math
from collections.abc import Callable, Mapping


def norm(vec: Mapping[str, float]) -> float:
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(
    vec1: Mapping[str, float], vec2: Mapping[str, float]
) -> float:
    pass


def build_semantic_descriptors(
    sentences: list[list[str]],
) -> dict[str, dict[str, int]]:
    pass


def build_semantic_descriptors_from_files(
    filenames: list[str],
) -> dict[str, dict[str, int]]:
    pass


def most_similar_word(
    word: str,
    choices: list[str],
    semantic_descriptors: dict[str, dict[str, int]],
    similarity_fn: Callable[[dict[str, int], dict[str, int]], float],
) -> str:
    pass


def run_similarity_test(
    filename: str,
    semantic_descriptors: dict[str, dict[str, int]],
    similarity_fn: Callable[[dict[str, int], dict[str, int]], float],
) -> float:
    pass
