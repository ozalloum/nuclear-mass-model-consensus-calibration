# Reproduce the current GSM revision

Download and extract JPhysG_106072_Reproducibility_v1.2.1.zip from this repository
or release v1.2.1. Start with public_release/README.md inside the ZIP.

```bash
cd public_release
python -m pip install -r requirements.txt
python reproduce_review_package.py --verify-only
python reproduce_review_package.py --output ../JPhysG_106072_reproduction
```

The root-level code/reproduce_repository.py reproduces the historical baseline
only. The current ZIP runner also covers the independent revision analyses, GSM,
source checks and updated submission figures. The output directory must be new.
