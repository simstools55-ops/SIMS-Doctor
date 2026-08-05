# SBM-Orchestrated Case Result V2

The standard RC12 route is:

```text
SBM -> Doctor -> SBM -> Writer -> SBM
```

SBM owns CaseID, workflow state, history, publication tracking, measurement, and reexamination scheduling. Doctor performs diagnosis and returns a treatment plan and referral recommendation. Doctor does not directly invoke Writer, Creator, or Merge.

The standard return contract is `SIMS_DOCTOR_CASE_RESULT_V2` version `2.0`.

Legacy direct specialist request builders are retained only for backward compatibility.
