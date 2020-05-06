def build_bottom(bricks):
    # init table
    table = [[0 for i in range(bricks + 1)] for j in range(bricks + 1)]
    
    # init case
    table[0][0] = 1
    
    # tabulate
    for last in range(1, bricks + 1):
        for left in range(bricks + 1):
            # update state
            table[last][left] = table[last - 1][left]
            
            # check if next state is valid
            if left >= last:
                table[last][left] += table[last - 1][left - last]
    return table[bricks][bricks] - 1

def solution(n):
    return build_bottom(n)

def test():
    assert solution(3) == 1
    assert solution(200) == 487067745
    
if __name__ == "__main__":
    test()