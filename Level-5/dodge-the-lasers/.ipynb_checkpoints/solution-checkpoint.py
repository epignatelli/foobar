from decimal import Decimal, getcontext

getcontext().prec = 100
sqrt2 = Decimal(2).sqrt()

def beatty_sqrt2(n):
    n_1 = long((sqrt2 - 1) * n)
    partial = n * n_1 + n * (n + 1) / 2 - n_1 * (n_1 + 1) / 2
    return partial if n_1 == 0 else partial + beatty_sqrt2(n_1)
    
def solution(str_n):
    n = long(str_n)
    return beatty_sqrt2(n)

if __name__ == "__main__":
    print(solution("77"))
    print(solution("5"))    