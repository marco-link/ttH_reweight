#!/bin/bash


<<<<<<< HEAD
python2 processors/reweight.py --process thw  --year 2017 -i test/thw.root -N 1000 |& tee crab_test.log
=======
python processors/reweight.py --process thw  --year 2017  --crab -N 1000 |& tee crab_test.log


# for p in thq thw
# do
#     python processors/reweight.py --process ${p} --input ${p}.root -N 1000 --year 2017 |& tee ${p}.log
# done

# p='thw'
# python processors/reweight.py --process ${p} --input ${p}_2016.root -N 1000 --year 2016 |& tee ${p}.log
# python processors/reweight.py --process ${p} --input ${p}_2018.root -N 1000 --year 2018 |& tee ${p}.log
>>>>>>> parent of 2a68eca1... fix local test
