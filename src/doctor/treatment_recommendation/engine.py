from __future__ import annotations

from typing import Any


class TreatmentRecommendationEngine:
    def __init__(self, policy: dict[str, Any]) -> None:
        self.policy = policy

    def recommend(
        self,
        medical_record: dict[str, Any],
        composite_diagnosis: dict[str, Any],
    ) -> dict[str, Any]:
        final = composite_diagnosis["final_diagnosis"]
        mapping = self.policy["mapping"][final]
        target = mapping["target"]
        mode = mapping["treatment_mode"]
        scope = list(mapping["scope"])
        safety = dict(composite_diagnosis.get("safety", {}))
        reasons = list(composite_diagnosis.get("reasons", []))

        if target == "SIMS_CREATOR" and not safety.get("new_article_allowed"):
            target = "FOLLOW_UP"
            mode = "FOLLOW_UP"
            scope = ["ADDITIONAL_DATA", "REASSESSMENT"]
            reasons.insert(0, "新記事作成の安全条件を満たしていないため再診へ変更しました。")

        if mode == "FULL_REWRITE" and not safety.get("full_rewrite_allowed"):
            target = "SIMS_WRITER"
            mode = "LOCAL_OPTIMIZATION"
            scope = [
                "SEO_TITLE", "META_DESCRIPTION",
                "INTRODUCTION", "HEADINGS", "FAQ"
            ]
            reasons.insert(0, "大規模リライト禁止条件により局所改善へ制限しました。")

        if final == "MERGE_RECOMMENDED" and target != "SIMS_MERGE":
            target = "SIMS_MERGE"
            mode = "MERGE_REVIEW"

        prohibited = [
            "AUTOMATIC_DELETE",
            "AUTOMATIC_NOINDEX",
            "AUTOMATIC_REDIRECT",
            "AUTOMATIC_PUBLICATION",
        ]
        if safety.get("winner_query_protected"):
            prohibited.extend([
                "REMOVE_WINNER_QUERY",
                "AGGRESSIVE_TITLE_CHANGE",
                "FULL_REWRITE",
            ])
        if target != "SIMS_MERGE":
            prohibited.append("MERGE_EXECUTION")
        if target != "SIMS_CREATOR":
            prohibited.append("NEW_ARTICLE_CREATION")

        monitoring = self._monitoring(final, target)
        reasons.insert(
            0,
            f"Composite Diagnosisの{final}を{target}向け紹介へ変換しました。"
        )

        return {
            "referral_target": target,
            "treatment_mode": mode,
            "priority": int(composite_diagnosis.get("priority", 0)),
            "recommended_scope": scope,
            "prohibited_actions": sorted(set(prohibited)),
            "reasons": self._dedupe(reasons),
            "monitoring": monitoring,
            "safety": {
                "doctor_executes_treatment": False,
                "winner_query_protected": bool(
                    safety.get("winner_query_protected")
                ),
                "new_article_allowed": bool(
                    safety.get("new_article_allowed")
                ),
                "full_rewrite_allowed": bool(
                    safety.get("full_rewrite_allowed")
                ),
                "merge_required": bool(safety.get("merge_required")),
            },
            "trace": {
                "composite_diagnosis_id":
                    composite_diagnosis["composite_diagnosis_id"],
                "supporting_assessment_ids": [
                    item.get("assessment_id")
                    for item in composite_diagnosis.get(
                        "supporting_assessments", []
                    )
                    if item.get("assessment_id")
                ],
            },
        }

    @staticmethod
    def _monitoring(final, target):
        if final == "HEALTHY":
            return {
                "required": False,
                "recommended_days": None,
                "metrics": [],
            }
        if target == "OBSERVE":
            return {
                "required": True,
                "recommended_days": 28,
                "metrics": ["CLICKS", "IMPRESSIONS", "CTR", "POSITION"],
            }
        if target == "FOLLOW_UP":
            return {
                "required": True,
                "recommended_days": 14,
                "metrics": ["DATA_COMPLETENESS", "CLICKS", "IMPRESSIONS"],
            }
        return {
            "required": True,
            "recommended_days": 28,
            "metrics": [
                "CLICKS", "IMPRESSIONS", "CTR",
                "POSITION", "VITAL_SCORE"
            ],
        }

    @staticmethod
    def _dedupe(items):
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
