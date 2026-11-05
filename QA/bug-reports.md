# FairQ Bug Reports

## BUG-001 — Whitespace-only service type is accepted

- **Severity:** Low (data quality)
- **Status:** Open — identified by source review; runtime reproduction has not yet been recorded.
- **Affected area:** Token creation validation (`backend/app/schemas/token.py`, `TokenBase.service_type`).
- **Evidence:** `service_type` has a minimum length of one, but the schema does not trim or reject whitespace-only values. A string containing spaces has a nonzero length and therefore appears to satisfy the configured length constraint.

### Reproduction steps

1. From the repository root, install the backend dependencies: `python -m pip install -e ./backend`.
2. Run:
   ```bash
   python -c 'from app.schemas.token import TokenCreate; print(repr(TokenCreate(service_type="   ").service_type))'
   ```
3. Observe whether validation accepts the value and prints a string containing spaces. Record the actual output and environment in the report.
4. For API confirmation, send `POST /tokens/` with `{"service_type":"   "}` to a local test instance using a disposable database; confirm whether a token is created. Do not use production.

### Expected result

Whitespace-only service types should be rejected as blank input, and no token should be created.

### Actual result

Source inspection indicates the schema accepts the value because it checks length but does not strip whitespace. Runtime/API behavior is **not yet verified**. The automated regression test is marked `xfail` until the application validation is fixed; this is not a claim that the test suite has been executed.

### Suggested correction

Normalize whitespace and reject an empty result in a Pydantic validator, then add a regular passing regression test for whitespace-only input.

## Exploratory note — transferring a finalized token

The current transfer handler sets a token back to `WAITING` and does not visibly restrict the source status. This may allow a `COMPLETED` token to be transferred back into the queue. Whether that is a defect depends on FairQ's intended operational policy. Treat this as an **Info / requirements question**, not a confirmed bug, until the product owner defines which statuses may be transferred and API-01-style manual testing confirms the behavior.

### Suggested investigation

1. Create and complete a test token.
2. Call `POST /tokens/{token_id}/transfer` with `{"target_counter_id":null}`.
3. Record the status code and resulting state.
4. Compare the result against the approved token lifecycle requirements.
