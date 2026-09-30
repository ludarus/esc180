def leibniz_pi_over_4(iterations: int) -> float:
    res: float = 0
    for i in range(iterations + 1):
        numerator: int = (-1) ** i
        denominator: int = 2 * i + 1
        res += numerator/denominator
    return res

def leibniz_pi_over_4_while(iterations: int) -> float:
    res: float = 0
    i = 0
    while i <= iterations:
        numerator: int = (-1) ** i
        denominator: int = 2 * i + 1
        res += numerator/denominator
        i += 1
    return res

print(leibniz_pi_over_4(1000) * 4)
print(leibniz_pi_over_4_while(1000) * 4)


