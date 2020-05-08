def get_two_sorted_nums(s):
    s_list_asc = [int(x) for x in s]
    s_list_asc.sort()
    s_list_desc = s_list_asc[:]
    s_list_desc.reverse()
    return s_list_desc, s_list_asc

def sottrazione_base_b(num1, num2, b):
    digits = len(num1)
    base = [b**x for x in range(digits-1,-1,-1)]
    num1_10 = sum( x*y for x,y in zip(num1,base) )
    num2_10 = sum( x*y for x,y in zip(num2,base) )

    result_10 = num1_10 - num2_10

    result = []
    reminder = result_10
    for elem_base in base:
        result.append( reminder // elem_base)
        reminder = reminder % elem_base
    return result

def solution(n, b):
    list_id = []
    while True:
        if n in list_id:
            where_is_it = list_id.index(n)
            return len(list_id) - where_is_it
        else:
            list_id.append(n)
        asc, rev = get_two_sorted_nums(n)
        result = sottrazione_base_b(asc, rev, b)
        n = ''.join([str(x) for x in result])