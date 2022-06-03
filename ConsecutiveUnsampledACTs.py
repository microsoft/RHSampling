from decimal        import *
from tqdm           import tqdm
from utils          import InclusiveRange
from KHeadsInARow   import *

def pUnsampledConsecutiveACTs(N, TH, p, MEMORY_OPTIMIZED):
    '''
    Computes probability of TH consecutive unsampled ACTs recursively.
        All this code implements the formula from DRAMSec 2022 paper titled
        "How to Correctly Configure Row-Sampling-Based Rowhammer Defenses"
    :param int N: number of row activations
    :param int TH: Rowhammer threshold
    :param Decimal p: probability of sampling a row ACT
    :param dram: dram config (namedtuple)
    :param MEMORY_OPTIMIZED: run a slower, but more memory-efficient version of the algorithm
    :rtype: Decimal
    :raise ValueError: if N and TH are less or equal than 0
    :raise TypeError: if parameters have incorrect types
    '''

    if (type(N) != int or type(TH) != int or type(p) != Decimal):
        raise TypeError("Incorrect parameter type")

    q = Decimal('1.0') - p

    if (N <= 0 or TH <= 0):
        raise ValueError("N and TH must be greater than 0")
    elif N < TH:
        return 0
    elif N == TH:
        return q**TH
    else:
        qToTheTH = q**TH
        pTimesqToTheTH = p * qToTheTH

        if 0 == MEMORY_OPTIMIZED:
            P = [0 for i in InclusiveRange(0,N)]
            P[TH] = qToTheTH

            for nIdx in tqdm(InclusiveRange(TH, N - 1)):
                P[nIdx + 1] = P[nIdx] + pTimesqToTheTH * (Decimal('1.0') - P[nIdx-TH])

            return P[N]
        else:
            P=[]
            for i in InclusiveRange(0, TH-1):
                P.append(0)
            P.append(qToTheTH)

            prev = qToTheTH
            for i in tqdm(InclusiveRange(TH, N-1)):
                prev = prev + pTimesqToTheTH * (Decimal('1.0') - P.pop(0))
                P.append(prev)

            return P.pop()            

# Main is used for testing only
if __name__ == '__main__':
    '''
    Decimal is initialized using strings or tuples, such as:
      Decimal('1.0')
      Decimal((0, (1, 0), -1))  # tuple format (sign, tuple_of_digits, integer_exponent) sign is 0 for + and 1 for -
    An incorrect way of initializing Decimal is Decimal(1.0) which coverts 1.0 to float first (losing precision)
    '''

    # We set precision to 2000000 and set all sorts of traps
    # We do not set rounding because we want to trap whenever rounding occurs
    context = Context(prec=2000000, traps=[Overflow, Underflow, Rounded, Inexact, FloatOperation])
    setcontext(context)

    testsPassed = True

    pFairCoin = Decimal('0.5')
    pUnfairCoin = Decimal('0.1')

    # Test both implementations: memory-optimized and non-memory-optimized

    # Test 1
    # Check return type is Decimal
    if (Decimal != type(pUnsampledConsecutiveACTs(10, 2, pFairCoin, 0)) and 
        Decimal != type(pUnsampledConsecutiveACTs(10, 2, pFairCoin, 1))):
        print("Test 1 failed")
        testsPassed = False

    # Test 2
    # Check against KHeadsInARow
    if (pUnsampledConsecutiveACTs(10, 2, pFairCoin, 0) != kHeadsInARow(10, 2, Decimal('1.0') - pFairCoin) and
        pUnsampledConsecutiveACTs(10, 2, pFairCoin, 1) != kHeadsInARow(10, 2, Decimal('1.0') - pFairCoin)):
        print("Test 2 failed")
        testsPassed = False

    # Test 3
    # Check against KHeadsInARow
    if (pUnsampledConsecutiveACTs(1000, 1000, pUnfairCoin, 0) != kHeadsInARow(1000, 1000, Decimal('1.0') - pUnfairCoin) and
        pUnsampledConsecutiveACTs(1000, 1000, pUnfairCoin, 1) != kHeadsInARow(1000, 1000, Decimal('1.0') - pUnfairCoin)):
        print("Test 3 failed")
        testsPassed = False    

    # Test 4
    # Check against KHeadsInARow
    if (pUnsampledConsecutiveACTs(1000, 256, pUnfairCoin, 0) != kHeadsInARow(1000, 256, Decimal('1.0') - pUnfairCoin) and
        pUnsampledConsecutiveACTs(1000, 256, pUnfairCoin, 1) != kHeadsInARow(1000, 256, Decimal('1.0') - pUnfairCoin)):
        print("Test 4 failed")
        testsPassed = False   

    if(testsPassed):
        print("Success!")
