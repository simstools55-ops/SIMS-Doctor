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
    "OBSERVE": "NONE",
    "FOLLOW_UP": "NONE",
}



def _treatment_class(destination: str, recommendation: dict[str, Any] | None) -> str:
    rec = recommendation or {}
    explicit = rec.get("treatment_class")
    if explicit:
        return str(explicit)
    level = str(rec.get("treatment_level") or rec.get("treatment_mode") or rec.get("treatment_code") or "").upper()
    if destination == "SIMS_CREATOR":
        return "新規記事作成"
    if destination == "SIMS_MERGE":
        return "記事統合"
    if destination == "NONE":
        return "経過観察"
    if any(token in level for token in ("FULL", "MAJOR", "L4")):
        return "全面リライト"
    if any(token in level for token in ("REWRITE", "L3")):
        return "通常リライト"
    if any(token in level for token in ("LIMITED", "LOCAL", "L2")):
        return "限定修正"
    return "軽微修正"


def _request_text(label: str, treatment_class: str, scope: list[Any], blocked: list[Any], dependencies: list[Any]) -> str:
    scope_text = "\n".join(f"・{item}" for item in scope) or "・診断で許可された範囲のみ実施"
    blocked_text = "\n".join(f"・{item}" for item in blocked) or "・診断範囲外の変更"
    dep_text = "\n".join(f"・{item}" for item in dependencies) or "・なし"
    return f"【担当】{label}\n【治療区分】{treatment_class}\n\n【実施すること】\n{scope_text}\n\n【変更しないこと】\n{blocked_text}\n\n【前提条件】\n{dep_text}\n\n処置後の結果はSBMへ登録してください。"

def _list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, (list, tuple)) else []


class CaseResultV2Builder:
    """Build a diagnostic result returned to SBM for orchestration.

    Doctor diagnoses and selects the next specialist, but does not create the
    final specialist request. SBM receives this JSON, combines it with the
    stored article body and evidence package, and generates the complete
    Writer, Creator, or Merge referral.
    """

    def build(self, medical_record: dict[str, Any], *, user_display: Any = None) -> dict[str, Any]:
        patient = medical_record.get("patient", {})
        diagnoses = medical_record.get("final_diagnoses", [])
        diagnosis = diagnoses[-1] if diagnoses else None
        recommendations = medical_record.get("treatment_recommendations", [])
        recommendation = recommendations[-1] if recommendations else None
        referrals = medical_record.get("referrals", [])
        legacy_referral = referrals[-1] if referrals else None
        algorithm_assessments = medical_record.get("algorithm_impact_assessments", [])
        algorithm_assessment = algorithm_assessments[-1] if algorithm_assessments else None

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
        dependencies = _list((recommendation or {}).get("dependencies"))

        workflow = medical_record.get("workflow") or {}
        locked = bool(workflow.get("lock", {}).get("locked") or workflow.get("workflow_locked"))
        if locked:
            action = "DEFER"
            treatment_required = False

        diagnosis_id = diagnosis.get("diagnosis_id") if diagnosis else None
        completed_at = datetime.now(timezone.utc).isoformat()
        treatment_class = _treatment_class(destination if treatment_required else "NONE", recommendation)
        request_text = _request_text(destination, treatment_class, recommended_scope, blocked_scope, dependencies) if treatment_required else None
        user_confirmation_text = request_text if destination == "MANUAL_REVIEW" or target == "SBM" else None
        action_checklist = []
        if user_confirmation_text:
            action_checklist.append({"order": 1, "owner": "USER", "action": "診断で指定された確認作業を行う", "dependencies": dependencies})
        elif treatment_required:
            action_checklist.append({"order": 1, "owner": destination, "action": "診断で許可された範囲の処置を実施する", "dependencies": dependencies})
        elif review_days:
            action_checklist.append({"order": 1, "owner": "SBM", "action": "再診日まで経過観察する", "dependencies": dependencies})
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
                "algorithm_assessment": algorithm_assessment,
            },
            "treatment_plan": {
                "action": action,
                "treatment_required": treatment_required,
                "treatment_level": (recommendation or {}).get("treatment_level") or treatment_code,
                "priority": (recommendation or {}).get("priority"),
                "objective": (recommendation or {}).get("objective") or (recommendation or {}).get("reason"),
                "expected_impact": (recommendation or {}).get("expected_impact") or {"risk": (recommendation or {}).get("risk")},
                "review_after_days": review_days,
                "strategy": (recommendation or {}).get("strategy"),
                "strategy_reason": (recommendation or {}).get("strategy_reason"),
                "wait_plan": (recommendation or {}).get("wait_plan"),
                "user_todo": _list((recommendation or {}).get("user_todo")),
                "reassurance_comment": (recommendation or {}).get("reassurance_comment"),
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
            "workflow_handoff": {
                "next_action": (
                    "USER_CONFIRMATION" if action == "MANUAL_REVIEW"
                    else "MONITOR" if locked or not treatment_required
                    else "WRITER" if destination == "SIMS_WRITER"
                    else "CREATOR" if destination == "SIMS_ARTICLE_CREATOR"
                    else "MERGE" if destination == "SIMS_MERGE"
                    else "USER_CONFIRMATION"
                ),
                "treatment_class": treatment_class,
                "action_checklist": action_checklist,
                "user_confirmation_text": user_confirmation_text,
                "writer_request_text": None,
                "creator_request_text": None,
                "merge_request_text": None,
                "dependencies": dependencies,
                "handoff_mode": "RETURN_TO_SBM_FOR_REFERRAL" if treatment_required else "RETURN_TO_SBM_FOR_MONITORING",
                "doctor_json_usage": "REQUIRED_SBM_REGISTRATION",
                "specialist_result_destination": "SIMS_BLOG_MANAGER" if treatment_required else None,
            },
            "user_display": user_display,
            "compatibility": {
                "legacy_contract": "SIMS_DOCTOR_SINGLE_CASE_RESULT_V1",
                "direct_specialist_invocation": "DISABLED",
                "doctor_result_registration_to_sbm": "REQUIRED",
                "specialist_referral_generation_by_sbm": "REQUIRED",
                "specialist_result_registration_to_sbm": "REQUIRED",
            },
        }
