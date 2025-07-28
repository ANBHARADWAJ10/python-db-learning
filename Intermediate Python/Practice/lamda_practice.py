import math
a = [1, 2, 3, 4, 5]
result = map(lambda x: math.pow(x,2), a)
result02 = map(lambda x: x**2, a)
print(list(result))
print(list(result02))
# result03 = [x]
# print(list(result03))


def prime(num):
    if num <= 1:
        return False
    elif num in [2,3]:
        return True
    else:
        for i in range(2, int(math.sqrt(num)+1)):
            if num % i == 0:
                return False
    return True
print(prime(15))

isprime = filter(lambda x: int(math.sqrt(x)%x != 0), a)
print(list(isprime))

# sieve of eratosthenes for primes:

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

ab = [1, 2, 3, 4, 5]

squares = map(lambda x: int(math.pow(x, 2)), ab)
new = list(squares)
print(new)

filtersthedata = filter(lambda x: x%2 == 0, a)
print(list(filtersthedata))

from functools import reduce
sumofall = reduce(lambda x, y: x + y, a)
print(sumofall)

enu = enumerate(a)
print(list(enu))

for key,value in zip(ab, a):
    print(key, value)

