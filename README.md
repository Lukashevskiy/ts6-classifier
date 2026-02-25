# bastion6-features

Feature extraction pipeline for T6SS effector classification tasks (Bastion6-like).

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
