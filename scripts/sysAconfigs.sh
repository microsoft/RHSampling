#!/bin/bash

echo
echo "Computes the RH failure rates for System A for the DRAMSec paper"
echo

p1=$(echo "1/512" | bc -l)
p2=$(echo "1/256" | bc -l)
p3=$(echo "1/128" | bc -l)
p4=$(echo "1/64" | bc -l)
p5=$(echo "1/32" | bc -l)
p6=$(echo "1/16" | bc -l)

th1=8192
th2=4096
th3=2048
th4=1024

for p in $p1 $p2 $p3 $p4 $p5 $p6
do
    for th in $th1 $th2 $th3 $th4
    do
        echo "python ../RHSampling.py --cfg A --prob $p --th $th --lt 1"
        python ../RHSampling.py --cfg A --prob $p --th $th --lt 1
    done
done
