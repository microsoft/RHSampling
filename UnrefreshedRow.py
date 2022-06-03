from decimal import *

def PUnrefreshedRow(TH, tRC, tRFW):
    '''
    Computes the probability of a victim row not being refreshed 
    in a series of TH consecutive row activations

    :param int TH: Rowhammer threshold
    :param int tRC: Row cycle time
    :param int tRFW: Row refresh window
    :rtype: Decimal
    :raise TypeError: if parameters have incorrect types
    '''

    if (type(TH) != int or type(tRC) != int or type(tRFW) != int):
        raise TypeError("Incorrect parameter type")

    # We multiply by decimal to force conversion from int to decimal
    return (Decimal('1.0') - (Decimal('1.0') * tRC * TH / tRFW))

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
    # Check return type is Decimal
    if (Decimal != type(PUnrefreshedRow(10, 2, 2))):
        print("Test 1 failed")
        testsPassed = False

    # Test 2
    # Returns 1.0 when tRC = 0
    if (Decimal('1.0') != PUnrefreshedRow(0, 2, 2)):
        print("Test 2 failed")
        testsPassed = False

    # Test 3
    # Let P2 = probability of an unrefreshed victim row when TH is 2
    # Let P1 = probability of an unrefreshed victim row when TH is 1
    # Then P2 - 2 * P1 = -1.0
    P2 = PUnrefreshedRow(2, 350, 64 * 1000 * 1000)
    P1 = PUnrefreshedRow(1, 350, 64 * 1000 * 1000)
    if (Decimal('-1.0') != P2 - 2 * P1):
        print("Test 3 failed")
        testsPassed = False

    if(testsPassed):
        print("Success!")