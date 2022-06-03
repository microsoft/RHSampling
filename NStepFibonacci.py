from decimal import *
from utils   import InclusiveRange

def NStepFibonacci(k, n):
    '''
    Computes k-th n-Step Fibonacci number.

    Code based on the following article. 
    https://mathworld.wolfram.com/Fibonaccin-StepNumber.html

    Traditional Fibonacci numbers are 2-step (1, 1, 2, 3, 5, ...) where each number is the sum of the two previous ones.
    n-Step Fibonacci is the sum of the n previous ones. 
    5-Step Fibonacci are (1, 1, 2, 4, 8, 16, 31, 61, 120, ...)

    :param int n: n-Step
    :param int k: k-th n-Step Fibonacci number
    :rtype: Decimal
    :raise ValueError: if n is less or equal to 0
    :raise TypeError: if parameters have incorrect types
    '''
    if (type(n) != int or type(k) != int):
        raise TypeError("Incorrect parameter type")
    
    if n <= 0:
        raise ValueError("n must be greater than 0")
    elif k <= 0:
        return Decimal('0.0')
    elif k == 1 or k == 2:
        return Decimal('1.0')
    else:
        # F[k] is the kth n-step Fibonacci number

        # Step 0: Initialize to 0
        F = [0 for i in InclusiveRange(0, k)]

        # Step 00: F[1] = F[2] = 1
        F[1] = Decimal('1.0')
        F[2] = Decimal('1.0')

        # Step 1: Compute F[3] through F[k]
        for kIdx in InclusiveRange(3, k):
            tmp = Decimal('0')
            for i in InclusiveRange(1, n):
                if kIdx - i > 0:
                    tmp += F[kIdx - i]
            F[kIdx] += tmp

        return F[k]

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

    # Test 1
    # 10-th Fibonacci number is 55
    if (Decimal('55') != NStepFibonacci(10, 2)):
        print("Test 1 failed")
        testsPassed = False

    # Test 2
    # 9-th 7-step Fibonacci number is 127
    if (Decimal('127') != NStepFibonacci(9, 7)):
        print("Test 2 failed")
        testsPassed = False

    if(testsPassed):
        print("Success!")

    