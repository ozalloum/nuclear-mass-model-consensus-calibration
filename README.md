# Nuclear-mass model consensus calibration
## Current corrected package — v1.1.0

**[Open the corrected v1.1.0 release](https://github.com/ozalloum/nuclear-mass-model-consensus-calibration/releases/tag/v1.1.0)**

[Download the complete corrected package (ZIP)](https://github.com/ozalloum/nuclear-mass-model-consensus-calibration/releases/download/v1.1.0/JPhysG_106072_Reproducibility_v1.1.0.zip)

For the current manuscript, numerical supplement, analysis code, scientific data,
figures and verification records, use the v1.1.0 package linked above.

After extracting the ZIP, start with `public_release/README.md`.

The root-level directories described below are retained as the historical baseline.
The original Git history and v1.0.0 release remain available for provenance.

---
Minimal reproducibility repository for the chronology-locked evaluation of
uncertainty calibration in the FRDM2012, HFB-27, DZ31, and WS4 global
nuclear-mass models.

AME2012-to-AME2016 defines the development sample and freezes the analysis.
AME2016-to-AME2020 supplies the locked confirmation sample. The reported
confirmation set contains 51 nuclei, with Spearman rho = 0.2648 between model
spread and later absolute error, FC-A = 0/51, FC-B = 2/51, and consensus
mass-excess MAE = 0.24695 MeV. For 34 measured-neighbor two-neutron separation
energies, the consensus MAE is 0.12595 MeV.

## Contents

- `code/`: analysis, figure generation, and verification scripts
- `data/processed/`: chronology-defined AME targets and processed AME data
- `data/standardized_models/`: four standardized model tables used in scoring
- `frozen_protocol/`: registered protocol and implementation amendment
- `stage2a_development/` and `stage2b_confirmation/`: locked scored datasets
- `tables/` and `figures/`: reported numerical and graphical outputs

## Reproduce

```bash
python -m pip install -r requirements.txt
python code/reproduce_repository.py
```

The command regenerates the tables and figures reported in the manuscript from
the locked scored data and verifies the headline results.

## Data provenance

Atomic-mass chronology is based on AME2012, AME2016, and AME2020. Model inputs
are FRDM2012 and WS4 from IAEA RIPL-4, HFB-27 from BRUSLIB, and DZ31 from the
official AMDC 31-parameter program. Consult the frozen protocol for eligibility,
standardization, and confirmation-lock rules.
