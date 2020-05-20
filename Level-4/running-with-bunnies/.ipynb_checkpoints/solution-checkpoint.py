from itertools import chain, combinations, permutations

def trajectories(n_bunnies):
    """
    Returns a list of all possible trajectories, given the number of bunnies.
    It includes partial trajectories, e.g, [0, 1] in case of 3 bunnies.
    Args:
        n_bunnies (int): the total number of bunnies in the game
    Returns:
        (iterator): Returns all the possible trajectories in episode
    """
    states = range(n_bunnies)
    sets = list(chain.from_iterable(combinations(states, r) for r in range(len(states) + 1)))
    ts = set()
    for s in sets:
        ts.update(permutations(s))
    return ts
   

def floyd_warshall(times):
    """
    Finds the all-pairs shortest paths in the graph using the Floyd-Warshall algorithm.
    For a matrix u x v it stores the shortest path from u to v in m[u][v].
    Achieves O(V^3).
    Args:
        times (List[List[int]]): The adjacency matrix of the weighted graph
    Returns:
        A matrix of the same size of the adjacency matrix containing the shortest paths from
        a state to another. I.e. delta[u][v] contains the shortest distance from u to v.
    """
    d = len(times)
    delta = [[times[u][v] for v in range(len(times[u]))] for u in range(len(times))]
    for k in range(d):
        for u in range(d):
            for v in range(d):
                if delta[u][v] > delta[u][k] + delta[k][v]:  # is it shorter?
                    delta[u][v] = delta[u][k] + delta[k][v]
                    
    for u in range(d):
        if delta[u][u] < 0:  # is there a negative cycle to itself?
            return None            
    return delta


def run(trajectory, deltas):
    """
    Makes a run, starting from the door and getting to the exit, and passing
    through the bunnies asked to rescue in the trajectory
    Args:
        trajectory (List[int]): The list of bunnies id to rescue
        deltas (List[List[int]]): The square matrix of shortest paths to another state
    Returns:
        (int): The time spent to walk through the hallway, starting from the door, saving the 
        requested bunnies and getting to the door
    """
    elapsed = 0
    parent = 0  # start at the door
    # get the bunnies 
    for bunny_id in trajectory:
        state_id = bunny_id + 1  # skip the door
        elapsed += deltas[parent][state_id]
        parent = state_id
    # got to the exit
    elapsed += deltas[parent][len(deltas) - 1]
    return elapsed


def optimise(deltas, time_limit):
    """
    Given the matrices of deltas fo a graph and the max number of moves to make, it returns the
    highest number of bunnies to be able to catch.
    It iterates over all the possible trajectories and returns the one that provides most bunnies.
    Args:
        deltas (List[List[int]]) a square matrix containing the shortest paths for all pair-wise
        combinations of nodes in the graph
        time_limit (int): the max distance allowed to go, while saving the bunnies
    Returns:
        (List[int]): A list containing the ids of the bunnies we have been able to save
    """
    n = len(deltas) - 2
    bunnies = [x for x in range(len(deltas) - 2)]
    trajs = trajectories(len(bunnies))

    best_rescue = []
    for traj in sorted(trajs):
        print(str(traj))
        # get the total time spent for the rescue run
        elapsed = run(traj, deltas)
        print("elapsed", elapsed)
        # how many bunnies am I saving?
        n_saved = len(traj)
        # did I exceed time limit?
        print("out of time", time_limit, ">", elapsed, elapsed > time_limit)
        if elapsed > time_limit:
            continue
        # ok, we made it in time, is this rescue better than the current best?
        print("better rescue", n_saved, ">", len(best_rescue), n_saved > len(best_rescue))
        if n_saved > len(best_rescue):
            best_rescue = traj
            # we got a better choice, have I already saved all bunnies?
            if n_saved == len(bunnies):
                return traj
        print("---")
    print(best_rescue)
    return sorted(best_rescue)

        
