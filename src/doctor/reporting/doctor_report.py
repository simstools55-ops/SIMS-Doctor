from __future__ import annotations

from typing import Any


class DoctorReportGenerator:
    def __init__(self, policy: dict[str, Any]) -> None:
        self.labels = policy["labels"]

    def generate(self, medical_record, composite, recommendation, *, audience):
        if audience not in {"USER", "SYSTEM"}:
            raise ValueError("Unsupported report audience")

        patient = medical_record.get("patient", {})
        final = composite["final_diagnosis"]
        label = self.labels.get(final, final)
        target = recommendation["referral_target"]
        priority = recommendation["priority"]

        article = {
            "site_id": patient.get("site_id"),
            "article_id": patient.get("article_id"),
            "url": patient.get("article_url") or patient.get("url"),
            "title": patient.get("article_title") or patient.get("title"),
        }
        summary = self._summary(label, target, priority)
        diagnosis = {
            "code": final,
            "label": label,
            "confidence": composite["confidence"],
            "severity": composite["severity"],
            "priority": composite["priority"],
        }
        recommendation_view = {
            "referral_target": target,
            "treatment_mode": recommendation["treatment_mode"],
            "recommended_scope": recommendation["recommended_scope"],
            "prohibited_actions": recommendation["prohibited_actions"],
        }

        sections = [
            {"code": "SUMMARY", "title": "診断概要", "content": summary},
            {
                "code": "CURRENT_STATE",
                "title": "現在の状態",
                "content": self._current_state(medical_record, composite),
            },
            {
                "code": "DIAGNOSIS",
                "title": "診断",
                "content": f"{label}（信頼度{composite['confidence']}%、優先度{priority}）",
            },
            {
                "code": "WHY",
                "title": "診断理由",
                "content": list(composite.get("reasons", [])),
            },
            {
                "code": "RECOMMENDED_ACTION",
                "title": "推奨する対応",
                "content": {
                    "target": target,
                    "mode": recommendation["treatment_mode"],
                    "scope": recommendation["recommended_scope"],
                },
            },
            {
                "code": "DO_NOT_DO",
                "title": "行わないこと",
                "content": recommendation["prohibited_actions"],
            },
            {
                "code": "MONITORING",
                "title": "今後の確認",
                "content": recommendation["monitoring"],
            },
        ]

        trace = {
            "composite_diagnosis_id": composite["composite_diagnosis_id"],
            "treatment_recommendation_id": recommendation["recommendation_id"],
            "medical_record_event_count": len(medical_record.get("events", [])),
        }
        if audience == "SYSTEM":
            trace["supporting_assessments"] = composite.get(
                "supporting_assessments", []
            )
            trace["referral_request"] = recommendation.get("referral_request")
            sections.append({
                "code": "SYSTEM_TRACE",
                "title": "System Trace",
                "content": {
                    "supporting_assessments": composite.get(
                        "supporting_assessments", []
                    ),
                    "safety": composite.get("safety", {}),
                },
            })

        return {
            "audience": audience,
            "article": article,
            "summary": summary,
            "diagnosis": diagnosis,
            "recommendation": recommendation_view,
            "monitoring": recommendation["monitoring"],
            "sections": sections,
            "trace": trace,
        }

    @staticmethod
    def _summary(label, target, priority):
        if target == "NONE":
            return f"診断結果は「{label}」です。現在、治療は不要です。"
        if target == "OBSERVE":
            return f"診断結果は「{label}」です。優先度{priority}で経過観察します。"
        if target == "FOLLOW_UP":
            return f"診断結果は「{label}」です。追加データ取得後に再診します。"
        return f"診断結果は「{label}」です。{target}への紹介を優先度{priority}で推奨します。"

    @staticmethod
    def _current_state(medical_record, composite):
        scores = [
            item for item in medical_record.get("vital_scores", [])
            if item.get("overall_score") is not None
        ]
        return {
            "vital_score": scores[-1]["overall_score"] if scores else None,
            "risk_score": composite.get("score", {}).get("risk_score"),
            "health_score": composite.get("score", {}).get("health_score"),
            "winner_query_protected": composite.get("safety", {}).get(
                "winner_query_protected", False
            ),
            "recent_change_or_update": composite.get("safety", {}).get(
                "recent_change_or_update", False
            ),
        }
