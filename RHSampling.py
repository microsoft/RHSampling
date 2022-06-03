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
    description += '  for different configurations.'
    usage        = 'use "%(prog)s --help" for more information'
    parser = ArgumentParser(description=description, usage=usage, formatter_class=RawTextHelpFormatter)
    parser.add_argument("--cfg",  metavar='cfg',    type=str, default='armSRV', help="armSRV or armFLEET or skxSRV or skxFLEET (default: %(default)s)", choices = ['armSRV', 'armFLEET', 'skxSRV', 'skxFLEET'])
    parser.add_argument("--lt",   metavar='lt',     type=int, default=1,        help="System lifetime (hours)       (default: %(default)s)")
    parser.add_argument("--th",   metavar='th',     type=int, default=8192,     help="Rowhammer threshold           (default: %(default)s)")
    parser.add_argument("--prob", metavar='p',      type=Decimal,required=True, help="Probability of ACT selection  (required)")
    parser.add_argument("--prec", metavar="prec",   type=int, default=100,      help="Precision of computation      (default: %(default)s)")
    args = parser.parse_args()
    cfg  = args.cfg
    lt   = args.lt
    th   = args.th
    p    = args.prob
    prec = args.prec

    print('System lifetime (hours): {}'.format(lt))
    print('Rowhammer threshold: {}'.format(th))
    
    # Check config type
    if ('armSRV' == cfg):
        cfg  = armSRV
        mc   = armMC 
        dram = ddr5
        print('Config: ARM server, 1 node, 1 socket, 12 MCs (DDR5)')
    elif ('armFLEET' == cfg):
        cfg  = armFLEET
        mc   = armMC 
        dram = ddr5
        print('Config: ARM server fleet, 100K, 1 socket, 12 MCs (DDR5)')
    elif ('skxSRV' == cfg):
        cfg  = skxSRV
        mc   = skxMC 
        dram = ddr4
        print('Config: SKX server, 1 node, 2 sockets, 4 MCs (DDR4)')
    elif ('skxFLEET' == cfg):
        cfg  = skxFLEET
        mc   = skxMC 
        dram = ddr4
        print('Config: SKX server fleet, 100K, 2 sockets, 4 MCs (DDR4)')
    else:
        raise Exception('Bug! Unreachable code.')

    # Print MC info
    PrintMC(mc)

    # Compute window: number of row activations in system's lifetime
    # We use the integer division operator ('//') to avoid W from being converted to a float
    # These divisions should not have any remainders (pls. double check dram config)
    W  = (dram.tRFW - (dram.tRFC * dram.cREF)) // dram.tRC      # W in a refresh window
    W *= 3600 // (dram.tRFW // 1000 // 1000)                    # W in an hour
    W *= lt                                                     # W in lifetime

    print('Total # of ACTs in system\'s lifetime (in billions): {}'.format(W / 1000 / 1000 / 1000))

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

    # Compute the probability of a victim row escaping refreshing
    prob_no_refresh = PUnrefreshedRow(th, dram.tRC, dram.tRFW)

    # Compute probability of RH failure all banks in a system
    banks = Banks(cfg, mc)
    prob_rh_fail = Decimal('1.0') - (Decimal('1.0') - prob_no_sampling * prob_no_refresh) ** banks
    
    # Print result
    print('Probability of consecutive ACTs escaping sampling : {}'.format(format_e(prob_no_sampling)))
    print('Probability of victim row escaping refresh : {}'.format(format_e(prob_no_refresh)))
    print('Probability of RH failure in a system with {} banks: {}'.format(banks, format_e(prob_rh_fail)))

    # Check if Inexact or Rounded flags were set. If so, report to the user
    if context.flags[Inexact]:
        print(colored(255, 0, 0, 'Inexact answer: non-zero digits were discarded during rounding.'))
    elif context.flags[Rounded]:
        print(colored(255, 0, 0, 'Rounded answer: digits (possibly zeros) were discarded during rounding.'))
    if context.flags[Inexact] or context.flags[Rounded]:
        print(colored(255, 0, 0, 'Try re-running the script with increased precision and see if the answer changes.'))

