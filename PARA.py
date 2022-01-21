from argparse import *
from tqdm import tqdm
from KHeadsInARow import *

def format_e(n):
    a = '%E' % n
    return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

'''
Computes probability of RowHammer failure in a window of w row activations, given sampling rate p and
    DRAM with mac threshold
'''

if __name__ == '__main__':
    '''
    Default parameters for DDR5 bank
    tRFW =  32 ms (refresh window)
    tRC  =  46 ns (minimum ACT-to-ACT gap)
    tRFC = 410 ns (row refresh cycle time -- timing for when no activity allowed after REF issued)
    cREF = 8192   (number of REFs during 1 tRFW)
    '''
    tRFW = 32 * 1000 * 1000
    tRC  = 46
    tRFC = 410
    cREF = 8192
    W    = int((tRFW - (tRFC * cREF)) / tRC)

    MAC  = 8192               # default MAC value
    p    = Decimal('0.01')    # default row activate selection probability

    # Start with arg parsing
    description  = 'Analysis for RowHammer Probabilistic Adjacent Row Activate (PARA)\n'
    description += '  computes the probability of a RowHammer failure of a DRAM with a given MAC\n'
    description += '  in a window of w row activations given a sampling rate p.'
    usage        = 'use "%(prog)s --help" for more information'
    parser = ArgumentParser(description=description, usage=usage, formatter_class=RawTextHelpFormatter)
    parser.add_argument("--w", metavar='w',         type=int, default=W,        help="# of ACTs in refresh window   (default: %(default)s)")
    parser.add_argument("--mac", metavar='mac',     type=int, default=MAC,      help="Maximum Activate Count        (default: %(default)s)")
    parser.add_argument("--prob", metavar='p',      type=Decimal, default=p,    help="Probability of ACT selection  (default: %(default)s)")
    parser.add_argument("--prec", metavar="prec",   type=int, default=100,      help="Precision of computation      (default: %(default)s)")
    args = parser.parse_args()
    W    = args.w
    MAC  = args.mac
    p    = args.prob
    prec = args.prec

    # Setup the context for the decimal operations. 
    # We do set traps on Inexact and Rounding, but flags only. A flag does not throw an exception, whereas trap does.
    # We will report the flags, and it is up to the user to decide on the desired precision of the computation.
    context = Context(prec=prec, traps=[Overflow, Underflow, FloatOperation], flags=[Inexact, Rounded])
    context.clear_flags()
    setcontext(context)
    
    # Compute probability of RowHammer failure
    #   That is the probability we have MAC unsampled rows back-to-back in a window of size W
    prob_rh_fail = kHeadsInARow(W, MAC, Decimal('1.0') - p)
    print(format_e(prob_rh_fail))
    
    # Check if Inexact or Rounded flags were set. If so, report to the user
    if context.flags[Inexact]:
        print(colored(255, 0, 0, 'Inexact answer: non-zero digits were discarded during rounding.'))
    elif context.flags[Rounded]:
        print(colored(255, 0, 0, 'Rounded answer: digits (possibly zeros) were discarded during rounding.'))
    if context.flags[Inexact] or context.flags[Rounded]:
        print(colored(255, 0, 0, 'Try re-running the script with increased precision and see if the answer changes.'))

