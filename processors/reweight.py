import os
import sys
import argparse
#import ROOT

from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.modules import *

parser = argparse.ArgumentParser()

parser.add_argument('--process')
parser.add_argument("-i", "--input", dest="inputfile", type=str, default=None, help="path to input file")
parser.add_argument('--year', dest='year', action='store', type=int)
parser.add_argument('--maxEntries', '-N', type=int, default=None)
parser.add_argument('--crab', action='store_true')
parser.add_argument('--output', type=str, default='weights.root')


args = parser.parse_args()
print(args)

the_inputfiles = None
keep = None
if args.crab:
    the_inputfiles = inputFiles()
    keep = './keep.txt'
else:
    the_inputfiles = [args.inputfile]
    keep = 'processors/keep.txt'

print('Inputfiles: ', the_inputfiles)



triggers = {
            2016: [
                    '(HLT_IsoMu24 == 1)',
                    '(HLT_IsoTkMu24 == 1)',
                    '(HLT_Ele27_WPTight_Gsf == 1)',


                    '(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL == 1)',
                    #'(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL == 1)',
                    #'(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL == 1)',
                    #'(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ == 1)',
                    '(HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL == 1)',
                    #'(HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ == 1)',


                    '(HLT_PFHT450_SixJet40_BTagCSV_p056 == 1)',
                    '(HLT_PFHT400_SixJet30_DoubleBTagCSV_p056 == 1)',
                    '(HLT_PFJet450 == 1)',
                   ],

            2017: [
                    '(HLT_IsoMu27 == 1)',
                    '(HLT_Ele32_WPTight_Gsf_L1DoubleEG == 1)',
                    '(HLT_Ele28_eta2p1_WPTight_Gsf_HT150 == 1)',


                    '(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL == 1)',
                    '(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    #'(HLT_Ele32_WPTight_Gsf == 1)',
                    '(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL == 1)',
                    '(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    #'(HLT_IsoMu24_eta2p1 == 1)',
                    '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ == 1)',
                    '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 == 1)',


                    '(HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 == 1)',
                    '(HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2 == 1)',
                    '(HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0 == 1)',
                    '(HLT_PFHT1050 == 1)',
                   ],

            2018: [
                    '(HLT_IsoMu24 == 1)',
                    '(HLT_Ele32_WPTight_Gsf == 1)',
                    '(HLT_Ele28_eta2p1_WPTight_Gsf_HT150 == 1)',


                    '(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL == 1)',
                    '(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Ele32_WPTight_Gsf == 1)',
                    '(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL == 1)',
                    '(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    '(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ == 1)',
                    #'(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 == 1)',
                    '(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 == 1)',


                    '(HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59 == 1)',
                    '(HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94 == 1)',
                    '(HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5 == 1)',
                    '(HLT_PFHT1050 == 1)',
                   ],
          }


triggercuts = ' || '.join(triggers[args.year])



analyzerChain = [
    TH_weights(args.process),
]






runner = PostProcessor(
    '.',
    the_inputfiles,
    postfix='_weights',
    cut=triggercuts,
    modules=analyzerChain,
    friend=False,
    outputbranchsel=keep,
    maxEntries=args.maxEntries,
    provenance = args.crab,
    fwkJobReport = args.crab,
    haddFileName=args.output
)


# Run analysis
runner.run()
