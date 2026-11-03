# How informative is agreement among nuclear-mass models? Chronology-respecting tests of error coverage and shell proximity

## Current GSM revision â€” v1.2.1

**[Open the current v1.2.1 release](https://github.com/ozalloum/nuclear-mass-models/releases/tag/v1.2.1)**

[Download the complete scientific package (ZIP)](https://github.com/ozalloum/nuclear-mass-models/releases/download/v1.2.1/JPhysG_106072_Reproducibility_v1.2.1.zip)

**How informative is agreement among nuclear-mass models? Chronology-respecting tests of error coverage and shell proximity** â€” JPhysG-106072

The complete scientific source/code/data tree is in the versioned ZIP. The standalone manuscript, numerical supplement, Figure 7 and GSM CSV are provided for direct access.

The current package includes the manuscript, numerical supplement, all 15 audited vector-digitized GSM values from Li et al. Figure 2(b), the two separate core series, matched-isotope comparisons, extraction sensitivity, the current Figure 7, and the complete scientific reproduction materials.

- Start here: download the current ZIP and open `public_release/README.md`.
- [Current manuscript](JPhysG_106072_Revised_v1.2.1.pdf)
- [Current numerical supplement](JPhysG_106072_Supplement_v1.2.1.pdf)
- [Digitized GSM values (CSV)](Li2020_Fig2b_GSM_digitized.csv)
- [Figure 7](Figure7_Calcium_S2n_v1.2.1.pdf)
- [GSM protocol amendment](GSM_PROTOCOL_AMENDMENT.txt)

Figure 7 uses identical linear scales in both panels: A=48â€“60 with steps of 2, and S2n=0â€“20 MeV with steps of 2.5 MeV. The current rendering places the legends inside the upper-right corner of panels (a) and (b). Values beyond A=60 are retained in Supplement S7. GSM is a regional comparator; the four-model ensemble and the primary and broad mass-cohort results are unchanged.

The original Fortran source, verification bundle and run report are retained. The missing original raw DZ31 output has been restored and verified. The numerical GSM values and frozen scientific inputs are unchanged.

The manuscript and supplement include the wording and notation refinements reviewed on 3 November 2026. The ten-step numerical reproduction passed, and 1,225 printed values across all 14 supplement tables were independently checked. See [release notes](RELEASE_NOTES_v1.2.1.md).

## Reproduce the current version

Download and extract `JPhysG_106072_Reproducibility_v1.2.1.zip` first.

```bash
cd public_release
python -m pip install -r requirements.review-tested.txt
python reproduce_review_package.py --verify-only
python reproduce_review_package.py --output ../JPhysG_106072_reproduction
```

The tested review environment used Python 3.13.9 and `requirements.review-tested.txt`; the original dependency pins are retained separately. The output directory must be new. The full pipeline compares 43 CSVs and preserves 19 frozen input files. Optional fresh Fortran compilation and source-PDF checks are explained in the package README.

## Earlier versions

The v1.1.0 release predates the numerical GSM addition. Earlier tags remain historical snapshots. Root-level historical directories are retained for provenance; use `public_release/` inside the v1.2.1 ZIP for the current manuscript and analysis.

The manuscript and README document the revision-stage data-source amendment, figure-derived status of GSM, retrospective comparison, and remaining provenance and extrapolation limitations.

The named release ZIP is the current scientific package. Automatic source-code downloads for the original v1.2.1 tag remain historical snapshots. Reviewer correspondence and cover letters remain in the separate submission package.
