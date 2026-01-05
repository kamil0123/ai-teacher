# ai-teacher

Minimal Python scaffold (src layout, requirements.txt).

## Quickstart
- Create venv (PowerShell): `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1`
- Install deps: `pip install -r requirements.txt`
- Run app (repo root): `set PYTHONPATH=%CD%\src` then `python -m ai_teacher`
- Run tests: `set PYTHONPATH=%CD%\src` then `python -m unittest`

## Project layout
- requirements.txt — runtime dependencies (empty starter)
- src/ai_teacher/ — package code; `__main__.py` enables `python -m ai_teacher`
- tests/ — unit tests anchored to src layout