# How informative is agreement among nuclear-mass models? Chronology-respecting tests of error coverage and shell proximity

## Current revision — v1.2.1 (4 November 2026)

**[Open the current v1.2.1 release](https://github.com/ozalloum/nuclear-mass-models/releases/tag/v1.2.1)**

[Download the complete scientific package (ZIP)](https://github.com/ozalloum/nuclear-mass-models/releases/download/v1.2.1/JPhysG_106072_Reproducibility_v1.2.1.zip)

**How informative is agreement among nuclear-mass models? Chronology-respecting tests of error coverage and shell proximity** — JPhysG-106072

The complete scientific source/code/data tree is in the versioned ZIP. The standalone manuscript, numerical supplement, Figure 7 and GSM CSV are provided for direct access.

The current package includes the manuscript, numerical supplement, all 15 audited vector-digitized GSM values from Li et al. Figure 2(b), the two separate core series, matched-isotope comparisons, extraction sensitivity, the current Figure 7, and the complete scientific reproduction materials.

- Start here: download the current ZIP and open `public_release/README.md`.
- [Current manuscript](JPhysG_106072_Revised_v1.2.1.pdf)
- [Current numerical supplement](JPhysG_106072_Supplement_v1.2.1.pdf)
- [Digitized GSM values (CSV)](Li2020_Fig2b_GSM_digitized.csv)
- [Figure 7](Figure7_Calcium_S2n_v1.2.1.pdf)
- [GSM protocol amendment](GSM_PROTOCOL_AMENDMENT.txt)

Figure 7 uses identical linear scales in both panels: A=48–60 with steps of 2, and S2n=0–20 MeV with steps of 2.5 MeV. The current rendering places the legends inside the upper-right corner of panels (a) and (b). Values beyond A=60 are retained in Supplement S7. GSM is a regional comparator; the four-model ensemble and the primary and broad mass-cohort results are unchanged.

The original Fortran source, verification bundle and run report are retained. The missing original raw DZ31 output has been restored and verified. The numerical GSM values and frozen scientific inputs are unchanged.

The manuscript and supplement include the final Abstract, Conclusion and minor corrections for 4 November 2026. All 1,273 printed numeric values across 15 supplement tables were independently checked. See [release notes](RELEASE_NOTES_v1.2.1.md).

## Reproduce the current version

Download and extract `JPhysG_106072_Reproducibility_v1.2.1.zip` first.

```bash
cd public_release
python -m pip install -r requirements.review-tested.txt
python reproduce_review_package.py --verify-only
python reproduce_review_package.py --output ../JPhysG_106072_reproduction
```

The tested review environment used Python 3.13.9 and `requirements.review-tested.txt`; the original dependency pins are retained separately. The output directory must be new. The full pipeline compares the 43 original scientific CSVs plus the new event-frequency CSV and preserves 19 frozen input files. Optional fresh Fortran compilation and source-PDF checks are explained in the package README.

## Earlier versions

The v1.1.0 release predates the numerical GSM addition. Earlier tags remain historical snapshots. Root-level historical directories are retained for provenance; use `public_release/` inside the v1.2.1 ZIP for the current manuscript and analysis.

The manuscript and README document the revision-stage data-source amendment, figure-derived status of GSM, retrospective comparison, and remaining provenance and extrapolation limitations.

The named release ZIP is the current scientific package. Automatic source-code downloads for the original v1.2.1 tag remain historical snapshots. Reviewer correspondence and cover letters remain in the separate submission package.

## Final submission update — 4 November 2026

- Applied the revised Abstract and Conclusion and minor terminology and interpretation corrections, preserving the scientific message.
- Ordered all 23 references by first citation and retained the visible v1.2.1 repository link.
- Added Supplement S9/Table 15: false-consensus counts and descriptive Wilson 95% intervals for all four cohorts, including conditional low-spread denominators. The added intervals do not adjust for isotopic-chain dependence.
- Verified 158 independent point checks and all 1,273 printed numeric values across 15 supplement tables.
- Preserved all 43 original scientific CSVs, seven figures and 19 frozen input/configuration files byte for byte. The new event-frequency CSV is independently recalculated from the preserved AME/model tables.
- Completed the 11-step reproduction on 4 November 2026: all 44 CSV comparisons passed (43 original files plus the new event-frequency table), with 19 frozen inputs unchanged.

The current checks and stand-alone event-frequency script are in `validation_2026_11_04/`. No fresh Fortran compilation is claimed. Download the named **JPhysG_106072_Reproducibility_v1.2.1.zip** and its matching **.sha256** attachment. Automatic source-code archives retain the original v1.2.1 tag snapshot. Reviewer correspondence, cover letters and highlighted/author-omitted submission copies are supplied separately in the private submission bundle.
