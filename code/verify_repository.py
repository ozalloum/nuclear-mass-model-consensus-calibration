#!/usr/bin/env python3
"""Verify the locked headline results in the minimal repository."""
from pathlib import Path
import json
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

perf = pd.read_csv(ROOT / "tables/Table2_Consensus_Performance.csv")
s2n = pd.read_csv(ROOT / "tables/Table5_S2n_Consensus.csv")
conf = pd.read_csv(ROOT / "stage2b_confirmation/CONFIRMATION_SCORED_LOCKED.csv")
lock = json.loads((ROOT / "stage2b_confirmation/CONFIRMATION_RESULTS_LOCKED.json").read_text())

row = perf.loc[perf["vintage"] == "confirmation"].iloc[0]
srow = s2n[(s2n["vintage"] == "confirmation") & (s2n["quantity"] == "consensus")].iloc[0]

checks = {
    "confirmation_rows": len(conf) == 51,
    "confirmation_n": int(row["n_complete"]) == 51,
    "confirmation_rho": math.isclose(float(row["spearman_D_vs_E"]), 0.2647963800904977, abs_tol=1e-12),
    "confirmation_mean_mae": math.isclose(float(row["consensus_mean_MAE_MeV"]), 0.2469463725490197, abs_tol=1e-12),
    "confirmation_median_mae": math.isclose(float(row["consensus_median_MAE_MeV"]), 0.24425821568627515, abs_tol=1e-12),
    "fc_a": int(row["fc_A_n"]) == 0,
    "fc_b": int(row["fc_B_n"]) == 2,
    "s2n_n": int(srow["n"]) == 34,
    "s2n_mae": math.isclose(float(srow["MAE_MeV"]), 0.12595085294117775, abs_tol=1e-12),
    "completion_lock": bool(lock),
}

result = {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks}
print(json.dumps(result, indent=2))
if result["status"] != "PASS":
    raise SystemExit(1)
