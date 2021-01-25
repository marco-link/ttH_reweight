#
# use 'python <file.py>' instead of 'crab submit <file.py>'!
#


# this will use CRAB client API
from CRABAPI.RawCommand import crabCommand

from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromCRIC


import os

years = [2016, 2017, 2018]


samples = {
    '2016':
        [
        '/THW_ctcvcp_HIncl_M125_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        #'/THQ_ctcvcp_HIncl_M125_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        ###'/ttH_4f_ctcvcp_TuneCP5_13TeV_madgraph_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        ],
    '2017':
        [
        #'/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        #'/THQ_ctcvcp_4f_Hincl_13TeV_madgraph_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        ###'/TTH_4f_ctcvcp_TuneCP5_13TeV_madgraph_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        ],
    '2018':
        [
        #'/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        #'/THQ_ctcvcp_4f_Hincl_13TeV_madgraph_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        ###'/TTH_4f_ctcvcp_TuneCP5_13TeV_madgraph_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v2/NANOAODSIM',
        ]
    }




for year in years:
    config = Configuration()

    config.section_("General")
    config.General.workArea = 'crab_{}'.format(year)
    config.General.transferOutputs = True


    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'PSet.py'
    config.JobType.scriptExe = 'crab_script.sh'
    config.JobType.inputFiles = ['../processors', '../ident_card.dat']
    config.JobType.sendPythonFolder = True
    config.JobType.maxMemoryMB = 2500
    #config.JobType.numCores = 1
    #config.JobType.sendExternalFolder = True


    config.section_("Data")
    config.Data.inputDBS = 'global'
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = 1
    config.Data.publication = False
    config.Data.outLFNDirBase = '/store/user/mlink/ttH_reweight_{}/v1/'.format(year)
    ##config.Data.totalUnits = 2
    #config.Data.publishDbsUrl = 'phys03'
    #config.Data.outputDatasetTag = 'Analysis_NanoAOD'


    config.section_("Site")
    config.Site.storageSite = 'T1_DE_KIT_Disk'
    #config.Site.blacklist = ['T2_US_*']


    config.section_("User")
    config.User.voGroup = 'dcms'
    config.JobType.outputFiles = ['weights.root']







    for sample in samples[str(year)]:
        process = None
        if 'THW' in sample.upper():
            process = 'thw'
        if 'THQ' in sample.upper():
            process = 'thq'

        if process == None:
            print('process for "{}" not found!'.format(sample))
            continue

        requestName = sample.split('/')[1]

        config.General.requestName = requestName
        config.Data.inputDataset = sample
        config.JobType.scriptArgs = ['process={}'.format(process), 'year={}'.format(year)]

        # save config
        with open('{}_{}.py'.format(year, requestName), 'w') as f:
            print >> f, config


        logpath = 'crab_{y}/crab_{proc}'.format(y=year, proc=requestName)
        if os.path.isdir(logpath):
            print('Already submitted (see "{}"). Skipping!'.format(logpath))
        else:
            print('submitting {} ...'.format(requestName))
            result = crabCommand('submit', config = config)
            print (result)
