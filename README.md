# Nuclear-mass model consensus calibration

## Current GSM revision — v1.2.0

**[Open the current v1.2.0 release](https://github.com/ozalloum/nuclear-mass-model-consensus-calibration/releases/tag/v1.2.0)**

[Download the complete scientific package (ZIP)](https://github.com/ozalloum/nuclear-mass-model-consensus-calibration/releases/download/v1.2.0/JPhysG_106072_Reproducibility_v1.2.0.zip)

**How informative is agreement among nuclear-mass models? Chronology-respecting
tests of error coverage and shell proximity** — JPhysG-106072

The complete source/code/data tree is in the versioned ZIP; the manuscript,
supplement, Figure 7 and GSM CSV are also available directly below.

The current package includes the manuscript, numerical supplement, all 15 audited
vector-digitized GSM values from Li et al. Figure 2(b), the two separate core
series, matched-isotope comparisons, extraction sensitivity, Figure 7 and the
complete scientific reproduction materials.

- Start here: download the current ZIP and open `public_release/README.md`.
- [Current manuscript](JPhysG_106072_Revised_v1.2.0.pdf)
- [Current numerical supplement](JPhysG_106072_Supplement_v1.2.0.pdf)
- [Digitized GSM values (CSV)](Li2020_Fig2b_GSM_digitized.csv)
- [Figure 7](Figure7_Calcium_S2n_v1.2.0.pdf)
- [GSM protocol amendment](GSM_PROTOCOL_AMENDMENT_2026-11-02.txt)

Figure 7 uses identical linear scales in both panels: A=48–60 with steps of 2,
and S2n=0–20 MeV with steps of 2.5 MeV. Values beyond A=60 are retained in
Supplement S7. GSM is a regional comparator; the four-model ensemble and the
primary and broad mass-cohort results are unchanged. The original Fortran source,
verification bundle, run report and raw output remain included.

## Reproduce the current version

Download and extract `JPhysG_106072_Reproducibility_v1.2.0.zip` first.

```bash
cd public_release
python -m pip install -r requirements.txt
python reproduce_review_package.py --verify-only
python reproduce_review_package.py --output ../JPhysG_106072_reproduction
```

The output directory must be new. The full pipeline compares 43 CSVs and preserves
19 frozen input files. Optional fresh Fortran compilation and source-PDF checks
are explained in the current package README.

## Earlier versions

The [v1.1.0 release](https://github.com/ozalloum/nuclear-mass-model-consensus-calibration/releases/tag/v1.1.0)
predates the numerical GSM addition. The original v1.0.0 release and Git history
remain available. Root-level `code/`, `data/`, `figures/`, `tables/`,
`frozen_protocol/` and `stage2*` directories are the historical baseline;
**use `public_release/` inside the v1.2.0 ZIP for the current manuscript and analysis**.

The manuscript and README document the revision-stage data-source amendment,
figure-derived status of GSM, retrospective comparison, and remaining provenance
and extrapolation limitations.
