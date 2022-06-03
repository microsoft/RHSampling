from collections    import namedtuple

DDR5 = namedtuple("DDR5", "tRFW tRC tRFC cREF")
DDR4 = namedtuple("DDR4", "tRFW tRC tRFC cREF")

'''
Default timings for DDR5
tRFW =  32 ms (refresh window)
tRC  =  46 ns (minimum ACT-to-ACT gap)
tRFC = 410 ns (row refresh cycle time -- timing for when no activity allowed after REF issued)
cREF = 8192   (number of REFs during 1 tRFW)
'''
ddr5 = DDR5(    32 * 1000 * 1000,   \
                46,                 \
                410,                \
                8192                \
            )

'''
Default timings for DDR4
tRFW =  64 ms (refresh window)
tRC  =  46 ns (minimum ACT-to-ACT gap)
tRFC = 350 ns (row refresh cycle time -- timing for when no activity allowed after REF issued (CHECK THIS!
cREF = 8192   (number of REFs during 1 tRFW)
'''
ddr4 = DDR4(    64 * 1000 * 1000,   \
                46,                 \
                350,                \
                8192                \
            )

def PrintDDR(DDR):
    '''
    Prints DDR timings
    '''

    print("DDR timings (nanoseconds):")
    print("  tRFW: {}".format(DDR.tRFW))
    print("  tRC:  {}".format(DDR.tRC))
    print("  tRFC: {}".format(DDR.tRFC))
    print("  cREF: {}".format(DDR.cREF))