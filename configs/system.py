from collections    import namedtuple

HOST = namedtuple('HOST', 'nodes sockets channels DPC')
DRAM = namedtuple('DRAM', 'ranks bgroups banks')

'''
Datacenter of ICX servers: 100K, 2 sockets, 8 channels, 2DPC
Datacenter of ARM servers: 100K, 1 socket, 12 channels, 1DPC

Dual-socket ICX server: 1 node, 2 sockets, 8 channels, 2DPC
ARM server:             1 node, 1 socket, 12 channels, 1DPC

drDDR5: 2 ranks, 8 BGs, 4 BAs
srDDR5: 1 rank, 8 BGs, 4 BAs
'''
icxFLEET    = HOST(100 * 1000, 2, 8, 2)
armFLEET    = HOST(100 * 1000, 1, 12, 1)
icxSRV      = HOST(1, 2, 8, 2)
armSRV      = HOST(1, 1, 12, 1)

drDDR5  = DRAM(2, 8, 4)
srDDR5  = DRAM(1, 8, 4)

'''
Configurations used in the DRAMSec paper
Sys A: dual-socket server with 16 channels (8 channels per socket), 2 DPC, 2 ranks, 8 BGs, 4 BAs
Sys B: single-socket server with 2 channels, 1 DPC, 1 rank, 4 BGs, 4 BAs
'''
hostA = icxSRV
dramA = drDDR5

hostB = HOST(1, 1, 2, 1)
dramB = DRAM(1, 4, 4)

def Banks(HOST, DRAM):
    '''
    Computes the number of banks in a system
    :param HOST: host config (namedtuple)
    :param DRAM: DRAM config (namedtuple)
    :rtype: int
    '''

    return HOST.nodes * HOST.sockets * HOST.channels * HOST.DPC * DRAM.ranks * DRAM.bgroups * DRAM.banks

def PrintConfig(HOST):
    '''
    Prints the configuration of the host
    '''
    
    print('Host:')
    print('  Nodes: {}'.format(HOST.nodes))
    print('  Sockets: {}'.format(HOST.sockets))
    print('  Channels: {}'.format(HOST.channels))
    print('  DPC: {}'.format(HOST.DPC))

def PrintDRAM(DRAM):
    '''
    Prints the configuration of the DRAM
    '''

    print('DRAM:')
    print('  Ranks: {}'.format(DRAM.ranks))
    print('  BGroups: {}'.format(DRAM.bgroups))
    print('  Banks: {}'.format(DRAM.banks))