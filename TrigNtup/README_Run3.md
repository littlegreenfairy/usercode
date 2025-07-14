# Running EGRegTreeMaker on MiniAOD Samples

## Overview
The EGRegTreeMaker has been updated to work with Run 3 MiniAOD samples. Here's how to run it:

## Prerequisites
1. You're working in CMSSW_13_3_0 
2. The branch 133XforMiniAOD from Sam Harper's 'SHarper' repository with the usercode has been cloned inside CMSSW_13_3_0/src 

## Building the Package
To compile all the Package in SHarper usercode repo:
```bash
cd $CMSSW_BASE/src
cmsenv
scram b -j8
```

## Key Changes with respect to branch 133X
The main ntuplizer script `test/egRegTreeMaker.py` has been updated with:

1. **isMiniAOD flag**: to choose whether to run on MiniAODSIM or on AODSIM. On this branch it is set to `True` by default.

2. **GlobalTag**: Updated to use appropriate Run 3 GlobalTags:
   - MC: `130X_mcRun3_2023_realistic_postBPix_v2`
   - Data: `130X_dataRun3_Prompt_v4`

3. **Input Tags**: Configured for MiniAOD format:
   - Vertices: `offlineSlimmedPrimaryVertices`
   - Electrons: `slimmedElectrons`
   - Photons: `slimmedPhotons`
   - GenParticles: `prunedGenParticles`
   - ECAL hits: `reducedEgamma:reducedEBRecHits`, `reducedEgamma:reducedEERecHits`

4. **Python 3 compatibility**: Updated print statements

## Running the Ntupliser

The Ntuplizer needed for egRegTree regression ntuples is `test/egRegTreeMaker.py`. You can run it in several ways:

### Method 1: Direct cmsRun command on local file
```bash
cmsRun egRegTreeMaker.py \
  inputFiles=file:/eos/cms/store/group/phys_egamma/soffi/4Elena/9cb4c438-4ddc-4068-85d4-499780df0dc0.root \
  outputFile=egRegTree_run3.root \
  maxEvents=1000 \
  isMC=True
```

### Method 2: Multiple files
```bash
cmsRun egRegTreeMaker.py \
  inputFiles=file1.root,file2.root,file3.root \
  outputFile=egRegTree_run3.root \
  maxEvents=-1 \
  isMC=True
```
### Method 3: Using CRAB

## Parameters
- `inputFiles`: Comma-separated list of input MiniAOD files
- `outputFile`: Output ROOT file name
- `maxEvents`: Number of events to process (-1 for all)
- `isMC`: True for MC, False for data (affects GlobalTag selection)

## Example Input Files

### MC Samples (Run 3)
- 2022 flat pt sample for Run 3 regression training: `/eos/cms/store/group/phys_egamma/soffi/4Elena/9cb4c438-4ddc-4068-85d4-499780df0dc0.root`


## Output
The ntupliser produces a ROOT file with TTree containing:
- Electron/photon regression variables
- Supercluster information
- ECAL hits information
- Event-level information
- Generator-level information (for MC)


