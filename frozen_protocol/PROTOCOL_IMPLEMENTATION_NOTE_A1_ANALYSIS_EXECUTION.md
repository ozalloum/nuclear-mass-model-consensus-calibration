# Implementation Note A1 — analysis execution (pre-result)

Date: 2026-09-01

This note records software decisions made after freezing `PAPER2_PROTOCOL_v1_0_FROZEN_PREMODEL.md` but before loading any of the four theoretical mass tables.

- Development-defined spread quintile and covariate-tercile **internal cut points** are frozen from AME2012→2016. When applied to later data, values below/above the development range remain in the first/last bin rather than being discarded.
- Bootstrap confidence intervals use 10,000 nonparametric resamples, seed 42, as frozen.
- Pearson correlations among **signed** model residuals are supplementary shared-error diagnostics; they do not define false consensus.
- Leave-one-model-out arithmetic means are sensitivity analyses only and cannot replace the frozen four-model headline consensus.
- Result figures use distinct color/marker/line-style encodings for multiple series.
- The calcium shell-model stage is a hard scientific source gate for the full mechanism claim. If authoritative numerical S2n values are unavailable, the main consensus analysis may run, but the shell-mechanism claim remains explicitly blocked rather than filled by digitization.

No model-dependent threshold or region was changed in this implementation note.
