# v1.2.1 — current synchronized scientific package

This release contains the current JPhysG-106072 scientific package and the documented revision-stage GSM data-source amendment.

- The manuscript is synchronized with the current journal revision.
- Figure 7 is synchronized with the manuscript. The plotted values and common axes are unchanged; the legends are placed inside the upper-right corner of panels (a) and (b).
- All 15 vector-digitized GSM values are unchanged and agree with the supplied journal PDF plot to 0.01 MeV; the maximum rounding discrepancy remains 0.0046093 MeV.
- Separate 48Ca-core and 54Ca-core series, matched-isotope comparisons and extraction sensitivity remain included.
- The frozen scientific data and numerical results are unchanged.
- Full scientific reproduction materials, original Fortran source, Windows verification bundle, run evidence and raw DZ31 output remain included.

The figure-derived GSM values are reconstructed estimates, not original solver outputs. The ±0.10 MeV allowance is a stress test, not a confidence interval. The regional comparison remains retrospective.

Reviewer correspondence and alternate submission documents are excluded from the public scientific package.

The manuscript repository name and published baseline URL have been updated to `ozalloum/nuclear-mass-models` (release `v1.2.1`). The manuscript source, PDF, package README and checksums are synchronized. This is a repository-location correction; scientific data and numerical results are unchanged.

Conclusion wording refined to describe the observed rank associations and their uncertainty, clarify empirical interval coverage, and distinguish cohort-specific scale estimates from universal calibration. The scientific message, numerical results, figures, and data are unchanged.

## Reviewed update — 3 November 2026

- Replaced the manuscript and numerical supplement PDFs and LaTeX sources with the reviewed versions. The scientific conclusion and numerical results are unchanged.
- Restored the original missing DZ31 raw output (21,275 rows), verified against its recorded SHA-256 digest.
- Preserved all 43 scientific CSVs and 19 frozen input/configuration files byte for byte.
- Included the successful ten-step reproduction record, 158 independent point checks, and checks of 1,225 printed values across all 14 supplement tables.
- Added the tested dependency specification and the Windows UTF-8 portability fix for the optional Coraggio source-PDF checker. No fresh Fortran compilation is claimed.

Download **JPhysG_106072_Reproducibility_v1.2.1.zip** and its matching **.sha256** attachment. The automatic “Source code” archives retain the original v1.2.1 tag snapshot; the named scientific ZIP contains this reviewed update. Reviewer correspondence, cover letters and alternate submission documents remain outside the public scientific package.

## Final submission update — 4 November 2026

- Applied the revised Abstract and Conclusion and minor terminology and interpretation corrections, preserving the scientific message.
- Ordered all 23 references by first citation and retained the visible v1.2.1 repository link.
- Added Supplement S9/Table 15: false-consensus counts and descriptive Wilson 95% intervals for all four cohorts, including conditional low-spread denominators. The added intervals do not adjust for isotopic-chain dependence.
- Verified 158 independent point checks and all 1,273 printed numeric values across 15 supplement tables.
- Preserved all 43 original scientific CSVs, seven figures and 19 frozen input/configuration files byte for byte. The new event-frequency CSV is independently recalculated from the preserved AME/model tables.
- Completed the 11-step reproduction on 4 November 2026: all 44 CSV comparisons passed (43 original files plus the new event-frequency table), with 19 frozen inputs unchanged.

The current checks and stand-alone event-frequency script are in `validation_2026_11_04/`. No fresh Fortran compilation is claimed. Download the named **JPhysG_106072_Reproducibility_v1.2.1.zip** and its matching **.sha256** attachment. Automatic source-code archives retain the original v1.2.1 tag snapshot. Reviewer correspondence, cover letters and highlighted/author-omitted submission copies are supplied separately in the private submission bundle.
