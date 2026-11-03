# v1.2.1 â€” current synchronized scientific package

This release contains the current JPhysG-106072 scientific package and the documented revision-stage GSM data-source amendment.

- The manuscript is synchronized with the current journal revision.
- Figure 7 is synchronized with the manuscript. The plotted values and common axes are unchanged; the legends are placed inside the upper-right corner of panels (a) and (b).
- All 15 vector-digitized GSM values are unchanged and agree with the supplied journal PDF plot to 0.01 MeV; the maximum rounding discrepancy remains 0.0046093 MeV.
- Separate 48Ca-core and 54Ca-core series, matched-isotope comparisons and extraction sensitivity remain included.
- The frozen scientific data and numerical results are unchanged.
- Full scientific reproduction materials, original Fortran source, Windows verification bundle, run evidence and raw DZ31 output remain included.

The figure-derived GSM values are reconstructed estimates, not original solver outputs. The Â±0.10 MeV allowance is a stress test, not a confidence interval. The regional comparison remains retrospective.

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
