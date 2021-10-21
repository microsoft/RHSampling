# PARA: Probabilistic Adjacent Row Activation

The code in this repository implements an analysis of PARA, a Rowhammer mitigation. PARA was never formally defined in a paper, 
although informal descriptions were published in the following two papers:

Yoongu Kim, Ross Daly, Jeremie Kim, Chris Fallin, Ji Hye Lee, Donghyuk Lee, Chris Wilkerson, Konrad Lai, and Onur Mutlu\
[Flipping Bits in Memory Without Accessing Them: An Experimental Study of DRAM Disturbance Errors](https://people.inf.ethz.ch/omutlu/pub/dram-row-hammer_isca14.pdf)\
<em>Proceedings of the 41st International Symposium on Computer Architecture (ISCA)</em>, June 2014.

Daehyun Kim, Prashant Nair and Moinuddin K. Qureshi\
[Architectural Support for Mitigating Row Hammering in DRAM MemoriesRefresh Pausing in DRAM Memory Systems](http://memlab.ece.gatech.edu/papers/CAL_2014_1.pdf)\
<em>Computer Architecture Letters (CAL)</em>, Volume 14, pp 9-12, June 2014.

# Technique used for PARA Analysis

PARA.py computes the probability of a RowHammer failure of a DRAM with a given MAC in a window of W row activations, 
given a sampling rate p.

A complete description of our analysis is TBD, but start by reading the code in PARA.py. We made an attempt to document it.

# Usage

To run the script, do:

```sh
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python PARA.py -h
```

When done, do:
```sh
deactivate
```