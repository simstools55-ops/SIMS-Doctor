# Diagnosis Report and Output Architecture

## Outputs

- `SIMS_DOCTOR_SINGLE_CASE_RESULT_V1`: Doctor's system result for SBM and other consumers
- User Display: plain-language diagnosis summary embedded in the result
- `SIMS_DOCTOR_WRITER_REQUEST_V1`: treatment referral for Writer

## Separation

The user display does not expose internal codes or raw rules.
The system result retains trace IDs.
The Writer request contains treatment goals and preservation constraints, not the full Medical Record.
