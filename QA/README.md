# FairQ QA Test Project

This folder contains a focused QA plan, test cases, reproducible findings, and an executable pytest suite for the FairQ backend.

## Scope

- DWFQ queue-selection logic (`backend/app/services/policies/dwfq.py`)
- Token input validation (`backend/app/schemas/token.py`)
- Manual API scenarios for token creation and lifecycle operations (`backend/app/routers/token.py`)

This is a test project for the existing application; it does not change application behavior. The API scenarios are documented for execution against a locally running FairQ instance. The automated tests are included, but this repository update does not claim that they have been run.

## Run the automated tests

From the repository root:

```bash
python -m pip install -e ./backend
python -m pip install pytest
python -m pytest QA/tests -v
```

The suite needs Python 3.10+ and the backend dependencies. It uses no live database or external SMS service.

## Documents

- [Test plan](test-plan.md) — objectives, scope, setup, and approach.
- [Test cases](test-cases.md) — scenarios with expected and actual-result tracking.
- [Bug reports](bug-reports.md) — reproducible findings and status.
- [Test summary](test-summary.md) — execution status, limitations, and release recommendation.

## Results honesty

A result marked **Not run** is not a measured runtime result. The whitespace-only service-type finding is identified by inspecting the current Pydantic schema and has a regression test marked as an expected failure until the validation is corrected. Run the suite and manual scenarios before reporting test pass counts or claiming the API has been verified.
