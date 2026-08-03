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
