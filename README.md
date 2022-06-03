# How to Configure Row-Sampling-Based Rowhammer Defenses

The code in this repository implements an analysis of Row-Sampling, a class of Rowhammer defenses. This analysis is 
based on formulae presented in the following DRAMSec 2022 paper:

Stefan Saroiu and Alec Wolman\
[How to Configure Row-Sampled-Based Rowhammer Defenses](https://stefan.t8k2.com/publications/dramsec/2022/rhsampling.pdf)\
<em>Proceedings of the 2nd Workshop on DRAM Security</em>, June 2022.

# Quick Background

Row-Sampling-based Rowhammer defenses are one of the oldest and simplest classes of defense
techniques suitable for a memory controller. On each row activate, the memory
controller flips a biased coin. With a low probability $p$ ($p\ll1$), the row
address is \emph{sampled} and the row is treated as if it is an aggressor row.
The memory controller performs a mitigative action such as refreshing the
corresponding victim rows. A sufficiently high sampling rate $p$ thwarts a \rh
attack because it ensures that an aggressor row cannot escape being sampled with
very high probability.  Some of the earliest papers on \rh introduced variants
of sampling-based defenses under the names of ``Probabilistic Adjacent Row
Activation'' (PARA)'' and ``Probabilistic Row
Activation'' (PRA).

Yoongu Kim, Ross Daly, Jeremie Kim, Chris Fallin, Ji Hye Lee, Donghyuk Lee, Chris Wilkerson, Konrad Lai, and Onur Mutlu\
[Flipping Bits in Memory Without Accessing Them: An Experimental Study of DRAM Disturbance Errors](https://people.inf.ethz.ch/omutlu/pub/dram-row-hammer_isca14.pdf)\
<em>Proceedings of the 41st International Symposium on Computer Architecture (ISCA)</em>, June 2014.

Daehyun Kim, Prashant Nair and Moinuddin K. Qureshi\
[Architectural Support for Mitigating Row Hammering in DRAM MemoriesRefresh Pausing in DRAM Memory Systems](http://memlab.ce.gatech.edu/papers/CAL_2014_1.pdf)\
<em>Computer Architecture Letters (CAL)</em>, Volume 14, pp 9-12, June 2014.

# Usage

To run the script, do:

```sh
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python RHSampling.py -h
```

When done, do:
```sh
deactivate
```