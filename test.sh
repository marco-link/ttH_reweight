#!/bin/bash


for p in thq thw tth
do
    python processors/reweight.py --process ${p} --input ${p}.root . -N 3000 --year 2017 |& tee ${p}.log
done

p='thw'
python processors/reweight.py --process ${p} --input ${p}_2016.root . -N 3000 --year 2016 |& tee ${p}.log
python processors/reweight.py --process ${p} --input ${p}_2018.root . -N 3000 --year 2018 |& tee ${p}.log


# samples

# /THW_ctcvcp_HIncl_M125_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM
# /THQ_ctcvcp_HIncl_M125_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM
# ttH currently only NanoAODv4 available!
#
#
# /THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM
# /THQ_ctcvcp_4f_Hincl_13TeV_madgraph_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM
# /TTH_4f_ctcvcp_TuneCP5_13TeV_madgraph_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM
#
#
# /THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM
# /THQ_ctcvcp_4f_Hincl_13TeV_madgraph_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM
# /TTH_4f_ctcvcp_TuneCP5_13TeV_madgraph_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v2/NANOAODSIM
