# MPX-GW-BSE-Analysis

## Overview

This repository contains post-processing workflows developed for the analysis of quasiparticle and optical properties obtained from first-principles GW and Bethe–Salpeter equation (BSE) calculations performed using VASP.

The repository was developed as part of a comparative study on MPX monolayers and includes automated tools for:

* extraction of direct and indirect GW quasiparticle band gaps,
* determination of k-point-resolved direct gaps,
* extraction of onset-based optical gaps from broadened BSE spectra,
* identification of first bright excitonic peaks.

The workflows are intended for reproducible and consistent analysis of low-dimensional materials exhibiting different excitonic behaviors.

---

## Repository Structure

```text
MPX-GW-BSE-Analysis/
│
├── README.md
├── LICENSE
├── requirements.txt
│
├── optical_onset_extraction/
│   ├── optical_onset.py
│   ├── README.md
│   └── examples/
│
├── gw_gap_analysis/
│   ├── gw_gap.py
│   ├── README.md
│   └── examples/
```

---

## Included Workflows

### 1. GW Gap Analysis

Location:

```text
gw_gap_analysis/
```

This workflow extracts:

* indirect quasiparticle band gap,
* minimum direct quasiparticle band gap,
* valence-band maximum (VBM),
* conduction-band minimum (CBM),
* corresponding k-point locations.

The script parses quasiparticle energies directly from the `OUTCAR` file generated from VASP GW calculations.

---

### 2. Optical Onset Extraction

Location:

```text
optical_onset_extraction/
```

This workflow extracts:

* onset-based optical gap,
* first bright excitonic peak,
* optimal linear fitting region,
* fitting quality (`R^2`).

The analysis is performed using broadened BSE absorption spectra obtained from VASPKIT post-processing.

---

## Motivation

Optical gaps obtained from BSE spectra are often determined using the first bright excitonic peak. However, in systems exhibiting weak or broadened low-energy excitonic features, the first peak may not provide a consistent description of the optical absorption edge across multiple materials.

To address this issue, the present workflow introduces an automated onset-based optical-gap extraction procedure using linear fitting of the low-energy absorption region while additionally reporting the first bright excitonic peak as a complementary descriptor.

---

## Requirements

Python packages required:

```bash
numpy
pandas
matplotlib
scipy
```

Install using:

```bash
pip install numpy pandas matplotlib scipy
```

---

## Example Systems

Example datasets and outputs are provided for:

* ZrPCl
* ZrPBr
* HfPCl
* HfPBr

---

## Code Availability

The workflows provided in this repository were developed for reproducible post-processing analysis of GW and BSE calculations performed using VASP.

If you use these scripts in published work, please cite the associated article and repository DOI.

```text
DOI: [To be added after Zenodo deposition]
```

---

## License

This project is released under the MIT License.

---

## Author

Md. Tanvir Ahmed  
TEAMS Lab  
Department of Physics  
Pabna University of Science and Technology, Pabna-6600, Bangladesh
