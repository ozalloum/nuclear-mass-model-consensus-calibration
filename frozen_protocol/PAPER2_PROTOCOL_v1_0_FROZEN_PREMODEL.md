# Paper 2 frozen protocol v1.0 - PRE-MODEL

**Freeze date:** 2026-09-01  
**Status:** Frozen before any FRDM2012, HFB27, DZ31, or WS4 prediction table is inspected in this Paper 2 analysis.

## Scientific question

**When should we trust nuclear-model consensus?**

The paper tests whether agreement among physically different global nuclear-mass models is an informative uncertainty surrogate for nuclei whose masses were measured later, and identifies conditions under which low inter-model spread gives false confidence.

Working title: **When Should We Trust Nuclear-Model Consensus? Historical Tests of Agreement, False Confidence, and Shell Structure**

## Scope boundary

The paper is deliberately narrow. It is **not** a model leaderboard and does not introduce a new mass model.

Included:
- FRDM2012
- HFB27
- DZ31
- WS4
- experimental AME2012, AME2016, AME2020
- primary observable: atomic mass excess
- structural secondary observable: two-neutron separation energy S2n
- one predeclared mechanistic regional benchmark: neutron-rich calcium isotopes using a published nuclear shell-model calculation

Excluded from the main study:
- semi-empirical mass formula (SEMF)
- Fermi-gas model
- machine-learning correction or residual learning
- Bayesian model averaging
- architecture/model-combination optimization
- large multi-observable survey
- multiple post-hoc shell-model regions

## Research questions

### RQ1 - Does model agreement predict future accuracy?
Is inter-model disagreement among FRDM2012, HFB27, DZ31, and WS4 calibrated to the errors observed when previously unmeasured nuclear masses are measured later?

### RQ2 - When does consensus fail?
Which prespecified nuclear-chart conditions are associated with low inter-model disagreement despite large later experimental error?

### RQ3 - Is false consensus associated with local shell structure?
In the predeclared calcium region, does a regional shell-model calculation provide structural information in S2n that is obscured by consensus among global mass models?

## Historical design

### Development
AME2012 -> AME2016 genuinely new measured nuclei. All diagnostic thresholds and calibration definitions are estimated/frozen here only.

### Confirmation
AME2016 -> AME2020 genuinely new measured nuclei. This is opened once after development is frozen. No threshold, model subset, region, observable, or plotting scale may be retuned from confirmation performance.

`new` means absent as a finite, measured, non-estimated mass in the previous AME vintage and present as measured/non-estimated in the later vintage.

### Claim boundary for chronology
The historical AME split is an **outcome-blind evaluation by experimental vintage**. Model-specific papers and data documentation will be audited for publication date and calibration inputs. A stronger claim that a target nucleus was excluded from a model's parameter adjustment will be made only where source documentation supports that statement. Otherwise the manuscript will say "later experimental outcome" rather than "strict model-fit holdout."

## Experimental population

Primary population in each AME vintage:
- Z >= 8 and N >= 8
- finite mass excess and binding-energy-per-nucleon entries
- mass and binding entries are measured/non-estimated (no `#`)
- finite mass-excess uncertainty < 100 keV

Broad measured sensitivity:
- same conditions but without the 100 keV mass-excess-uncertainty cutoff.

Estimated values (`#`) never enter measured headline samples. Missing values (`*`) are NA, never zero.

## Consensus definitions

For a target nucleus i and K=4 global models with mass-excess predictions M_ik:

- Primary consensus center: arithmetic mean
  Mbar_i = (1/K) sum_k M_ik
- Primary inter-model disagreement:
  D_i = sample standard deviation across the four model predictions (ddof=1)
- Later experimental error:
  E_i = |Mbar_i - Mexp_i|

The primary hypothesis interrogated is the common reliability assumption that smaller D should imply smaller E.

### Sensitivities
- consensus median instead of mean
- leave-one-model-out consensus (four prespecified subsets)
- pairwise residual correlations to quantify shared error structure

No weights are learned from confirmation data.

## False-consensus definitions

Two definitions are frozen before model predictions are examined.

### FC-A: absolute, physically interpretable
`D <= 0.25 MeV` AND `E >= 1.00 MeV`.

### FC-B: development-rank sensitivity
Low-spread threshold = Q25 of D on AME2012->2016 development.  
High-error threshold = Q75 of E on AME2012->2016 development.  
Both numerical thresholds are frozen after development and applied unchanged to confirmation.

FC-B is a sensitivity analysis; FC-A is the primary named event.

## Calibration analysis (RQ1)

Development and confirmation are analyzed separately.

Primary summaries:
1. Spearman correlation rho(D,E), with 95% percentile bootstrap CI.
2. D grouped by **development-defined quintile edges**; report mean E, median E, and 68%/95% bootstrap CIs in each bin.
3. Low-spread failure rate P(E>=1 MeV | D<=0.25 MeV).
4. FC-A and FC-B prevalence with Wilson 95% intervals.

Bootstrap: 10,000 resamples, seed 42. Confirmation bin edges and FC-B thresholds are never recomputed.

