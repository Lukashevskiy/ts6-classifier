# bastion6-features

Feature extraction pipeline for T6SS effector classification tasks (Bastion6-like).

Submission-ready report: `REPORT.md`

## Structure
- `src/t6` — core library (IO, features, pipeline)
- `scripts/` — entrypoints and quick checks
- `data/` — input data (gitignored)
- `out/` — generated artifacts (gitignored)

## Quick start
1) Put `T6SE_training_data.zip` into `data/`
2) Create and activate a venv:
   - `python3.11 -m venv .venv`
   - `source .venv/bin/activate` (Linux/macOS)
   - `.\.venv\Scripts\Activate.ps1` (Windows PowerShell)
3) Install deps: `pip install -e .`
4) Run: `python scripts/make_features.py`

## Sanity check
Run a tiny in-memory example:
`python scripts/demo_check_api.py`

## Output files for assignment
After `scripts/make_features.py` finishes, `out/` contains:
- Combined full tables:
  - `positive_features.csv/.tsv`
  - `negative_features.csv/.tsv`
  - `all_features.csv/.tsv`
- Separate tables by feature type (for positive/negative/all):
  - `*_aac.csv/.tsv` (AAC)
  - `*_dpc.csv/.tsv` (DPC)
  - `*_qso.csv/.tsv` (QSO)
  - `*_ctdc.csv/.tsv` (7 physicochemical CTDC composition groups)
  - `*_ctdt.csv/.tsv` (CTDT transition frequencies)
