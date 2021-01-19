import os
import sys
import math
import argparse
import random
import ROOT
import numpy as np

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.modules import *

parser = argparse.ArgumentParser()

parser.add_argument('--process')
parser.add_argument('--input', dest='inputFiles', action='append', default=[])
parser.add_argument('--year', dest='year', action='store', type=int)
parser.add_argument('--maxEntries', '-N', type=int, default=None)
parser.add_argument('output', nargs=1)


args = parser.parse_args()
print(args)



triggers = {
            2016: [
                    '(HLT_IsoMu24 == 1)',
                    '(HLT_IsoTkMu24 == 1)',
                    '(HLT_Ele27_WPTight_Gsf == 1)',


                    '(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL == 1)',
                    '(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL == 1)',
                    '(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL == 1)',
                    '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ == 1)',
                    '(HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL == 1)',
                    '(HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ == 1)'
                   ],

            2017: [
                    '(HLT_IsoMu27 == 1)',
                    '(HLT_Ele32_WPTight_Gsf_L1DoubleEG == 1)',
                    '(HLT_Ele28_eta2p1_WPTight_Gsf_HT150 == 1)',


                    '(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL == 1)',
                    '(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Ele32_WPTight_Gsf == 1)',
                    '(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL == 1)',
                    '(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_IsoMu24_eta2p1 == 1)',
                    '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ == 1)',
                    '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 == 1)'
                   ],

            2018: [
                    '(HLT_IsoMu24 == 1)',
                    '(HLT_Ele32_WPTight_Gsf_v == 1)',
                    '(HLT_Ele28_eta2p1_WPTight_Gsf_HT150 == 1)',


                    '(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL == 1)',
                    '(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Ele32_WPTight_Gsf == 1)',
                    '(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL == 1)',
                    '(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 == 1)',
                    '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 == 1)'
                   ],
          }


cut = ' || '.join(triggers[args.year])



analyzerChain = [
    TH_weights(args.process),
]



runner = PostProcessor(
    args.output[0],
    args.inputFiles,
    postfix='_weights',
    cut=cut,
    modules=analyzerChain,
    friend=False,
    outputbranchsel='processors/keep.txt',
    maxEntries=args.maxEntries,
)


# Run analysis
runner.run()
