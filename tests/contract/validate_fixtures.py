from pathlib import Path
import json
import sys

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    print("Install dependency: pip install jsonschema")
    raise

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts"
FIXTURES = ROOT / "tests" / "fixtures"

CASES = [

    (
        CONTRACTS / "SIMS_DOCTOR_IMPROVEMENT_FAILURE_ASSESSMENT_V1.schema.json",
        ROOT / "tests" / "fixtures" / "improvement_failure" / "result.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_DOCTOR_VITAL_SCORE_RESULT_V1.schema.json",
        ROOT / "tests" / "fixtures" / "vital_score" / "result.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_DOCTOR_RULE_EVALUATION_RESULT_V1.schema.json",
        ROOT / "tests" / "fixtures" / "diagnostic_rules" / "evaluation_result.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_SBM_DOCTOR_BATCH_REQUEST_V1.schema.json",
        ROOT / "tests" / "fixtures" / "sbm_batch" / "request.json",
        True,
    ),
    (
        CONTRACTS / "SIMS_SBM_DOCTOR_BATCH_ACCEPTED_V1.schema.json",
        ROOT / "tests" / "fixtures" / "sbm_batch" / "accepted.json",
        True,
    ),
    (
        CONTRACTS / "SIMS_SBM_DOCTOR_BATCH_STATUS_V1.schema.json",
        ROOT / "tests" / "fixtures" / "sbm_batch" / "status.json",
        True,
    ),
    (
        CONTRACTS / "SIMS_SBM_DOCTOR_BATCH_RESULT_PACKAGE_V1.schema.json",
        ROOT / "tests" / "fixtures" / "sbm_batch" / "result_package.json",
        True,
    ),
    (
        CONTRACTS / "SIMS_SBM_DOCTOR_BATCH_IMPORT_ACK_V1.schema.json",
        ROOT / "tests" / "fixtures" / "sbm_batch" / "import_ack.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_DOCTOR_BATCH_QUEUE_RECORD_V1.schema.json",
        ROOT / "tests" / "fixtures" / "batch_queue" / "queue_record.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_DOCTOR_BATCH_REQUEST_V1.schema.json",
        ROOT / "tests" / "fixtures" / "batch" / "batch_request.json",
        True,
    ),
    (
        CONTRACTS / "SIMS_DOCTOR_BATCH_RESULT_V1.schema.json",
        ROOT / "tests" / "fixtures" / "batch" / "batch_result.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_DOCTOR_LONGITUDINAL_PROFILE_V1.schema.json",
        ROOT / "tests" / "fixtures" / "longitudinal" / "profile.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_DOCTOR_TREATMENT_HISTORY_INPUT_V1.schema.json",
        ROOT / "tests" / "fixtures" / "treatment_history" / "worsened.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_DOCTOR_LONG_TERM_OBSERVATION_INPUT_V1.schema.json",
        ROOT / "tests" / "fixtures" / "long_term" / "gradual_decline.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_DOCTOR_CROSS_ARTICLE_OBSERVATION_INPUT_V1.schema.json",
        ROOT / "tests" / "fixtures" / "cross_article" / "merge_candidate.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_DOCTOR_SINGLE_CASE_RESULT_V1.schema.json",
        ROOT / "tests" / "fixtures" / "output" / "single_case_result.json",
        True,
    ),
    (
        CONTRACTS / "SIMS_DOCTOR_WRITER_REQUEST_V1.schema.json",
        ROOT / "tests" / "fixtures" / "output" / "writer_request.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_DOCTOR_ARTICLE_SNAPSHOT_INPUT_V1.schema.json",
        ROOT / "tests" / "fixtures" / "article_snapshot" / "complete_snapshot.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_DOCTOR_SERP_OBSERVATION_INPUT_V1.schema.json",
        ROOT / "tests" / "fixtures" / "serp" / "complete_serp.json",
        True,
    ),

    (
        CONTRACTS / "SIMS_DOCTOR_SEARCH_CONSOLE_OBSERVATION_INPUT_V1.schema.json",
        ROOT / "tests" / "fixtures" / "search_console" / "complete_365_days.json",
        True,
    ),
    (
        CONTRACTS / "SIMS_DOCTOR_SINGLE_CASE_REQUEST_V1.schema.json",
        FIXTURES / "valid" / "single_case_request.json",
        True,
    ),
    (
        CONTRACTS / "SIMS_DOCTOR_MEDICAL_RECORD_V1.schema.json",
        FIXTURES / "valid" / "initial_medical_record.json",
        True,
    ),
    (
        CONTRACTS / "SIMS_DOCTOR_SINGLE_CASE_REQUEST_V1.schema.json",
        FIXTURES / "invalid" / "missing_article_id.json",
        False,
    ),
    (
        CONTRACTS / "SIMS_DOCTOR_SINGLE_CASE_REQUEST_V1.schema.json",
        FIXTURES / "invalid" / "unsupported_version.json",
        False,
    ),
]

failed = 0
for schema_path, fixture_path, should_pass in CASES:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    errors = list(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(fixture)
    )
    passed = not errors
    expected = "PASS" if should_pass else "FAIL"
    actual = "PASS" if passed else "FAIL"
    ok = passed == should_pass
    print(f"[{'OK' if ok else 'NG'}] {fixture_path.name}: expected={expected}, actual={actual}")
    if not ok:
        failed += 1
        for error in errors[:5]:
            print("  -", error.message)

sys.exit(1 if failed else 0)
