def solution(l):
    l_list = [version_to_list(x) for x in l]
    l_list_sorted = bubble_sort(l_list)
    l_sorted = [list_to_version(x) for x in l_list_sorted]
    return l_sorted

def version_to_list(v):
    v = v.split(".")
    v = [int(x) for x in v]
    v.extend([None]*(3-len(v)))
    return v

def list_to_version(v):
    return '.'.join([str(x) for x in v if x is not None])

def is_ordered(x,y):
    if (x[0] > y[0]) or (y[0] is None and x[0] is not None):
        return False
    elif (x[0] < y[0]) or (x[0] is None and y[0] is not None):
        return True
    else:
        return is_ordered(x[1:],y[1:])

def bubble_sort(l):
    for first in range(len(l)-1):
        for second in range(first+1, len(l)):
            if not is_ordered(l[first], l[second]):
                _ = l[first]
                l[first] = l[second]
                l[second] = _
    return l

if __name__ == "__main__":
    l = ["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]
    sol = solution(l)
    assert sol == ["0.1","1.1.1","1.2","1.2.1","1.11","2","2.0","2.0.0"]

    sol = solution(["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"])
    assert sol == ["1.0","1.0.2","1.0.12","1.1.2","1.3.3"]




