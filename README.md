# SIMS Doctor v1.0

SIMS Doctor is the independent diagnosis product in the SIMS Editorial Platform.
It receives a case request from SIMS Blog Manager, maintains the medical record as the diagnostic SSOT, and later produces diagnosis and referral contracts. It does not rewrite articles.

## Current release

`1.0.0-sprint2.2-foundation`

Sprint2-2 implements the reception foundation:

1. Receive `SIMS_DOCTOR_SINGLE_CASE_REQUEST_V1`
2. Validate and normalize the request
3. Generate Request ID
4. Create or reuse an active Case
5. Create or update `SIMS_DOCTOR_MEDICAL_RECORD_V1`
6. Return `SIMS_DOCTOR_SINGLE_CASE_RESULT_V1`

365-day data collection, SERP comparison, diagnosis, and referral generation remain outside this release.

## Repository structure

```text
contracts/   JSON interface contracts and registries
docs/        architecture and compatibility documentation
integration/ SBM safety boundary documents
knowledge/   Doctor-specific diagnostic knowledge
product/     product definition and sprint specifications
runtime/     existing runtime assets and validators
src/doctor/  Sprint2-2 implementation
tests/       unit, contract and integration tests
```

## Run tests

```bash
python -m pip install pytest jsonschema
pytest -q
python tests/contract/validate_fixtures.py
```

## Compatibility warning

The single-case schemas remain provisional until compared with one real JSON copied from the current SBM Doctor dialog. Do not change SBM output silently to fit the schema. Contract incompatibility requires an explicit contract revision.

## Architectural principles

- SBM contains no Doctor diagnosis logic.
- JSON contracts are the only system-to-system interface.
- Medical Record is the Doctor diagnostic SSOT.
- User-facing messages and system-facing contracts are separated.
- Diagnosis and referral are separate artifacts.
- Observation and diagnosis do not read the raw SBM request directly.


## Sprint3.1 Clinical Knowledge Base

Doctor now includes a declarative Clinical Knowledge Base for:

- Observation types
- Evidence codes
- Vital Signs and normal ranges
- Findings and severity
- Medical-record event types

Runtime loading is implemented in `src/doctor/knowledge/`.
Scoring, diagnosis, and referral decisions remain intentionally unimplemented.


## Sprint3.2 Observation Event Log

- Append-only Medical Record event log
- Event sequencing and payload-integrity verification
- Idempotent Observation replay
- 28/90/365-day Search Console input contract
- Search Console Observation recording into the medical record

Live Search Console retrieval remains outside this release.


## Sprint3.3 Evidence Engine

Doctor can now extract and store traceable Evidence from Observation data.

Initial Evidence codes:

- CTR_BELOW_POSITION_EXPECTATION
- POSITION_DECLINE_OBSERVED
- VISIBILITY_DECLINE_OBSERVED
- LONG_TIME_SINCE_UPDATE

Thresholds remain versioned in the Clinical Knowledge Base.
LOW_SAMPLE Evidence is retained and flagged.


## Sprint3.4 Vital Signs and Vital Profile

Doctor now creates a seven-sign Vital Profile.

Available now:

- Visibility
- Traffic
- CTR Health
- Ranking Stability
- Freshness

Unavailable until later Observation layers:

- Competition Resilience
- Content Integrity


## Sprint4.1 Findings Engine

Doctor now creates severity-bearing Findings from Evidence and the latest Vital Profile.

Initial Findings:

- CTR_UNDERPERFORMING
- POSITION_DECLINING
- LOW_VISIBILITY
- CONTENT_OUTDATED
- HIGH_VISIBILITY_LOW_CLICK
- INSUFFICIENT_EVIDENCE

Findings remain distinct from Diagnosis.


## Sprint4.2 Differential Diagnosis

Doctor now produces ranked diagnostic hypotheses with confidence, support, contradiction,
and full traceability.

Initial candidates:

- LOW_CTR_WITH_STRONG_POSITION
- LONG_TERM_DECLINE
- CONTENT_STALE
- UPDATE_FAILURE
- INSUFFICIENT_DATA

These candidates are not yet Final Diagnoses.


## Sprint4.3 Final Diagnosis

Doctor now records CONFIRMED or DEFERRED final diagnosis outcomes.


## Sprint5.1 Treatment Recommendation and Referral

Doctor now converts the latest Final Diagnosis into a separate treatment direction and referral.

Active routing:

- confirmed CTR, decline, stale-content, and update-failure diagnoses → Writer
- deferred diagnoses → Observation / follow-up

Creator, Merge, noindex, and delete routing remain reserved for later diagnosis expansion.


## Sprint6.1 Search Console 365-Day Acquisition

Doctor now contains a provider-neutral acquisition service and Google API adapter for:

- 28-day aggregate metrics
- 90-day aggregate metrics
- 365-day aggregate metrics
- paged query-level metrics
- retry and partial-failure reporting
- conversion into the existing Search Console Observation contract

Credentials and OAuth UI are intentionally excluded.


## Sprint6.2 SERP Observation

Doctor now supports provider-neutral SERP acquisition and Medical Record snapshots.

Recorded data includes:

- top results
- search intent
- SERP features
- competition strength
- changes from the previous SERP snapshot

SERP data now enables the Competition Resilience Vital Sign.


## Sprint6.3 Article Snapshot Observation

Doctor now records article structure and content metadata as an immutable snapshot.

This enables the final previously unavailable Vital Sign:

- Content Integrity

All seven Vital Signs can now be represented when the required observations exist.
