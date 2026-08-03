from __future__ import annotations

from typing import Any


DIAGNOSIS_LABELS = {
    "CTR_PROBLEM": "検索結果でクリックされにくい状態です",
    "POSITION_DECLINE": "検索順位と表示機会が低下しています",
    "CONTENT_STALE": "記事情報の鮮度不足が確認されました",
    "UPDATE_FAILURE": "前回の改善後も回復が確認できません",
    "CANNIBALIZATION": "同じ検索需要を複数記事が取り合っている可能性があります",
    "ARTICLE_MERGE_REQUIRED": "内容が重複する記事の統合を検討すべき状態です",
    "NEW_ARTICLE_NEEDED": "既存記事とは異なる検索意図の記事が必要です",
}

DEFER_LABELS = {
    "LOW_SAMPLE_ONLY": "データが少ないため、現時点では診断を確定できません",
    "CLOSE_CANDIDATES": "複数の原因が拮抗しているため、追加観察が必要です",
    "LOW_CONFIDENCE": "診断の確度が不足しているため、経過観察が必要です",
    "MISSING_EVIDENCE": "診断に必要なデータが不足しています",
    "MISSING_FINDINGS": "診断に必要な所見が不足しています",
    "MISSING_CONTEXT": "改善履歴などの確認が必要です",
    "CONTRADICTION": "判断材料に矛盾があるため、診断を保留します",
    "NO_CANDIDATE": "明確な異常パターンを特定できませんでした",
    "INSUFFICIENT_DATA": "診断に十分なデータがありません",
}

TREATMENT_LABELS = {
    "REWRITE_SNIPPET_AND_INTENT_ALIGNMENT": "Writerでタイトル・説明文・検索意図の整合を見直します",
    "REWRITE_CONTENT_RECOVERY": "Writerで順位回復を目的とした部分改善を行います",
    "REFRESH_OUTDATED_CONTENT": "Writerで古い情報を確認し、必要部分を更新します",
    "REASSESS_FAILED_TREATMENT": "Writerで前回改善の影響を確認し、再治療方針を立てます",
    "OBSERVATION_ONLY": "現時点では記事を変更せず、データを蓄積します",
    "ADDITIONAL_OBSERVATION": "追加データを取得して再診します",
    "COLLECT_MISSING_EVIDENCE": "不足している診断材料を収集します",
    "COLLECT_TREATMENT_HISTORY": "過去の改善履歴を確認して再診します",
    "MANUAL_REVIEW": "矛盾する情報を確認してから再診します",
    "REVIEW_QUERY_CONFLICT": "Mergeでクエリ競合と統合可否を確認します",
    "MERGE_OVERLAPPING_ARTICLES": "Mergeで重複記事の統合設計を行います",
    "CREATE_DISTINCT_INTENT_ARTICLE": "Creatorで別の検索意図に対応する新記事を作成します",
}


class DiagnosisReportBuilder:
    def build(self, medical_record: dict[str, Any]) -> dict[str, Any]:
        diagnoses = medical_record.get("final_diagnoses", [])
        if not diagnoses:
            return {
                "headline": "診断を完了できませんでした",
                "summary": "確定診断または診断保留の記録がありません。",
                "reasons": [],
                "next_action": "診療処理を再実行してください。",
                "attention": "システム管理者による確認が必要です。",
            }

        diagnosis = diagnoses[-1]
        treatment = (
            medical_record.get("treatment_recommendations", [])[-1]
            if medical_record.get("treatment_recommendations")
            else None
        )
        findings_by_id = {
            item["finding_id"]: item for item in medical_record.get("findings", [])
        }
        reasons = [
            self._finding_reason(findings_by_id[item_id])
            for item_id in diagnosis.get("supporting_finding_ids", [])
            if item_id in findings_by_id
        ][:5]

        if diagnosis["status"] == "CONFIRMED":
            headline = DIAGNOSIS_LABELS.get(
                diagnosis["diagnosis_code"], "記事に改善が必要な状態です"
            )
            summary = self._confirmed_summary(diagnosis)
            next_action = (
                TREATMENT_LABELS.get(treatment["treatment_code"], "紹介先で治療方針を確認します")
                if treatment else "治療方針を作成してください。"
            )
            attention = None
        else:
            headline = "診断は保留です"
            summary = DEFER_LABELS.get(
                diagnosis.get("defer_reason"), "追加観察後に再診します"
            )
            next_action = (
                TREATMENT_LABELS.get(treatment["treatment_code"], "追加データを取得します")
                if treatment else "再診日までデータを蓄積してください。"
            )
            attention = "診断が確定するまで、記事の大幅な変更は行わないでください。"

        return {
            "headline": headline,
            "summary": summary,
            "reasons": reasons,
            "next_action": next_action,
            "attention": attention,
        }

    @staticmethod
    def _confirmed_summary(diagnosis: dict[str, Any]) -> str:
        confidence = diagnosis.get("confidence")
        severity = diagnosis.get("severity")
        parts = ["診断を確定しました。"]
        if confidence is not None:
            parts.append(f"診断信頼度は{confidence}%です。")
        if severity:
            parts.append(f"重症度は{severity}です。")
        return "".join(parts)

    @staticmethod
    def _finding_reason(finding: dict[str, Any]) -> str:
        labels = {
            "CTR_UNDERPERFORMING": "掲載順位に対してクリック率が低い状態です。",
            "HIGH_VISIBILITY_LOW_CLICK": "表示機会はあるもののクリックにつながっていません。",
            "POSITION_DECLINING": "比較期間で平均順位の低下が確認されました。",
            "LOW_VISIBILITY": "表示回数の減少が確認されました。",
            "CONTENT_OUTDATED": "最終更新から長期間が経過しています。",
            "INSUFFICIENT_EVIDENCE": "利用できるデータ量が不足しています。",
            "QUERY_OVERLAP_HIGH": "複数記事で同じクエリの重複が確認されました。",
            "MERGE_SUITABILITY_HIGH": "記事内容と検索意図の重複度が高い状態です。",
            "DISTINCT_INTENT_OPPORTUNITY": "既存記事と異なる検索意図が確認されました。",
        }
        return labels.get(finding["finding_code"], "診断に関連する所見が確認されました。")
