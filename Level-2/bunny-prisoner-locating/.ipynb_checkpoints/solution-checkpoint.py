def sum_series(n):
    """
    Given a number n, returns the sum of all the integers from 1 to n
    """
    last = 0
    for i in range (1, int(n)+1):
        last = last + i
    return last
    

def solution(x, y):
    # get the depth of the diagonal
    d = x + y - 1
    # once we know the depth, we know
    # what number the diagonal starts from 
    start = sum_series(d - 1)
    # and k is just the x offset from that start 
    k = start + x
    return str(k)