## Nuclear-chart conditions (RQ2)

All covariates are fixed before model predictions:

### Extrapolation distance
Primary distance to previous-vintage primary measured set:

d2(N,Z) = min_j sqrt[(N-N_j)^2 + (Z-Z_j)^2].

Sensitivity:

d1(N,Z) = min_j |N-N_j| + |Z-Z_j|.

### Traditional shell proximity
Neutron magic numbers: {20, 28, 50, 82, 126}.  
Proton magic numbers: {20, 28, 50, 82}.

Record `dN_magic`, `dZ_magic`, and a prespecified `near_magic` indicator equal to 1 when either distance <=2.

### Isospin asymmetry
I=(N-Z)/A.

RQ2 is explanatory, not a data-driven search for a favorable subgroup. Main comparisons are by extrapolation-distance terciles (defined on development), near-magic vs not, and neutron-excess terciles (development-defined). Continuous associations are also reported.

## S2n analysis

For mass excess ME in MeV:

S2n(N,Z) = ME(N-2,Z) + 2*Delta_n - ME(N,Z),
where Delta_n = 8.0713181 MeV.

Experimental S2n is reported only if target and required neighbor masses are finite and non-estimated in that AME vintage. Model S2n requires predictions for both nuclei from the same model.

Define D_S2n and E_S2n exactly analogously to mass-excess D and E. S2n is a secondary structural endpoint; it does not redefine the mass-excess headline conclusion.

## Calcium shell-model mechanism (RQ3)

The regional mechanism is frozen as the **calcium isotopic chain, Z=20, N=28..40** (48Ca through 60Ca), with emphasis on N=32 and N=34 shell evolution and S2n.

Primary published shell-model reference candidate (predeclared):
J. G. Li et al., Phys. Rev. C 102, 034302 (2020), realistic Gamow shell model with continuum coupling.

Secondary corroborating reference:
L. Coraggio et al., Phys. Rev. C 102, 054326 (2020).

The shell model is **not** a fifth global ensemble member and will not receive a global RMS ranking. It is a mechanistic regional control. Numerical shell-model values will be used only from a source table, author data, or reproducible calculation; no manual figure digitization will support headline numerical claims.

Because these shell-model studies are 2020 publications, the regional analysis is explicitly described as a **retrospective structural mechanism**, not as an untouched AME2016->2020 prospective prediction unless source-level chronology establishes otherwise.

## Global-model source and leakage gate

Each model must pass before analysis:
- exact model/version identification
- original or authoritative public prediction table
- source URL / citation
- local SHA-256
- documented units and quantity (mass excess, atomic mass, or binding energy)
- parser identity checks (A=N+Z, unique N,Z)
- at least 6 deterministic spot checks against published values or an independent authoritative copy
- publication/calibration-data chronology note

The four-model headline sample uses complete cases only: a target must have predictions from all four models. Missing prediction coverage is reported, not imputed.

## Model ensemble

Frozen four-model set:
1. FRDM2012 - finite-range droplet, macroscopic-microscopic
2. HFB27 - Skyrme Hartree-Fock-Bogoliubov / EDF
3. DZ31 - Duflo-Zuker
4. WS4 - Weizsacker-Skyrme macroscopic-microscopic

No model can be dropped because of poor confirmation performance. A model may be excluded only if its source/provenance gate cannot be validated; such an exclusion must be documented before opening confirmation and the four-model headline analysis then remains blocked rather than silently switching ensembles.

## Statistical multiplicity and interpretation

- RQ1 mass-excess calibration is primary.
- S2n and RQ2 condition analyses are secondary/mechanistic.
- Calcium is a predeclared case study.
- Exact p-values are not the main contribution; effect sizes, calibration behavior, confidence intervals, and replicated direction from development to confirmation are prioritized.
- No claim of causal origin is made from chart-location associations alone.

## Planned main figures (maximum six)

1. Historical design and model-consensus schematic / target map.
2. Consensus calibration: later error E versus inter-model spread D, with FC-A quadrant highlighted.
3. Development-defined spread bins versus later error, development and locked confirmation.
4. Nuclear-chart map of false-consensus cases and extrapolation distance.
5. Mass-excess consensus versus S2n consensus reliability.
6. Predeclared calcium S2n mechanism: four global models, experiment, regional shell-model result.

Every multi-series line plot must use a distinct combination of **color + line style + marker**.

## Planned main tables

1. Data/model provenance and historical target counts.
2. Individual model sanity-check errors plus unweighted consensus calibration summaries.
3. False-consensus prevalence and condition effects.
4. Calcium structural case (only if numerical shell-model values pass provenance gate).

## Release rules

- Never expose AME2016->2020 model-error results before the development thresholds/configuration hash is written.
- Confirmation is scored once and locked by a completion file; the code must refuse a second scoring unless run in an explicitly separate forensic-copy directory.
- Synthetic data are software validation only and must never be described as empirical results.
- Final release requires code compilation, file-hash manifest, figure/table source checks, LaTeX compilation, PDF render QA, and a final audit with zero hard failures.
