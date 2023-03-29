# NDA Study 1887: Structural MRI scans for Autism Subtypes study in BIDS format 

This repository provides data curation scripts and a viewable README for the anatomical imaging dataset shared as [NDA Study 1887](https://nda.nih.gov/study.html?id=1887). The NDA Study 1887 is associated with [NDA Collection 2368](https://nda.nih.gov/edit_collection.html?id=2368), also known as, the Clinical and Immunological Investigations of Subtypes of Autism. 

The study is described in detail in [Raznahan et al. 2013](#references) and [Smith et al. 2016](#references) among other publications. 

We provide a script `bidsify_1887.py` to convert the data downloaded through NDA into a [BIDS](https://bids-specification.readthedocs.io/en/stable/) format dataset. The script is distributed with the NDA Study 1887 data package under `results/` directory and is also available on this repository. Script usage instructions are described [below](#nda-data-package-to-bids-directory). 

## NDA Data Download

**NOTE:** To access the study, you will need permissions to the "NIMH Data Archive" group under `Data Permissions --> Active NDA Permissions`. If you don't see "NIMH Data Archive" listed under "Active NDA Permissions", then you'll have to request it. More information on access requests can be found [here](https://nda.nih.gov/nda/access-data-info.html).

To download data from NDA, the user would have to:
1. Create a data package.
2. Download the data package. 

### Creating a Data Package

Steps below demonstrate creating a data package on [NDA](https://nda.nih.gov)

1. Go to [NDA study 1887 page](https://nda.nih.gov/study.html?id=1887) and click on the `Download` button at the bottom of the page.

    <img src="images/download_1.png">

2. The cart at top right corner should now have 173 subjects. Give it a few seconds to update. Click on `Create Data Package/Add Data to Study` button to see the next prompt.

    <img src="images/download_3.png" width="70%" height="40%">

3. Provide a desired name for the new package. Make sure to check the `Include associated data files` to download NIfTI images along with the metadata. 

    <img src="images/download_5.png">

4. Go back to your account dashboard and click on `Data Packages`. It might take about 15-20 minutes to create the package but once it's ready you should see something like this under data packages list. 

    <img src="images/download_7.png">
    
**NOTE:** As of 2023-03-29, these instructions are valid. However, this might not be the case in future. Please report it as an issue on this repo, if the instructions are not valid any more. 

### Downloading the Data Package

The NDA Study 1887 data package is less than 5 GB in size. It can be downloaded using one of two options:

1. NDA Tools: Download instructions using the command line utility can be found at https://github.com/NDAR/nda-tools#installing-python (Recommended)

2. Instructions to download a data package using *NDA Download Manager* can be found on https://nda.nih.gov/tools/nda-tools.html#download-manager-beta .

Here's a snapshot of the partial directory after the data package has been downloaded:
```bash
study1887
├── README.pdf
├── dataset_collection.txt
├── datastructure_manifest.txt
├── fmriresults01
│   ├── manifests
│   ├── sub-NDARXXXXXXXX
...
│   └── sub-NDARXXXXXXXX
├── fmriresults01.txt
├── md5_values.txt
├── package_info.txt
├── results
│   ├── CHANGES
│   ├── README.md
│   ├── bidsify_1887.py
│   ├── dataset_description.json
│   ├── participants.json
│   ├── participants.tsv
│   ├── scans.json
│   └── scans.tsv
└── study_1887.pdf

```

## NDA Data Package to BIDS Directory 

Here's an example to `copy` over the NIfTI and associated metadata files into a new directory. 

`python3 bidsify_1887.py -i nda-study-1887 -b bids-study-1887 -m copy`

The user can also choose other file mapping methods such as `softlink` and `move` options. The help prompt for script is as follows:
```
$ python bidsify_1887.py -h
usage: bidsify_1887.py [-h] -i INPUT_DIR -b BIDS_DIR -m METHOD

This script generates BIDS formatted directory for NDA Study 1887 downloaded from NDA.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input INPUT_DIR
                        Path to input directory with data downloaded from NDA Study 1887 containing fmriresults01/ and results/ subfolders.
  -b BIDS_DIR, --bids BIDS_DIR, -d BIDS_DIR, --destination BIDS_DIR
                        Path to output the BIDS formatted directory.
  -m METHOD, --method METHOD
                        Choose a method by which you'd like the files mapped: 
                        copy = Outputs copies to the destination BIDS directory. 
                        move = Moves files (without creating a copy) to the destination BIDS directory. 
                        softlink = Create a softlink (a.k.a. symbolic link or symlink) between NDA files and the destination BIDS directory.
```

## Data Preparation Notes
Anatomical imaging data is shared in a minimally processed, raw format. However, in order to facilitate data
analysis, the MRI data are converted to NIfTI and transformed into [BIDS](https://bids-specification.readthedocs.io/en/stable/index.html) format using [Dcm2Bids version
2.1.6](https://github.com/UNFmontreal/Dcm2Bids/releases/tag/2.1.6), which is a wrapper for [dcm2niix version
1.0.20211006](https://github.com/rordenlab/dcm2niix). The
following [modality agnostic files](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#modality-agnostic-files)
have been shared as supporting documentation:

| Filename                   | Description                                                                                            |
|----------------------------|--------------------------------------------------------------------------------------------------------|
| `dataset_description.json` | A JSON file describing the dataset.                                                                    |
| `README`                   | A text file describing the dataset in greater detail.                                                  |
| `CHANGES`                  | A text file with version history of the dataset (describing changes, updates and corrections).         |
| `participants.tsv`         | A tab separated tabular file with additional information like age, sex, and group of each participant. |
| `participants.json`        | A JSON formatted data dictionary describing fields in `participants.tsv`.        |
| `scans.tsv`                | A tab separated tabular file indicating the method used to deface every scan available in the dataset. |
| `scans.json`               | A JSON formatted data dictionary describing fields in `scans.tsv`.                                     |

The structural image types included in the dataset are T1w, T2w, FLAIR, PDw, and MTR. For Magnetization Transfer Ratio (
MTR) images acquired in the presence and absence of an MT pulse have the `mt-on` and `mt-off` entities in their
filenames, respectively.

To preserve subject privacy, MRI scans are defaced
using [AFNI Refacer version 2.4](https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/tutorials/refacer/refacer_run.html).
Defaced scans were visually inspected for quality
using [VisualQC's](https://github.com/raamana/visualqc/tree/0.6.1https://github.com/raamana/visualqc/tree/0.6.1) suite
of QC tools. More details on the defacing workflow used can be
found [here](https://github.com/nih-fmrif/dsst-defacing-pipeline).

8 of the 31 scans that failed first round of QC were manually defaced
using [FSLeyes image editor](https://open.win.ox.ac.uk/pages/fsl/fsleyes/fsleyes/userdoc/editing_images.html) and the remaining 23 of 31 were programmatically corrected to ensure defacing quality. Defacing technique used for each scan in the dataset has been documented in the `scans.tsv` file.

## Code availability

Scripts used for DICOM to BIDS format conversion and de-identification of anatomical MRI scans
are available on the git repository at [https://github.com/nimh-dsst/nda-study-1887](https://github.com/nimh-dsst/nda-study-1887).

## References
1. [Study design of the Clinical and Immunological Investigations of Subtypes of Autism](https://clinicaltrials.gov/ct2/show/NCT00298246)
2. Armin Raznahan, et al., Mapping cortical anatomy in preschool aged children with autism using surface-based morphometry, NeuroImage: Clinical, 2013, https://doi.org/10.1016/j.nicl.2012.10.005.
3. Elizabeth Smith, et al., Cortical thickness change in autism during early childhood, Human Brain Mapping, 2016, https://doi.org/10.1002/hbm.23195 .
4. Other publications related to the study are listed in the [`dataset_description.json`](https://github.com/nimh-dsst/nda-study-1887/blob/12d5a6f3ced98c11133a8054f5a247ac1a766d8b/BIDS_modality_agnostic_files/dataset_description.json#L28) file. 
