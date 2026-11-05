# FairQ QA Test Plan

## 1. Objective

Assess core backend behavior in FairQ with repeatable checks for queue selection and token input validation, and define practical API scenarios for token lifecycle behavior. Record expected and actual outcomes and document reproducible defects.

## 2. System under test

FairQ is a bank queue management system. This test plan targets the backend source in this repository, particularly:

- `backend/app/services/policies/dwfq.py`
- `backend/app/schemas/token.py`
- `backend/app/routers/token.py`

The DWFQ test cases use its current formula, vulnerability threshold, and default fairness ratio from source. They do not establish that the policy is fair for all real-world populations.

## 3. In scope

- Empty, single-group, and mixed-group DWFQ queues.
- Priority selection and fairness-ratio override.
- Valid and invalid token schema inputs: service type, NIC, age, gender, phone, language, and score bounds.
- Manual API checks for token creation and status transitions.
- Logging expected versus actual results and reporting defects.

## 4. Out of scope

- Production load, concurrency, penetration, accessibility, and cross-browser testing.
- Live SMS/OTP delivery and third-party integrations.
- Full end-to-end UI automation or deployment verification.
- Proving fairness outcomes using real bank-customer data.

## 5. Test approach

1. Run the isolated pytest suite in `QA/tests` for DWFQ selection and Pydantic validation.
2. Start a local FairQ backend with a disposable test database for manual API scenarios.
3. Use only synthetic test data and test phone numbers; do not use real customer identity data.
4. Capture each actual status code, response, and relevant resulting token state in `test-cases.md`.
5. Record a defect when actual behavior differs from the stated expected behavior; distinguish confirmed behavior from assumptions requiring product clarification.

## 6. Environment and prerequisites

- Python 3.10 or later.
- Backend dependencies installed (`python -m pip install -e ./backend`).
- pytest installed (`python -m pip install pytest`).
- For manual API scenarios, the local backend and a disposable database are configured per the repository README and environment example.
- API calls should use local test data. SMS-dependent paths require a controlled mock/test configuration; no external SMS should be sent during testing.

## 7. Entry and exit criteria

**Entry:** source checked out; dependencies installed; test database separated from any user or production data.

**Exit:** automated tests executed and results recorded; selected manual cases executed or explicitly left pending; all discrepancies logged with severity and reproduction steps; no result represented as executed when it was only inferred from source.

## 8. Severity guide

- **High:** blocks core queue or token processing, or risks incorrect service to customers.
- **Medium:** significant input or workflow defect with a workaround.
- **Low:** limited data-quality/usability issue with a workaround.
- **Info:** behavior or policy decision that needs clarification, not yet a confirmed defect.

## 9. Risks and assumptions

- DWFQ expectations in these cases reflect the implementation and examples; fairness policy thresholds should be confirmed by the product owner.
- Manual API outcomes depend on local database setup and application configuration.
- A passing unit suite does not prove correctness of the complete system or fairness in production.
