"""Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
"""

import math


def norm(vec: dict[str, int]) -> float:
    """Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    """

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def dp(vec1: dict[str, int], vec2: dict[str, int]) -> int:
    res: int = 0
    for k in vec1.keys():
        if k in vec2:
            res += vec1[k] * vec2[k]
    return res


def cosine_similarity(vec1: dict[str, int], vec2: dict[str, int]) -> float:
    return dp(vec1, vec2) / (norm(vec1) * norm(vec2))


def build_semantic_descriptors(
    sentences: list[list[str]],
) -> dict[str, dict[str, int]]:
    outer = {}
    for s in sentences:
        s_set = set(s)
        for w in s_set:
            if w not in outer:
                outer[w] = {}
            inner = outer[w]
            for w_other in s_set:
                if w_other == w:
                    continue
                inner[w_other] = inner.get(w_other, 0) + 1
    return outer


def build_semantic_descriptors_from_files(
    filenames: list[str],
) -> dict[str, dict[str, int]]:
    sentences = []
    for n in filenames:
        f = open(n, "r", encoding="latin1")
        text = f.read()
        f.close()
        for punctuation in ",-:;":
            text = text.replace(punctuation, " ")
        file_sentences = text.lower().replace("!", ".").replace("?", ".").split(".")
        for s in file_sentences:
            words = s.split()
            if words:
                sentences.append(words)
    return build_semantic_descriptors(sentences)


def most_similar_word(
    word: str,
    choices: list[str],
    semantic_descriptors: dict[str, dict[str, int]],
    similarity_fn,
) -> str:
    best = (None, float("-inf"))
    word_vec = semantic_descriptors.get(word, None)
    for c in choices:
        c_vec = semantic_descriptors.get(c, None)
        if c_vec and word_vec:
            sim = similarity_fn(word_vec, c_vec)
        else:
            sim = -1
        if sim > best[1]:
            best = (c, sim)
    if best[0] == None:
        raise ValueError("best is None??")
    return best[0]


def run_similarity_test(
    filename: str,
    semantic_descriptors: dict[str, dict[str, int]],
    similarity_fn,
) -> float:
    res = 0
    f = open(filename)
    lines = f.read().split("\n")
    n = len(lines)
    for l in lines:
        if not l:  # newline at end
            n -= 1
            continue
        parts = l.split(" ")
        word = parts[0]
        correct = parts[1]
        choices = parts[2:]
        guess = most_similar_word(word, choices, semantic_descriptors, similarity_fn)
        if guess == correct:
            res += 1
    return (res / n) * 100
