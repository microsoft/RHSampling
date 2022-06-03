from collections    import namedtuple

SYS = namedtuple('SYS', 'nodes sockets MCs')
MC  = namedtuple('MC',  'channels DPC ranks bgroups banks')

'''
Datacenter of ARM servers: 100K, 1 sockets, 12MCs
'''
armFLEET = SYS(100 * 1000, 1, 12)

'''
Datacenter of SKX servers: 100K, 2 sockets, 4MCs
'''
skxFLEET = SYS(100 * 1000, 2, 4)

'''
ARM server: 1 node, 1 socket, 12 MCs
'''
armSRV = SYS(1, 1, 12)

'''
Dual-socket SKX server: 1 node, 2 sockets, 4 MCs
'''
skxSRV = SYS(1, 2, 4)

'''
Skylake MC: 3 channels, 2 DPC, 2 ranks, 2 BGs, 2 BAs
'''
skxMC = MC(3, 2, 2, 2, 2)

'''
ARM MC: 1 channel, 1 DPC, 2 ranks, 3 BG2, 2BAs 
'''
armMC = MC(1, 1, 2, 3, 2)

def Banks(SYS, MC):
    '''
    Computes the number of banks in a system
    :param SYS: system config (namedtuple)
    :param MC: memory controller config (namedtuple)
    :rtype: int
    '''

    return SYS.nodes * SYS.sockets * SYS.MCs * MC.channels * MC.DPC * MC.ranks * MC.bgroups * MC.banks

def PrintConfig(SYS):
    '''
    Prints the configuration of a system
    '''
    
    print('System:')
    print('\tNodes: {}'.format(SYS.nodes))
    print('\tSockets: {}'.format(SYS.sockets))
    print('\tMCs: {}'.format(SYS.MCs))

def PrintMC(MC):
    '''
    Prints the configuration of the MC
    '''

    print('MC:')
    print('\tChannels: {}'.format(MC.channels))
    print('\tDPC: {}'.format(MC.DPC))
    print('\tRanks: {}'.format(MC.ranks))
    print('\tBGroups: {}'.format(MC.bgroups))
    print('\tBanks: {}'.format(MC.banks))