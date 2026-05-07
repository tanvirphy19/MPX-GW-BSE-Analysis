# GW Gap Analysis from VASP OUTCAR

## Overview

This workflow provides an automated procedure for extracting direct and indirect quasiparticle band gaps from GW calculations performed using VASP.

The script parses quasiparticle energies directly from the `OUTCAR` file and automatically determines:

* indirect quasiparticle band gap,
* minimum direct quasiparticle band gap,
* valence-band maximum (VBM),
* conduction-band minimum (CBM),
* corresponding k-point locations.

The workflow was developed for comparative analysis of quasiparticle electronic structures in low-dimensional materials.

---

## Motivation

In GW calculations, both indirect and direct quasiparticle band gaps are important for understanding electronic and optical properties. While the indirect gap governs carrier transport behavior, the optical response is typically dominated by the minimum direct transition.

Manual extraction of k-point-resolved direct gaps from large VASP `OUTCAR` files can be time-consuming and error-prone. This workflow automates the extraction process and provides a consistent analysis across multiple materials.

---

## Method Summary

The workflow performs the following steps automatically:

1. Reads the `OUTCAR` file generated from VASP GW calculations.

2. Detects valid k-points in reciprocal space.

3. Parses quasiparticle energies and occupation numbers from the GW band tables.

4. Identifies:

   * local valence-band maximum (VBM),
   * local conduction-band minimum (CBM),
   * direct gap at each k-point.

5. Determines:

   * global VBM,
   * global CBM,
   * indirect quasiparticle band gap,
   * minimum direct quasiparticle band gap.

6. Reports the corresponding k-point locations for all extracted quantities.

The workflow avoids duplicate k-point entries and ignores invalid reciprocal-space coordinates outside the first Brillouin zone.

---

## Input File

The script requires:

```text
OUTCAR
```

This file must be generated from GW calculations performed using VASP.

The script parses:

* quasiparticle energies,
* occupation numbers,
* k-point coordinates,

directly from the GW band information written in the `OUTCAR` file. 

---

## Requirements

Python packages required:

```bash
numpy
```

Install using:

```bash
pip install numpy
```

---

## Usage

Place the script in the same directory as `OUTCAR`, then run:

```bash
python gw_gap.py
```

---

## Output

The script generates:

### 1. Terminal output

The following quantities are printed:

* direct gap at each k-point,
* minimum direct quasiparticle gap,
* indirect quasiparticle gap,
* VBM and CBM locations,
* gap type (direct or indirect).

---

### 2. Output file

```text
GW_results.dat
```

Contains:

* direct gaps for all valid k-points,
* minimum direct gap,
* indirect gap,
* VBM/CBM energies,
* corresponding k-point coordinates.

---

## Example Systems

Example datasets and outputs are provided for:

* ZrPCl
* ZrPBr
* HfPCl
* HfPBr

These examples demonstrate the applicability of the workflow to systems exhibiting indirect quasiparticle band gaps and k-dependent direct transitions.

---

## Notes

The workflow was developed for GW calculations performed using VASP. The present implementation assumes the standard GW quasiparticle band information written in the `OUTCAR` file.

Minor modifications may be required for:

* different VASP versions,
* modified OUTCAR formatting,
* spin-polarized calculations,
* spin–orbit coupled calculations with different output structures.

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
