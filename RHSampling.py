from argparse                   import ArgumentParser, RawTextHelpFormatter
from configs.ddr                import *
from configs.system             import *
from tqdm                       import tqdm
from utils                      import *
from KHeadsInARow               import *
from ConsecutiveUnsampledACTs   import *
from UnrefreshedRow             import *

   
# Some of our code is memory intensive and it might run out of memory. In that case set MEMORY_OPTIMIZED to 1
MEMORY_OPTIMIZED = 1

'''
Main entry point for computing the probability of RH failures in a system
    for different configurations of a row-sampling scheme
'''

if __name__ == '__main__':
    # Start with arg parsing
    description  = 'Analysis for a row-sampling Rowhammer defense\n'
    description += '  computes the probability of a RowHammer failure in a system\n'
    description += '  given a sampling rate for different system configurations.'
    usage        = 'use "%(prog)s --help" for more information'
    parser = ArgumentParser(description=description, usage=usage, formatter_class=RawTextHelpFormatter)
    parser.add_argument("--cfg",  metavar='cfg',    type=str, default='armSRV', help="armSRV/armFLEET/icxSRV/icxFLEET/A/B   (default: %(default)s)", choices = ['armSRV', 'armFLEET', 'icxSRV', 'icxFLEET', 'A', 'B'])
    parser.add_argument("--lt",   metavar='lt',     type=int, default=1,        help="Attack lifetime (hours)               (default: %(default)s)")
    parser.add_argument("--th",   metavar='th',     type=int, default=8192,     help="Rowhammer threshold                   (default: %(default)s)")
    parser.add_argument("--rate", metavar='p',      type=Decimal,required=True, help="Sampling rate (required)              (no default value)")
    parser.add_argument("--prec", metavar="prec",   type=int, default=100,      help="Precision of computation              (default: %(default)s)")
    args = parser.parse_args()
    cfg  = args.cfg
    lt   = args.lt
    th   = args.th
    p    = args.rate
    prec = args.prec

    print('System lifetime (hours): {}'.format(lt))
    print('Rowhammer threshold: {}'.format(th))
    
    # Check config type
    if ('armSRV' == cfg):
        host = armSRV 
        dram = drDDR5
        ddr = ddr5
    elif ('armFLEET' == cfg):
        host = armFLEET 
        dram = drDDR5
        ddr = ddr5
    elif ('icxSRV' == cfg):
        host = icxSRV 
        dram = drDDR5
        ddr = ddr5
    elif ('icxFLEET' == cfg):
        host = icxFLEET 
        dram = drDDR5
        ddr = ddr5
    elif ('A' == cfg):
        host = hostA 
        dram = dramA
        ddr = ddr5
    elif ('B' == cfg):
        host = hostB 
        dram = dramB
        ddr = ddr5
    else:
        raise Exception('Bug! Unreachable code.')

    # Print CFG and CPU info
    print("System configuration: {}".format(cfg))
    PrintConfig(host)
    PrintDRAM(dram)
    PrintDDR(ddr)

    # Compute window: number of row activations in system's lifetime
    # We use the integer division operator ('//') to avoid W from being converted to a float
    # These divisions should not have any remainders (pls. double check dram config)
    W  = (ddr.tRFW - (ddr.tRFC * ddr.cREF)) // ddr.tRC      # W in a refresh window
    W *= 3600 // (ddr.tRFW // 1000 // 1000)                 # W in an hour
    W *= lt                                                 # W in lifetime

    print('Total # of banks: {}'.format(Banks(host, dram)))
    print('Approx # of ACTs in attack\'s lifetime (in billions): ~{:.2f}'.format(W / 1000 / 1000 / 1000))

    # Setup the context for the decimal operations. 
    # We do set traps on Inexact and Rounding, but flags only. A flag does not throw an exception, whereas trap does.
    # We will report the flags, and it is up to the user to decide on the desired precision of the computation.
    context = Context(prec=prec, traps=[Overflow, Underflow, FloatOperation], flags=[Inexact, Rounded])
    context.clear_flags()
    setcontext(context)

    # Compute probability of escaping sampling
    # We have two ways of doing it: using the K-Heads-In-a-Row scheme, or using the unsampled ACTs scheme.
    # The former is very slow, and we only use it for testing purposes. The latter is much faster.
    # 1/ Using the K-Heads-In-A-Row algorithm 
    #prob_no_sampling = kHeadsInARow(W, th, Decimal('1.0') - p)

    # 2/ Using the unsampled ACTs algorithm
    prob_no_sampling = pUnsampledConsecutiveACTs(W, th, p, MEMORY_OPTIMIZED)
    # print('Probability of consecutive ACTs escaping sampling : {}'.format(format_e(prob_no_sampling)))

    # Compute the probability of a victim row escaping refreshing
    prob_no_refresh = PUnrefreshedRow(th, ddr.tRC, ddr.tRFW)
    # print('Probability of victim row escaping refresh : {}'.format(format_e(prob_no_refresh)))

    # Compute probability of RH failure all banks in a system
    banks = Banks(host, dram)
    prob_rh_fail = Decimal('1.0') - (Decimal('1.0') - prob_no_sampling * prob_no_refresh) ** banks
    print('\nProbability of RH failure in a system with {} banks: {}'.format(banks, format_e(prob_rh_fail)))

    # Given the nature of the computations above, the results are always inexact and rounded. 
    # Showing a warning for an event that always occurs is a little silly.
    # Comment out these warnings 
    # # Check if Inexact or Rounded flags were set. If so, report to the user
    # if context.flags[Inexact]:
    #     print(colored(255,204, 0, 'Inexact answer: non-zero digits were discarded during rounding.'))
    # elif context.flags[Rounded]:
    #     print(colored(255, 204, 0, 'Rounded answer: digits (possibly zeros) were discarded during rounding.'))
    # if context.flags[Inexact] or context.flags[Rounded]:
    #     print(colored(255, 204, 0, 'Try re-running the script with increased precision and see if the answer changes.'))

