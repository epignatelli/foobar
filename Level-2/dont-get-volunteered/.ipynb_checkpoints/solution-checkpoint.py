def get_checkboard():
    checkboard = []
    for i in range(8):
        checkboard.append(list(range(i * 8, (i + 1) * 8)))
    return checkboard

def get_position(src):
    x = int(src / 8)
    y = src - (8 * x)
    return x, y

def children(src):
    # get x, y position of src
    x, y = get_position(src)
    checkboard = get_checkboard()
    
    # available moves
    a = (x - 2, y + 1)
    b = (x - 1, y + 2)
    c = (x + 1, y + 2)
    d = (x + 2, y + 1)
    e = (x + 2, y - 1)
    f = (x + 1, y - 2)
    g = (x - 1, y - 2)
    h = (x - 2, y - 1)

    new_pos = []
    for move in [a, b, c, d, e, f, g, h]:
        # check if out of bounds
        if (move[0] >= 0 and move[0] < 8) and (move[1] >= 0 and move[1] < 8):
            x, y = move[0], move[1]
            # if move is legal (not out of bounds) save it
            new_pos.append(checkboard[move[0]][move[1]])
    return new_pos

def breadth_first_search(src, dest):
    queue = [src]
    level = {src: 0}
    
    while len(queue) > 0:
        # dequeue
        node = queue.pop(0)
        
        for child in children(node):
            # check if visited
            if child not in level:
                queue.append(child)
                # the distance of child from src is
                # level[node] + 1, inasmuch as level[node]
                # is the distance of src to node
                level[child] = level[node] + 1
            
            # have we found it?
            if child == dest:
                return level[dest]
    return 0

def solution(src, dest):
    return breadth_first_search(src, dest)
