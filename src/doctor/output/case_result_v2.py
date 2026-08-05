from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


_TARGET_MAP = {
    "WRITER": "SIMS_WRITER",
    "SIMS_WRITER": "SIMS_WRITER",
    "CREATOR": "SIMS_CREATOR",
    "SIMS_CREATOR": "SIMS_CREATOR",
    "MERGE": "SIMS_MERGE",
    "SIMS_MERGE": "SIMS_MERGE",
    "OBSERVATION": "NONE",
    "MONITOR": "NONE",
}


def _list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, (list, tuple)) else []


class CaseResultV2Builder:
    """Build the SBM-owned diagnostic result contract.

    This builder does not invoke Writer, Creator, or Merge. It returns a
    treatment plan and referral recommendation to SBM, which owns orchestration.
    """

    def build(self, medical_record: dict[str, Any], *, user_display: Any = None) -> dict[str, Any]:
        patient = medical_record.get("patient", {})
        diagnoses = medical_record.get("final_diagnoses", [])
        diagnosis = diagnoses[-1] if diagnoses else None
        recommendations = medical_record.get("treatment_recommendations", [])
        recommendation = recommendations[-1] if recommendations else None
        referrals = medical_record.get("referrals", [])
        legacy_referral = referrals[-1] if referrals else None

        status = diagnosis.get("status") if diagnosis else "LIMITED"
        diagnosis_code = diagnosis.get("diagnosis_code") if diagnosis else None
        target = None
        if recommendation:
            target = recommendation.get("target") or recommendation.get("referral_target")
        if target is None and legacy_referral:
            target = legacy_referral.get("target")
        destination = _TARGET_MAP.get(target, "MANUAL_REVIEW" if target else "NONE")

        deferred = status == "DEFERRED"
        treatment_code = recommendation.get("treatment_code") if recommendation else None
        treatment_required = bool(recommendation and destination not in {"NONE"}) and not deferred
        action = "REFER" if treatment_required else ("MONITOR" if deferred or destination == "NONE" else "MANUAL_REVIEW")

        recommended_scope = []
        blocked_scope = []
        instructions = []
        review_days = diagnosis.get("recommended_review_days") if diagnosis else None
        if recommendation:
            recommended_scope = _list(recommendation.get("recommended_scope"))
            if not recommended_scope:
                recommended_scope = _list(recommendation.get("scope"))
            blocked_scope = _list(recommendation.get("prohibited_actions"))
            monitoring = recommendation.get("monitoring") or {}
            review_days = monitoring.get("review_after_days") or monitoring.get("recommended_review_days") or review_days
            instructions = _list(recommendation.get("instructions"))

        workflow = medical_record.get("workflow") or {}
        locked = bool(workflow.get("lock", {}).get("locked") or workflow.get("workflow_locked"))
        if locked:
            action = "DEFER"
            treatment_required = False

        diagnosis_id = diagnosis.get("diagnosis_id") if diagnosis else None
        completed_at = datetime.now(timezone.utc).isoformat()
        return {
            "format": "SIMS_DOCTOR_CASE_RESULT_V2",
            "contract_name": "SIMS_DOCTOR_SINGLE_CASE_RESULT_V1",
            "contract_version": "2.0",
            "case_id": medical_record.get("case_id"),
            "diagnosis_id": diagnosis_id,
            "medical_record_id": medical_record.get("medical_record_id"),
            "site_id": patient.get("site_id"),
            "article_id": patient.get("article_id"),
            "completed_at": completed_at,
            "diagnosis": {
                "status": status,
                "primary_code": diagnosis_code,
                "code": diagnosis_code,
                "secondary_codes": _list(diagnosis.get("secondary_codes")) if diagnosis else [],
                "priority": (recommendation or {}).get("priority") or (diagnosis or {}).get("priority"),
                "severity": (diagnosis or {}).get("severity"),
                "confidence": {
                    "overall": (diagnosis or {}).get("confidence"),
                },
                "summary": (diagnosis or {}).get("summary") or (diagnosis or {}).get("rationale"),
                "evidence_ids": _list((diagnosis or {}).get("evidence_ids")),
            },
            "treatment_plan": {
                "action": action,
                "treatment_required": treatment_required,
                "treatment_level": (recommendation or {}).get("treatment_level") or treatment_code,
                "priority": (recommendation or {}).get("priority"),
                "objective": (recommendation or {}).get("objective") or (recommendation or {}).get("reason"),
                "expected_impact": (recommendation or {}).get("expected_impact") or {"risk": (recommendation or {}).get("risk")},
                "review_after_days": review_days,
            },
            "referral": {
                "required": treatment_required,
                "destination": destination if treatment_required else "NONE",
                "target": (legacy_referral or {}).get("target") if treatment_required else None,
                "reason_codes": [code for code in [diagnosis_code, treatment_code] if code],
                "allowed_scope": recommended_scope,
                "blocked_scope": blocked_scope,
                "instructions": instructions,
            },
            "workflow": {
                "doctor_diagnosis_allowed": True,
                "doctor_treatment_recommended": treatment_required,
                "workflow_locked": locked,
                "lock_owner": (workflow.get("lock") or {}).get("lock_owner"),
                "lock_reference_id": (workflow.get("lock") or {}).get("lock_reference_id"),
                "user_approval_required": action in {"REFER", "MANUAL_REVIEW"},
                "return_to": "SIMS_BLOG_MANAGER",
            },
            "reexamination": {
                "required": bool(review_days),
                "trigger": "AFTER_MEASUREMENT" if review_days else None,
                "recommended_review_days": review_days,
                "required_evidence": ["PUBLICATION_CONFIRMATION", "POST_TREATMENT_PERFORMANCE"] if treatment_required else ["UPDATED_PERFORMANCE"],
            },
            "user_display": user_display,
            "compatibility": {
                "legacy_contract": "SIMS_DOCTOR_SINGLE_CASE_RESULT_V1",
                "direct_specialist_invocation": "DEPRECATED",
            },
        }
