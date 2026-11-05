# FairQ QA Test Cases

**Execution status key:** `Not run` means no runtime result has yet been recorded. Update the Actual result and Status fields after executing each case. The automated test file names are included where applicable.

## A. Automated DWFQ checks

| ID | Scenario / input | Expected result | Actual result | Status |
|---|---|---|---|---|
| DWFQ-01 | Empty queue `[]` | Returns `None`; no exception. | Not run | Not run |
| DWFQ-02 | One normal customer, score `0`, wait `10` minutes | Returns that customer. | Not run | Not run |
| DWFQ-03 | Only vulnerable customers; scores `0.8` and `1.2`, equal wait | Returns the higher-priority customer (score `1.2`). | Not run | Not run |
| DWFQ-04 | Mixed group within fairness threshold: vulnerable score `0.6`, wait `0`; normal score `0`, wait `5` | Returns the vulnerable customer by effective priority. | Not run | Not run |
| DWFQ-05 | Fairness override: normal score `0`, wait `40`; vulnerable score `1`, wait `1`; default max ratio `1.5` | Returns the normal customer from the longer-waiting group (group average wait ratio `40:1`). | Not run | Not run |
| DWFQ-06 | Mixed groups at exactly the threshold: normal wait `3`; vulnerable wait `2`; default ratio `1.5` | Override is not triggered because implementation uses `>`; highest effective priority is selected. | Not run | Not run |
| DWFQ-07 | `vulnerability_score` exactly `0.5` | Customer is classified as vulnerable (`>= 0.5`). | Not run | Not run |

Automated file: `QA/tests/test_dwfq.py`.

## B. Automated token-schema checks

| ID | Scenario / input | Expected result | Actual result | Status |
|---|---|---|---|---|
| TOK-01 | Minimal valid payload: `{"service_type":"Cash deposit"}` | `TokenCreate` accepts it and applies defaults. | Not run | Not run |
| TOK-02 | NIC `" 123456789v "` | Accepted and normalized to `123456789V`. | Not run | Not run |
| TOK-03 | Phone `"+94 77-123-4567"` | Accepted and normalized by removing spaces and dashes. | Not run | Not run |
| TOK-04 | NIC with invalid format, e.g. `"12345"` | Rejected with Pydantic `ValidationError`. | Not run | Not run |
| TOK-05 | Phone with letters, e.g. `"077ABC1234"` | Rejected with `ValidationError`. | Not run | Not run |
| TOK-06 | Age `-1` or `151` | Rejected by the `0..150` bounds. | Not run | Not run |
| TOK-07 | Unsupported language, e.g. `"french"` | Rejected; only Sinhala, English, or Tamil are allowed. | Not run | Not run |
| TOK-08 | Vulnerability score above `2` or below `0` | Rejected by the `0..2` bounds. | Not run | Not run |
| TOK-09 | Unexpected field, e.g. `{"service_type":"Cash","unexpected":true}` | Rejected because extra input fields are forbidden. | Not run | Not run |
| TOK-10 | Whitespace-only service type, `"   "` | Should be rejected as blank input. Current schema appears to accept it; see BUG-001. | Source review indicates accepted; runtime test not run | Open / regression test xfail |

Automated file: `QA/tests/test_token_schema.py`.

## C. Manual API scenarios

Use the local API documentation (`/docs`) or an HTTP client. Use a disposable database, and avoid sending actual SMS messages. `token_id` below means an ID returned by a successful test token creation.

| ID | Scenario / steps | Expected result | Actual result | Status |
|---|---|---|---|---|
| API-01 | `POST /tokens/` with `{"service_type":"Cash deposit"}` | Successful creation; response contains a token ID/number and status `WAITING`. | Not run | Not run |
| API-02 | `POST /tokens/` with empty service type `{"service_type":""}` | Validation error; token is not created. | Not run | Not run |
| API-03 | `POST /tokens/` with invalid NIC `{"service_type":"Cash","nic":"bad-nic"}` | Validation error; token is not created. | Not run | Not run |
| API-04 | `POST /tokens/{token_id}/call` for a `WAITING` token | Success; token becomes `CALLED`. | Not run | Not run |
| API-05 | Call the same token again after it is `CALLED` | HTTP 400; state remains `CALLED`. | Not run | Not run |
| API-06 | `POST /tokens/{token_id}/start` for a `WAITING` token | Success; token becomes `SERVING`. | Not run | Not run |
| API-07 | `POST /tokens/{token_id}/complete` before it is `SERVING` | HTTP 400; state is unchanged. | Not run | Not run |
| API-08 | Complete a `SERVING` token | Success; token becomes `COMPLETED`. | Not run | Not run |
| API-09 | Call an unknown token ID | HTTP 404; no token state changes. | Not run | Not run |
| API-10 | Create a token with an unverified phone number | HTTP 400; no token is created. Configure SMS/OTP checks safely for this test. | Not run | Not run |

For each manual case, record the date, app revision, request, response status/body, and resulting database-visible state. If product requirements differ from an expected result above, update the expected result before marking the case failed.
