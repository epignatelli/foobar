def bfs(maze, pos):
    w = len(maze[0])
    h = len(maze)
    level = {pos: 0}

    queue = [pos]
    while len(queue) > 0:
        # dequeue
        node = queue.pop(0)
        
        # move
        for i in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
            child = (node[0] + i[0], node[1] + i[1])
            # if out of bounds
            if 0 <= child[0] < h and 0 <= child[1] < w:
                if child not in level:
                    level[child] = level[node] + 1
                    # hit a wall
                    if maze[child[0]][child[1]] == 1:
                        continue
                    queue.append(child)
    return level

def solution(maze):
    w = len(maze[0])
    h = len(maze)
    # from start
    exit = bfs(maze, (0, 0))
    # from exit
    enter = bfs(maze, (h - 1, w - 1))

    shortest = float("inf")
    for x in range(h):
        for y in range(w):
            if (x, y) in exit and (x, y) in enter:
                shortest = min(exit[(x, y)] + enter[(x, y)] + 1, shortest)
    return shortest