def get_primes():
    primes = [2]
    
    i = 3
    while len("".join(map(str, primes))) < 10000 + 5:
        is_prime = False
        for prime in primes:
            if (i % prime) != 0:
                is_prime = True
            else:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
        i += 1
    return primes

primes = get_primes()
primes_string = "".join(map(str, primes))

def solution(i):
    # Your code here
    return primes_string[i:i+5]

def test():
    cases = {
        0: "23571",
        3: "71113"
    }
    
    for k, v in cases.items():
        assert solution(k) == v, "Error for {} = {}, instead of {} = {}".format(k, solution(k), k, v)
        
test()