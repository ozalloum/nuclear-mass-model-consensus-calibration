# Reproduction

From the repository root, run:

```bash
python -m pip install -r requirements.txt
python code/reproduce_repository.py
```

Expected final output:

```text
"status": "PASS"
```

The reproduction regenerates all reported CSV tables and the five PDF figures,
then checks the locked confirmation population, correlations, MAEs,
false-consensus counts, separation-energy result, and completion lock.
