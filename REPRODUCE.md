# Reproduce the current GSM revision

Download and extract JPhysG_106072_Reproducibility_v1.2.1.zip from this repository
or release v1.2.1. Start with public_release/README.md inside the ZIP.

```bash
cd public_release
python -m pip install -r requirements.review-tested.txt
python reproduce_review_package.py --verify-only
python reproduce_review_package.py --output ../JPhysG_106072_reproduction
```

The root-level code/reproduce_repository.py reproduces the historical baseline
only. The current ZIP runner also covers the independent revision analyses, GSM,
source checks and updated submission figures. The output directory must be new.

The reviewed environment used Python 3.13.9. Current successful checks are in
public_release/validation_2026_11_03/. The named ZIP contains the reviewed update;
the automatic source-code download for the tag retains its historical snapshot.
