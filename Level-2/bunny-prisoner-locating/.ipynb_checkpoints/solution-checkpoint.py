def sum_series(n):
    last = 0
    for i in range (1, int(n)+1):
        last = last + i
    return last
    

def solution(x, y):
    d = x + y - 1
    start = sum_series(d - 1)
    k = start + x
    print("x, y", x, y)
    print("depth", d)
    print("k", k)
    print("---")
    return str(k)


solution(3, 2)
solution(5, 10)
solution(5, 1)
solution(5, 2)
solution(2, 4)
