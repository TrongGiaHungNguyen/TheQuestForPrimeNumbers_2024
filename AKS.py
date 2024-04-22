import math
import multiprocessing
import decimal
import time

decimal.getcontext().prec = 400

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

def main():
    # Example number to test
    start_time = time.time()
    result = aks(4000060000800009000010000012000014000015000016000018000020000021000022000024000025000026000027000028000030000032000033000034000035000036000038000039000040000042000044000045000046000048000049000050000051)
    #result = aks(120118116114112110108106104102100989694929088868482807876747270686664626058565452504846444240383634323028262422201816141210864213579111315171921232527293133353739414345474951535557596163656769717375777981838587899193959799101103105107109111113115117119121)
    #result = aks(100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000118000000080101811009000118101080000000811000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
    #result = aks(147905612304049314530022347858051795393169843567686496119778103525328675398119462130526918624189025093221823879535477996560410449665190880468513606241420472470681055332721887591747863405964601930591007609161946038677991696595604464433826327996801243951556854274701334312260550305897135170116383049658549024443746904511563699126930309386309517504941636470564772320067276393)
    end_time = time.time()
    print(f"Testing number: {'Prime' if result else 'Composite'}")
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
