#!/usr/bin/env python3
"""Regenerate reported tables and figures, then verify locked results."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def run(script):
    subprocess.run([sys.executable, str(ROOT / "code" / script), "--root", str(ROOT)], check=True)

run("plot_registered_design.py")
run("stage2c_analysis_figures.py")
subprocess.run([sys.executable, str(ROOT / "code/verify_repository.py")], check=True)
