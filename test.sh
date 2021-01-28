#!/bin/bash


python2 processors/reweight.py --process thw  --year 2018 -i test/thw.root -N 1000 |& tee crab_test.log
