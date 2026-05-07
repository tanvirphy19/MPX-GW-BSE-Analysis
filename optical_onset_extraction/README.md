# Optical Onset Extraction from BSE Spectra

## Overview

This workflow provides an automated procedure for extracting onset-based optical gaps and first bright excitonic peaks from broadened Bethe–Salpeter equation (BSE) absorption spectra.

The method was developed for comparative optical analysis of low-dimensional materials calculated using first-principles many-body perturbation theory within the GW-BSE framework using VASP.

The workflow is particularly useful for:

* materials exhibiting weak or broadened excitonic features,
* indirect-gap systems,
* comparative studies involving multiple compounds.

---

## Motivation

Optical gaps obtained from BSE spectra are commonly estimated from the first bright excitonic peak. However, in many systems, especially those exhibiting weak or broadened low-energy excitonic features, the first peak may not consistently represent the optical absorption edge.

To ensure a consistent comparison across multiple materials, this workflow extracts the optical onset from the low-energy region of the broadened BSE absorption spectrum using an automated linear-fitting procedure. The first bright excitonic peak is additionally reported as a complementary descriptor of the optical excitation behavior.

---

## Method Summary

The workflow performs the following steps automatically:

1. Reads the `ABSORPTION.dat` file generated from BSE post-processing using VASPKIT.

2. Extracts the in-plane absorption spectrum using:

```text
(XX + YY)/2
```

3. Applies slight Gaussian smoothing to reduce numerical noise.

4. Detects the first bright excitonic peak from the first local maximum in the spectrum.

5. Identifies the low-energy onset region using a fixed intensity threshold relative to the maximum absorption.

6. Restricts the fitting region to energies preceding the first peak to avoid higher-energy continuum features.

7. Performs automated linear fitting over moving windows.

8. Selects the optimal fitting region according to the highest coefficient of determination (`R^2`).

9. Determines the optical onset energy from the intercept of the fitted line with the energy axis.

The same fitting parameters and extraction criteria should be consistently applied to all materials within a comparative study.

---

## Input File

The script requires:

```text
ABSORPTION.dat
```

This file is obtained from BSE optical calculations post-processed using VASPKIT.

Expected columns:

```text
Energy   XX   YY   ZZ   XY   YZ   XZ
```

Only the in-plane components (`XX` and `YY`) are used in the present workflow.

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

## Usage

Place the script in the same directory as `ABSORPTION.dat`, then run:

```bash
python optical_onset.py
```

---

## Output

The script generates:

### 1. Optical onset results

```text
output/optical_gap_results.dat
```

Contains:

* optical onset energy,
* first bright excitonic peak,
* fitting quality (`R^2`),
* maximum absorption intensity.

---

### 2. Verification figure

```text
optical_gap_plot.png
```

and

```text
output/optical_gap_plot.png
```

The figure includes:

* BSE absorption spectrum,
* optimal linear fitting region,
* extracted optical onset,
* first bright excitonic peak.

---

## Example Systems

Example datasets and outputs are provided for:

* ZrPCl
* ZrPBr
* HfPCl
* HfPBr

These examples demonstrate the applicability of the workflow to systems exhibiting different excitonic behaviors.

---

## Notes for Bulk Materials

The present workflow was primarily designed for 2D systems using the in-plane optical spectrum. For bulk materials, minor modifications may be required depending on:

* crystal symmetry,
* optical anisotropy,
* choice of dielectric tensor components.

Users may adapt the optical component selection accordingly.

---

## Citation

If you use this workflow in published work, please cite the associated article and repository DOI.

```text
DOI: [To be added after Zenodo deposition]
```

---

## Author

Md. Tanvir Ahmed
TEAMS Lab
Department of Physics
Pabna University of Science and Technology, Pabna-6600, BD