def solution(times, time_limit):
    if len(times) <= 2:
        return []
    deltas = floyd_warshall(times)
    if deltas is None:
        return list(range(len(times) - 2))
    bunnies = optimise(deltas, time_limit)
    return sorted(bunnies)


def test(m, t, a):
    r = solution(m, t)
    assert r == a, "{} different from {}".format(r, a)
    

if __name__ == "__main__":
    test([[0,  1,  5,  5,  2],
          [10, 0,  2,  6,  10],
          [10, 10, 0,  1,  5],
          [10, 10, 10, 0,  1],
          [10, 10, 10, 10, 0]], 5, [0, 1, 2])
    
    test([[0, 1, 3, 4, 2],
          [10, 0, 2, 3, 4],
          [10, 10, 0, 1, 2],
          [10, 10, 10, 0, 1],
          [10, 10, 10, 10, 0]], 4, [])            
    
    test([[0, 2, 2, 2, -1],
          [9, 0, 2, 2, -1],
          [9, 3, 0, 2, -1],
          [9, 3, 2, 0, -1],
          [9, 3, 2, 2, 0]], 1, [1, 2])    
    
    test([[0,  1, 10, 10, 10],
          [10, 0,  1,  1,  2],
          [10, 1,  0, 10, 10],
          [10, 1,  10, 0, 10],
          [10, 10, 10, 10, 0]], 7, [0, 1, 2])
    
    test([[0, 1, 1, 1, 1],
          [1, 0, 1, 1, 1],
          [1, 1, 0, 1, 1],
          [1, 1, 1, 0, 1],
          [1, 1, 1, 1, 0]], 3, [0, 1])
    
    test([[0, 5, 11, 11, 1],
          [10, 0, 1, 5, 1],
          [10, 1, 0, 4, 0],
          [10, 1, 5, 0, 1],
          [10, 10, 10, 10, 0]], 10, [0, 1])
    
    test([[0, 20, 20, 20, -1],
          [90, 0, 20, 20, 0],
          [90, 30, 0, 20, 0],
          [90, 30, 20, 0, 0],
          [-1, 30, 20, 20, 0]], 0, [0, 1, 2])
    
    test([[0, 10, 10, 10, 1],
          [0, 0, 10, 10, 10],
          [0, 10, 0, 10, 10],
          [0, 10, 10, 0, 10],
          [1, 1, 1, 1, 0]], 5, [0, 1])
    
    test([[0, 10, 10, 1, 10],
         [10, 0, 10, 10, 1],
         [10, 1, 0, 10, 10],
         [10, 10, 1, 0, 10],
         [1, 10, 10, 10, 0]], 6, [0, 1, 2])
    
    test([[1, 1, 1, 1, 1, 1, 1],    
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1]], 1, [])
    
    test([[0, 0, 1, 1, 1],
          [0, 0, 0, 1, 1],
          [0, 0, 0, 0, 1],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0]], 0, [0, 1, 2])
    
    
    test([[1, 1, 1, 1, 1],
          [-1, 1, 1, 1, 1],
          [-1, 1, 1, 1, 1],
          [-1, 1, 1, 1, 1],
          [-1, 1, 1, 1, 1]], 1, [0, 1, 2])
    
    test([[0, 1, 5, 5, 5, 5],
          [5, 0, 1, 5, 5, 5],
          [5, 5, 0, 5, 5, -1],
          [5, 5, 1, 0, 5, 5],
          [5, 5, 1, 5, 0, 5],
          [5, 5, 1, 1, 1, 0]], 3, [0, 1, 2, 3])
    
    test([[0, 1, 5, 5, 5, 5, 5],
          [5, 0, 1, 5, 5, 5, 5],
          [5, 5, 0, 5, 5, 0, -1],
          [5, 5, 1, 0, 5, 5, 5],
          [5, 5, 1, 5, 0, 5, 5],
          [5, 5, 0, 5, 5, 0, 0],
          [5, 5, 1, 1, 1, 0, 0]]
          , 3, [0, 1, 2, 3, 4])    
    
    test([[0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0]], 0, [0, 1, 2])