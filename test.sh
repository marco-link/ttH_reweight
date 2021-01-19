#!/bin/bash


for p in thq thw tth
do
    python processors/reweight.py --process ${p} --input ${p}.root . -N 3000 --year 2017 |& tee ${p}.log
done


