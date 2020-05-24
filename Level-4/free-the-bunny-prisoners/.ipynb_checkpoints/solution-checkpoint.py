from itertools import combinations 

def distribute(num_buns, num_required):
    """
    Distributes n keys to each bunny such that each num_required bunny can open all the locks
    but num_required - 1 can't.
    The total number of keys is (math.factorial(num_buns) / math.factorial(num_required) / (num_buns - num_required)).
    Args:
        num_buns (int): the number of available bunnies
        num_required (int): the minimum number of required bunnies to open all locks
    Returns:
        List[List[int]]: Returns the list of keys received by each bunny
    """
    n_key_copies = num_buns - num_required + 1
    bunnies = [[] for _ in range(num_buns)]
    
    key = 0
    for bunnies_idx in combinations(range(len(bunnies)), n_key_copies):
        for idx in bunnies_idx:
            bunnies[idx].append(key)
        key += 1
    return bunnies


def solution(num_buns, num_required):
    return distribute(num_buns, num_required)


if __name__ == "__main__":
    tests = [
        {
            "q": (3, 1),
            "a": [[0], [0], [0]]
        },
        {
            "q": (2, 2),
            "a": [[0], [1]]
        },    
        {
            "q": (3, 2),
            "a": [[0, 1], [0, 2], [1, 2]]
        },   
        {
            "q": (2, 1),
            "a": [[0], [0]]
        },    
        {
            "q": (4, 4),
            "a": [[0], [1], [2], [3]]
        },
        {
            "q": (5, 3),
            "a": [[0, 1, 2, 3, 4, 5], [0, 1, 2, 6, 7, 8], [0, 3, 4, 6, 7, 9], [1, 3, 5, 6, 8, 9], [2, 4, 5, 7, 8, 9]]
        },  
    ]
    
    for test in tests:
        assert solution(*(test["q"])) == test["a"]