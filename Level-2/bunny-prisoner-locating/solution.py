def sum_series(n):
    last = 0
    for i in range (1, int(n)+1):
        last = last + i
    return last
    

def solution(x, y):
    d = x + y - 1
    start = sum_series(d - 1)
    k = start + x
    return str(k)
