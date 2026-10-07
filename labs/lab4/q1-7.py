import math

def count_evens(L: list[int]) -> int:
    count = 0
    for num in L:
        if num % 2 == 0:
            count += 1
    return count

def list_to_str(L: list[object]) -> str:
    if not L: return "[]"
    res = "["
    for item in L:
            res += f"{str(item)}, "
    res = res[:-2]
    res += "]"
    return res

def lists_are_the_same(l1: list[object], l2: list[object]) -> bool:
    if len(l1) != len(l2):
        return False
    n = len(l1)
    for i in range(n):
        if l1[i] == l2[i]:
            continue
        return False
    return True

def input_loop() -> None:
    names = ""
    while True:
        print("Enter a name:")
        name = input()
        if name == "END":
            break
        names += f"{name}, "
    print("The names are: " + names[:-2])

def gcd(n: int, m: int):
    up_to = min(n, m)
    biggest_gcd = 0
    for i in range(1, up_to + 1):
        rem_n = n % i
        rem_m = m % i
        if rem_n == 0 and rem_m == 0:
            biggest_gcd = i
    return biggest_gcd

def efficient_gcd(n: int, m: int):
    up_to = min(n, m)
    for i in range(up_to, 0, -1):
        rem_n = n % i
        rem_m = m % i
        if rem_n == 0 and rem_m == 0:
            return i

def liebniz_pi_iterations(n: int) -> int:
    scale: int = 10 ** (n-1)
    match: int = int(math.pi * scale)
    sum = 0
    k = 0
    while match != int(4 * sum * scale):
        num: int = (-1) ** k
        den: int = 2 * k + 1
        sum += num/den
        k += 1
    return k

if __name__ == "__main__":
    assert count_evens([1, 2, 3, 4]) == 2
    assert count_evens([-2, 0, 3]) == 2
    assert count_evens([]) == 0

    assert list_to_str([1, 2, 3]) == "[1, 2, 3]"
    assert list_to_str([42]) == "[42]"
    assert list_to_str([]) == "[]"

    assert lists_are_the_same([1, 2], [1, 2])
    assert not lists_are_the_same([1, 2], [2, 1])
    assert not lists_are_the_same([1], [1, 2])
    assert lists_are_the_same([], [])

    assert gcd(12, 18) == 6
    assert gcd(7, 11) == 1
    assert gcd(8, 8) == 8
    assert efficient_gcd(12, 18) == 6
    assert efficient_gcd(7, 11) == 1
    assert efficient_gcd(8, 8) == 8

    assert liebniz_pi_iterations(1) == 3
    assert liebniz_pi_iterations(2) == 19
    assert liebniz_pi_iterations(3) == 119

    print("All tests passed!")

    # Manual input_loop tests: enter Alice, Bob, END; then try END immediately.
    # input_loop()
