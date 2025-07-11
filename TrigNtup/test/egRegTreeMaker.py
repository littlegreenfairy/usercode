isCrabJob=False #script seds this if its a crab job

# Import configurations
import FWCore.ParameterSet.Config as cms
import os
import sys
# set up process
from Configuration.Eras.Era_Run3_cff import Run3
process = cms.Process("HEEP",Run3)

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('analysis') 
options.register('isMiniAOD',True,options.multiplicity.singleton,options.varType.bool," whether we are running on miniAOD or not")
options.register('isMC',True,options.multiplicity.singleton,options.varType.bool," whether we are running on MC or not")
options.register('datasetCode',1,options.multiplicity.singleton,options.varType.int," datasetcode")
options.register('datasetName',"",options.multiplicity.singleton,options.varType.string," datasetName")
options.parseArguments()

print(options.inputFiles)
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(options.inputFiles),  
                          )

if isCrabJob:
    datasetCode=DATASETCODE
else:
    datasetCode=options.datasetCode

if datasetCode==0: isMC=False
else: isMC=True

datasetVersion="TOSED:DATASETVERSION"

print("isCrab = ",isCrabJob,"isMC = ",isMC," datasetCode = ",datasetCode," useMiniAOD = ",options.isMiniAOD,"datasetVersion = ",datasetVersion)


# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(5000),
    limit = cms.untracked.int32(10000000)
)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

#Load geometry
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.autoCond import autoCond
from Configuration.AlCa.GlobalTag import GlobalTag
if isMC:
    # Change from Run 2 global tag to Run 3
    process.GlobalTag = GlobalTag(process.GlobalTag, '130X_mcRun3_2022_realistic_v5', '')  # Run 3 MC
else:
    process.GlobalTag = GlobalTag(process.GlobalTag, '130X_dataRun3_PromptAnalysis_v1','')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')


process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Geometry.CaloEventSetup.CaloTowerConstituents_cfi")
process.load("Configuration.StandardSequences.Services_cff")

# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.outputFile)
)

def swapEGRegToMiniAOD(egRegPara):
    """Swap EGRegTreeMaker input tags from AOD to MiniAOD format"""
    egRegPara.usePatCollections = cms.bool(True)
    egRegPara.verticesTag = cms.InputTag("offlineSlimmedPrimaryVertices")
    egRegPara.genPartsTag = cms.InputTag("prunedGenParticles")
    egRegPara.puSumTag = cms.InputTag("slimmedAddPileupInfo")
    egRegPara.ecalHitsEBTag = cms.InputTag("reducedEgamma","reducedEBRecHits")
    egRegPara.ecalHitsEETag = cms.InputTag("reducedEgamma","reducedEERecHits")
    egRegPara.elesTag = cms.InputTag("slimmedElectrons")
    egRegPara.phosTag = cms.InputTag("slimmedPhotons")
    # For MiniAOD, SuperClusters are in reducedEgamma
    egRegPara.scTag = cms.VInputTag("reducedEgamma:reducedSuperClusters")
    egRegPara.scAltTag = cms.VInputTag()  # Not available in MiniAOD
    egRegPara.rhoTag = cms.InputTag("fixedGridRhoFastjetAll")

process.egRegTreeMaker = cms.EDAnalyzer("EGRegTreeMaker",
                                        verticesTag = cms.InputTag("offlinePrimaryVertices"),
                                        rhoTag = cms.InputTag("fixedGridRhoFastjetAllTmp"),
                                        genPartsTag = cms.InputTag("genParticles"),
                                        puSumTag = cms.InputTag("addPileupInfo"),
                                        scTag = cms.VInputTag("particleFlowSuperClusterECAL:particleFlowSuperClusterECALBarrel","particleFlowSuperClusterECAL:particleFlowSuperClusterECALEndcapWithPreshower"),
                                        scAltTag = cms.VInputTag("particleFlowSuperClusterECALNoThres:particleFlowSuperClusterECALBarrel","particleFlowSuperClusterECALNoThres:particleFlowSuperClusterECALEndcapWithPreshower"),
                                        ecalHitsEBTag = cms.InputTag("reducedEcalRecHitsEB"),
                                        ecalHitsEETag = cms.InputTag("reducedEcalRecHitsEE"),
                                        elesTag = cms.InputTag("gedGsfElectrons"),
                                        phosTag = cms.InputTag("gedPhotons"),
                                        elesAltTag = cms.VInputTag(),
                                        phosAltTag = cms.VInputTag()
                                        )

# Configure for MiniAOD vs AODSIM
if options.isMiniAOD:
    swapEGRegToMiniAOD(process.egRegTreeMaker)

process.p = cms.Path(process.egRegTreeMaker)
#!!!!
process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('MINIAODSIM'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fileName = cms.untracked.string(options.outputFile.replace(".root","_EDM.root")),
    outputCommands = cms.untracked.vstring('drop *',
                                           "keep *_*_*_HEEP",
                                    )                                           
                                   )
#process.out = cms.EndPath(process.AODSIMoutput)
