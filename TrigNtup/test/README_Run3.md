# Running EGRegTreeMaker on Run 3 MiniAOD Samples

## Overview
The EGRegTreeMaker has been updated to work with Run 3 MiniAOD samples. Here's how to run it:

## Prerequisites
1. You're working in CMSSW_13_3_0 (which you already have)
2. The SHarper packages are compiled

## Key Changes for Run 3
The main configuration file `egRegTreeMaker.py` has been updated with:

1. **GlobalTag**: Updated to use appropriate Run 3 GlobalTags:
   - MC: `130X_mcRun3_2023_realistic_postBPix_v2`
   - Data: `130X_dataRun3_Prompt_v4`

2. **Input Tags**: Configured for MiniAOD format:
   - Vertices: `offlineSlimmedPrimaryVertices`
   - Electrons: `slimmedElectrons`
   - Photons: `slimmedPhotons`
   - GenParticles: `prunedGenParticles`
   - ECAL hits: `reducedEgamma:reducedEBRecHits`, `reducedEgamma:reducedEERecHits`

3. **Python 3 compatibility**: Updated print statements

## Running the Ntupliser

### Method 1: Direct cmsRun command
```bash
cmsRun egRegTreeMaker.py \
  inputFiles=/store/mc/Run3Summer22MiniAODv4/DYToLL_M-50_TuneCP5_13p6TeV-pythia8/MINIAODSIM/130X_mcRun3_2022_realistic_v5-v2/2530000/00d7ba86-b64d-4f29-952d-9c7e4cf5ff11.root \
  outputFile=egRegTree_run3.root \
  maxEvents=1000 \
  isMC=True
```

### Method 2: Using the helper script
```bash
python3 run_egRegTreeMaker_run3.py
```
(Edit the script to specify your input files)

### Method 3: Multiple files
```bash
cmsRun egRegTreeMaker.py \
  inputFiles=file1.root,file2.root,file3.root \
  outputFile=egRegTree_run3.root \
  maxEvents=-1 \
  isMC=True
```

## Parameters
- `inputFiles`: Comma-separated list of input MiniAOD files
- `outputFile`: Output ROOT file name
- `maxEvents`: Number of events to process (-1 for all)
- `isMC`: True for MC, False for data (affects GlobalTag selection)

## Example Input Files

### MC Samples (Run 3)
- DY samples: `/store/mc/Run3Summer22MiniAODv4/DYToLL_M-50_TuneCP5_13p6TeV-pythia8/MINIAODSIM/130X_mcRun3_2022_realistic_v5-v2/...`
- TTbar samples: `/store/mc/Run3Summer22MiniAODv4/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2022_realistic_v5-v2/...`

### Data Samples (Run 3)
- EGamma: `/store/data/Run2022C/EGamma/MINIAOD/22Sep2023-v1/...`
- SingleElectron: `/store/data/Run2022C/SingleElectron/MINIAOD/22Sep2023-v1/...`

## Output
The ntupliser produces a ROOT file with TTree containing:
- Electron/photon regression variables
- Supercluster information
- ECAL hits information
- Event-level information
- Generator-level information (for MC)

## Troubleshooting

### Common Issues:
1. **Module not found**: Make sure you've compiled the packages:
   ```bash
   cd $CMSSW_BASE/src
   scram b -j8
   ```

2. **File not found**: Verify the input file path and ensure you have access to the files.

3. **GlobalTag issues**: The GlobalTags are automatically selected based on the `isMC` parameter.

### Checking Available Files:
You can find available Run 3 samples using DAS:
```bash
dasgoclient --query="dataset=/*/Run3*/MINIAOD*"
```

## Building the Package
If you haven't built the packages yet:
```bash
cd $CMSSW_BASE/src
cmsenv
scram b -j8
```

## Notes
- The configuration automatically handles the differences between MC and data
- For Run 3, make sure you're using appropriate Era settings if needed
- The rePFSuperCluster sequence is included for additional supercluster collections
