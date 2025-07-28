def is_prime(num):
    # Create a boolean list to track prime status of numbers
    primes = [True] * (num + 1)
    primes[0] = primes[1] = False
    p = 2

    # Sieve of Eratosthenes algorithm
    while p * p <= num:
        if primes[p]:

            # Mark all multiples of p as non-prime
            for i in range(p * p, num + 1, p):
                primes[i] = False
        p += 1

    res = []
    for i in range(2, num + 1):
        if primes[i]:
            res.append(i)

    return res