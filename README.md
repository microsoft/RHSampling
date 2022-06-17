# How to Configure Row-Sampling-Based Rowhammer Defenses

The code in this repository implements an analysis of Row-Sampling, a class of Rowhammer defenses. 
This analysis is based on formulae presented in the following DRAMSec 2022 paper:

Stefan Saroiu and Alec Wolman\
[How to Configure Row-Sampled-Based Rowhammer Defenses](https://stefan.t8k2.com/publications/dramsec/2022/rhsampling.pdf)\
<em>Proceedings of the 2nd Workshop on DRAM Security</em>, June 2022.

# Quick Background

Row-Sampling-based Rowhammer defenses are one of the oldest and simplest classes of defense
techniques suitable for a memory controller. On each row activate, the memory
controller flips a biased coin. With a low probability $p$ ($p\ll1$), the row
address is *sampled* and the row is treated as if it is an aggressor row.
The memory controller performs a mitigative action such as refreshing the
corresponding victim rows. A sufficiently high sampling rate $p$ thwarts a Rowhammer
attack because it ensures that an aggressor row cannot escape being sampled with
very high probability.  Some of the earliest papers on Rowhammer introduced variants
of sampling-based defenses under the names of ``Probabilistic Adjacent Row Activation (PARA)``
and ``Probabilistic Row Activation (PRA)``.

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

# Notes

## Dual formula

We implemented two ways to derive the Row-Sampling configuration. The way described in the DRAMSec paper, and also a dual way. The dual computes the probability of no Rowhammer failure (recursively) by counting all possible cases when at least one of the row activations in an attack is sampled. The dual formula is a more complex recursion because enumerating all possibility of no Rowhammer failures requires more distinct cases. As a result, it is also much slower.  

The dual should be used only for testing purposes. Both ways produce the same results.

## Testing

Each script other than main one (``RHSampling.py``) comes with a few tests implemented in the main body of the script. Simply run the script to run the tests. For example:

```sh
python ConsecutiveUnsampledACTs.py
```

## Examples

Table V in the workshop paper shows that a sampling rate of 1 in 256 has a Rowhammer failure of 7e-6 for a threshold of 8192. To see this result, run:

```sh
python RHSampling.py --th 8192 --rate 0.00390625 --cfg A 
```

The scripts directory has a couple of scripts to produce the numbers presented in our paper.

## On Precision

 Given the nature of the computations above, the results are always inexact and rounded. However, the code uses the decimal module that supports arbitrary levels of precision. You can always increase the precision of the computation (the default is '100') and check whether the result changes (see the ``--prec`` flag).

 In my experience with different parameters and configurations, the script can sometimes return a failure rate of '0E+00' or '1E+00'. This is an indication of an inadequate level of precision (the rowhammer failure rate can never 0% or 100%). In these cases, increase the precision and re-run the script until the failure rate changes either to a value very close to 0 or very close to 1.  