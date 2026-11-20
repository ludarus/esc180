from collections import defaultdict


def get_word_counts(f: str):
    text = open(f).read()
    word_list = text.split()
    word_counts = defaultdict(int)
    for w in word_list:
        word_counts[w] += 1
    return word_counts

# not useful
def top10(L: list[int]): #o(n)
    top = []
    for _ in range(10):
        maxx = max(L)
        top.append(maxx)
        L.remove(maxx)
    return top


def top10_pairs(pairs: list[tuple[str, int]]) -> list[tuple[str, int]]:
    remaining = pairs.copy()
    top = []
    for _ in range(min(10, len(remaining))):
        best = max(remaining, key=lambda pair: pair[1])
        top.append(best)
        remaining.remove(best)
    return top


word_counts = get_word_counts("book.txt")
pairs = list(word_counts.items())
print(top10_pairs(pairs))




# you search wikipedia by doing https://en.wikipedia.org/w/index.php?search=[edit me]
#
#

import urllib.request
from urllib.parse import quote_plus
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def num_of_results(term: str) -> int:
    link = f"https://en.wikipedia.org/w/index.php?search={quote_plus(term)}&fulltext=1"
    req = urllib.request.Request(link, headers={"User-Agent":
"ESC180-Lab7/1.0 (University of Toronto course lab)"})
    f = urllib.request.urlopen(req)
    page: str = f.read().decode("utf-8")
    f.close()
    marker = 'data-mw-num-results-total="'
    marker_start = page.find(marker)
    if marker_start == -1:
        raise ValueError("Could not find the search result count")

    start = marker_start + len(marker)
    end = page.find('"', start)
    if end == -1:
        raise ValueError("Could not find the closing quote for the result count")

    return int(page[start:end])

print(num_of_results("dogs"))

def choose_variant(variants: list[str]) -> list[str]:
    best: list[tuple[str, int]] = []
    for variant in variants:
        n = num_of_results(variant)
        if not best or n > best[0][1]:
            best = [(variant, n)]
        elif n == best[0][1]:
            best.append((variant, n))
    return [b[0] for b in best]

print(choose_variant(["dogs", "cats"]))


