from decimal    import *
from tqdm       import tqdm
from utils      import InclusiveRange

def NotKHeadsInARow(n, k, p):
    '''
    Computes probability of not flipping k heads in a row
    given a series of n coin flips

    Code based on StackExchange article:
    https://math.stackexchange.com/questions/148353/given-n-raffles-what-is-the-chance-of-winning-k-in-a-row

    The article derives a few recursive equations. The code inverts the recursion into dynamic programming.

    :param int n: number of coin flips
    :param int k: number of heads in a row
    :param Decimal p: probability of flipping a head
    :rtype: Decimal
    :raise ValueError: if n and k are less or equal than 0
    :raise TypeError: if parameters have incorrect types
    '''
    if (type(n) != int or type(k) != int or type(p) != Decimal):
        raise TypeError("Incorrect parameter type")

    if n <= 0 or k <= 0:
        raise ValueError("n and k must be greater than 0")
    elif n < k:
        return 1
    else:
        q = Decimal('1.0') - p

        # Pre-compute the values for p^i. We'll use them a lot in the math below
        PowersOfP = []
        PowersOfP.append(Decimal('1.0'))
        for i in InclusiveRange(1, k-1):
            PowersOfP.append(p * PowersOfP[i-1])

        # P[n] is the probability that a string of length n has less than k heads in a row *and* it ends with 0 heads 
        #   It corresponds to P(n,k,0) in the article. The rest of this code computes this probability using dynamic programming

        # Step 0: Initialize to -1
        P = [-1 for i in InclusiveRange(0,n)]

        # Step 00: Initialize P[0] to 1
        # The probability that a string of length 0 has less than 0 heads in a row *and* ends with 0 heads is 1
        P[0] = 1

        # Step 1: Compute P[1] through P[k]
        # P(n,k,0) is q whenever n <= k
        #   when n < k
        #     corresponds to probability that a string of length n has less than k heads in a row, which is 1 when n < k
        #     *and* the string of length n ends with a tail, which is q
        #   when n = k
        #     reduces to probability that last flip is a tail, which is q
        for nIdx in InclusiveRange(1,k):
            P[nIdx] = q

        # Step 2: Compute P[k+1] through P[n]
        # P(n+1, k, 0) = q * \sum_{i=0}^{k-1} p^i * P(n-i, k, 0)
        for nIdx in tqdm(InclusiveRange(k, n - 1)):
            tmp = Decimal('0')
            for i in InclusiveRange(0, k-1):
                tmp += PowersOfP[i] * P[nIdx - i]
            P[nIdx + 1] = q * tmp

        #  We can now compute P(n,k) from all the P(n,k,0)s computed above (i.e., stored in P[])
        # P(n, k) = \sum_{i=0}^{k-1} p^i * P(n-i, k, 0)
        tmp = Decimal('0')
        for i in InclusiveRange(0,k-1):
            tmp += PowersOfP[i] * P[n-i]

        return tmp


def kHeadsInARow(n, k, p):
    return Decimal('1.0') - NotKHeadsInARow(n, k, p)

# Main is used for testing only
if __name__ == '__main__':
    '''
    Decimal is initialized using strings or tuples, such as:
      Decimal('1.0')
      Decimal((0, (1, 0), -1))  # tuple format (sign, tuple_of_digits, integer_exponent) sign is 0 for + and 1 for -
    An incorrect way of initializing Decimal is Decimal(1.0) which coverts 1.0 to float first (losing precision)
    '''

    from NStepFibonacci import *

    # We set precision to 2000000 and set all sorts of traps
    # We do not set rounding because we want to trap whenever rounding occurs
    context = Context(prec=2000000, traps=[Overflow, Underflow, Rounded, Inexact, FloatOperation])
    setcontext(context)

    pFairCoin = Decimal('0.5')
    pUnfairCoin = Decimal('0.1')

    testsPassed = True

    # Test 1
    # Flipping 1 heads in a row given 1 coin flips is 1-in-2
    if (Decimal('0.50') != kHeadsInARow(1, 1, pFairCoin)):
        print("Test 1 failed")
        testsPassed = False

    # Test 2
    # Flipping 1 heads in a row given 2 coin flips is 3-in-4
    if (Decimal('0.75') != kHeadsInARow(2, 1, pFairCoin)):
        print("Test 2 failed")
        testsPassed = False

    # Test 3
    # Flipping 2 heads in a row given 2 coin flips is 1-in-4
    if (Decimal('0.25') != kHeadsInARow(2, 2, pFairCoin)):
        print("Test 3 failed")
        testsPassed = False

    # Test 4
    # Flipping 1 heads in a row given 3 coin flips is 7-in-8
    if (Decimal('0.875') != kHeadsInARow(3, 1, pFairCoin)):
        print("Test 4 failed")
        testsPassed = False

    # Test 5
    # Flipping 2 heads in a row given 3 coin flips is 3-in-8
    if (Decimal('0.375') != kHeadsInARow(3, 2, pFairCoin)):
        print("Test 5 failed")
        testsPassed = False

    # Test 6
    # Flipping 3 heads in a row given 3 coin flips is 1-in-8
    if (Decimal('0.125') != kHeadsInARow(3, 3, pFairCoin)):
        print("Test 6 failed")
        testsPassed = False

    # Test 7
    # Flipping 3 heads in a row given 2 coin flips is 0
    if (Decimal('0') != kHeadsInARow(2, 3, pFairCoin)):
        print("Test 7 failed")
        testsPassed = False

    # Test 8
    # Flipping 1 heads in a row given 1 biased-coin flips (p=0.1) is 0.1
    if (Decimal('0.1') != kHeadsInARow(1, 1, pUnfairCoin)):
        print("Test 8 failed")
        testsPassed = False

    # Test 9
    # Flipping 2 heads in a row given 2 biased-coin flips (p=0.1) is 0.01
    if (Decimal('0.01') != kHeadsInARow(2, 2, pUnfairCoin)):
        print("Test 9 failed")
        testsPassed = False

    # Test 10
    # Flipping 1000 heads in a row given 1000 biased-coin flips (p=0.1) is (0.1)^100
    if ((Decimal('0.1') ** 1000) != kHeadsInARow(1000, 1000, pUnfairCoin)):
        print("Test 10 failed")
        testsPassed = False

    # Test 11
    # Flipping 3 heads in a row given 5 coin flips is a function of the 7th 3-step Fibonacci
    # See https://math.stackexchange.com/questions/148353/given-n-raffles-what-is-the-chance-of-winning-k-in-a-row
    if (1 - NStepFibonacci(7, 3) / (Decimal('2') ** 5)) != kHeadsInARow(5, 3, pFairCoin):
        print("Test 11 failed")
        testsPassed = False

    # Test 12
    # Flipping 59 heads in a row given 100 coin flips is a function of the 102nd 59-step Fibonacci
    # See https://math.stackexchange.com/questions/148353/given-n-raffles-what-is-the-chance-of-winning-k-in-a-row
    if (1 - NStepFibonacci(102, 59) / (Decimal('2') ** 100)) != kHeadsInARow(100, 59, pFairCoin):
        print("Test 12 failed")
        testsPassed = False

    if(testsPassed):
        print("Success!")
