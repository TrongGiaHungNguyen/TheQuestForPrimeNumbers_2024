import math
import multiprocessing
import decimal
import time
import random

decimal.getcontext().prec = 500

def find_invpowAlt(x, n):
    """ Finds the integer component of the n'th root of x, an integer such that y ** n <= x < (y + 1) ** n. """
    low = 10 ** (len(str(x)) / n)
    high = low * 10
    while low < high:
        mid = (low + high) // 2
        if low < mid and decimal.Decimal(mid) ** n < x:
            low = mid
        elif high > mid and decimal.Decimal(mid) ** n > x:
            high = mid
        else:
            return mid
    return mid + 1

def phi(n):
    """ Calculate Euler's totient function. """
    amount = 0
    for k in range(1, n + 1):
        if math.gcd(k, n) == 1:
            amount += 1
    return amount

def step1(n):
    """ Check for perfect powers. """
    for b in range(2, math.floor(math.log2(n) + 1)):
        a = find_invpowAlt(n, b)
        if decimal.Decimal(a) ** decimal.Decimal(b) == n:
            print(f"{n} - composite. Step 1")
            return False
    return True

def step2(n):
    """ Find the smallest r such that ord_r(n) > (log n)^2. """
    mk = math.floor(math.log2(n) ** 2)
    r = mk
    while True:
        if math.gcd(r, n) == 1:
            k = 1
            s = n % r
            while k <= mk:
                s = (s * n) % r
                if s == 1:
                    break
                k += 1
            if k > mk:
                return r
        r += 1

def step3(n, r):
    """ Check if gcd(a, n) = 1 for all a ≤ r. """
    for a in range(1, r + 1):
        if 1 < math.gcd(a, n) < n:
            return False
    return True

def step4(n, r):
    """ Check if n ≤ r. """
    if n <= r:
        print(f"{n} - prime. Step 4")
        return True
    return False

def step5_check(start, end, n):
    """ Check if (X + a)^n ≡ X^n + a (mod X^r - 1, n) for each a in the range start to end. """
    for a in range(start, end):
        if pow(a, n, n) != a:
            return False
    return True

def step5(n, r):
    """ Final check for primality using multiprocessing. """
    max_a = int(math.sqrt(phi(r)) * math.log2(n))
    if max_a > n:
        max_a = n
    ran = max(1, max_a // 8)

    with multiprocessing.Pool() as pool:
        results = pool.starmap(step5_check, [(i, min(i + ran, max_a + 1), n) for i in range(1, max_a + 1, ran)])
        if all(results):
            print(f"{n} - prime. Step 5")
            return True
    return False

def aks(n):
    """ AKS primality test. """
    if step1(n):
        r = step2(n)
        if step3(n, r) and (step4(n, r) or step5(n, r)):
            return True
    return False

def miller_rabin(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n as 2^r * d + 1
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Miller-Rabin test
    def witness(a, d, n):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False
        return True

    # Repeat the test k times
    for _ in range(k):
        a = random.randint(2, n - 2)
        if witness(a, d, n):
            return False  # n is composite
    return True  


def main():
    start_time = time.time()
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]

    for _ in range(5):
        newPrime = 1
        for item in primes:
            newPrime *= item

        newPrime += 1
        
        while (miller_rabin(newPrime) == False or aks(newPrime) == False):
            newPrime += 2
    
        primes.append(newPrime)
    
    end_time = time.time()
    
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
