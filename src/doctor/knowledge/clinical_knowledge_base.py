from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


class KnowledgeValidationError(ValueError):
    pass


@dataclass(frozen=True)
class RegistryItem:
    code: str
    raw: dict[str, Any]


class ClinicalKnowledgeBase:
    REQUIRED_FILES = {
        "manifest": "registry/CKB_MANIFEST.json",
        "observation": "observation/observation_types.json",
        "evidence": "evidence/evidence_codes.json",
        "vital_signs": "vital_signs/vital_signs.json",
        "findings": "findings/finding_codes.json",
        "events": "workflow/medical_record_events.json",
        "evidence_rules": "evidence/rules/evidence_rules_v1.json",
        "vital_formulas": "vital_signs/formulas/vital_sign_formulas_v1.json",
        "finding_rules": "findings/rules/finding_rules_v1.json",
        "diagnosis_codes": "diagnosis/diagnosis_codes.json",
        "differential_rules": "differential/rules/differential_rules_v1.json",
        "final_diagnosis_rules": "diagnosis/rules/final_diagnosis_rules_v1.json",
        "treatment_rules": "treatment/rules/treatment_rules_v1.json",
        "referral_rules": "referral/rules/referral_rules_v1.json",
        "pipeline_policy": "workflow/clinical_pipeline_policy_v1.json",
    }

    def __init__(self, knowledge_root: Path) -> None:
        self.knowledge_root = Path(knowledge_root)
        self._documents: dict[str, dict[str, Any]] = {}

    def load(self) -> "ClinicalKnowledgeBase":
        documents: dict[str, dict[str, Any]] = {}
        for key, relative_path in self.REQUIRED_FILES.items():
            path = self.knowledge_root / relative_path
            if not path.is_file():
                raise KnowledgeValidationError(f"Missing knowledge file: {relative_path}")
            try:
                documents[key] = json.loads(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise KnowledgeValidationError(
                    f"Invalid UTF-8 or JSON in {relative_path}: {exc}"
                ) from exc

        self._documents = documents
        self.validate()
        return self

    def validate(self) -> None:
        if not self._documents:
            raise KnowledgeValidationError("Knowledge base has not been loaded")

        manifest = self._documents["manifest"]
        if manifest.get("knowledge_base") != "SIMS_DOCTOR_CLINICAL_KNOWLEDGE_BASE_V1":
            raise KnowledgeValidationError("Unsupported clinical knowledge base")
        if manifest.get("version") != "1.0":
            raise KnowledgeValidationError("Unsupported CKB version")

        self._validate_unique_codes("observation", "items")
        self._validate_unique_codes("evidence", "items")
        self._validate_unique_codes("vital_signs", "items")
        self._validate_unique_codes("findings", "items")

        vital = self._documents["vital_signs"]
        ranges = vital.get("normal_ranges", [])
        if not ranges:
            raise KnowledgeValidationError("Vital sign normal ranges are missing")
        covered = set()
        for item in ranges:
            minimum = item.get("minimum")
            maximum = item.get("maximum")
            if not isinstance(minimum, int) or not isinstance(maximum, int) or minimum > maximum:
                raise KnowledgeValidationError("Invalid vital sign normal range")
            covered.update(range(minimum, maximum + 1))
        if covered != set(range(0, 101)):
            raise KnowledgeValidationError("Vital sign ranges must cover 0 through 100 exactly")

        finding = self._documents["findings"]
        allowed_levels = set(finding.get("severity_levels", []))
        for item in finding.get("items", []):
            item_levels = set(item.get("allowed_severity", []))
            if not item_levels or not item_levels.issubset(allowed_levels):
                raise KnowledgeValidationError(
                    f"Invalid severity declaration for finding {item.get('code')}"
                )

        rules_doc = self._documents["evidence_rules"]
        rule_codes = [item.get("evidence_code") for item in rules_doc.get("rules", [])]
        known_evidence = self.codes("evidence")
        if not rule_codes or any(code not in known_evidence for code in rule_codes):
            raise KnowledgeValidationError("Evidence rule references unknown evidence code")
        if len(rule_codes) != len(set(rule_codes)):
            raise KnowledgeValidationError("Duplicate evidence rule code")

        vital_formula_codes = [item.get("code") for item in self._documents["vital_formulas"].get("formulas", [])]
        known_vitals = self.codes("vital_signs")
        if set(vital_formula_codes) != known_vitals:
            raise KnowledgeValidationError("Vital formula registry must match Vital Sign registry")

        finding_rule_codes = [item.get("finding_code") for item in self._documents["finding_rules"].get("rules", [])]
        known_findings = self.codes("findings")
        if any(code not in known_findings for code in finding_rule_codes):
            raise KnowledgeValidationError("Finding rule references unknown finding code")
        if len(finding_rule_codes) != len(set(finding_rule_codes)):
            raise KnowledgeValidationError("Duplicate finding rule code")

        diagnosis_codes = [item.get("code") for item in self._documents["diagnosis_codes"].get("items", [])]
        if not diagnosis_codes or len(diagnosis_codes) != len(set(diagnosis_codes)):
            raise KnowledgeValidationError("Invalid diagnosis code registry")
        differential_codes = [item.get("diagnosis_code") for item in self._documents["differential_rules"].get("candidates", [])]
        if any(code not in diagnosis_codes for code in differential_codes):
            raise KnowledgeValidationError("Differential rule references unknown diagnosis code")
        if len(differential_codes) != len(set(differential_codes)):
            raise KnowledgeValidationError("Duplicate differential diagnosis rule")

        final_rules = self._documents["final_diagnosis_rules"].get("diagnoses", [])
        final_candidate_codes = {item.get("candidate_code") for item in final_rules}
        differential_codes_set = set(differential_codes)
        if any(code not in differential_codes_set for code in final_candidate_codes):
            raise KnowledgeValidationError("Final diagnosis rule references unknown candidate code")
        final_codes = {item.get("final_diagnosis_code") for item in final_rules}
        if any(code not in diagnosis_codes for code in final_codes):
            raise KnowledgeValidationError("Final diagnosis rule references unknown diagnosis code")

        treatment_codes = [item.get("diagnosis_code") for item in self._documents["treatment_rules"].get("rules", [])]
        if any(code not in diagnosis_codes for code in treatment_codes):
            raise KnowledgeValidationError("Treatment rule references unknown diagnosis code")
        referral_targets = self._documents["referral_rules"].get("targets", [])
        if not referral_targets or len(referral_targets) != len(set(referral_targets)):
            raise KnowledgeValidationError("Invalid referral target registry")

        events = self._documents["events"].get("items", [])
        if len(events) != len(set(events)):
            raise KnowledgeValidationError("Duplicate medical record event code")

    def _validate_unique_codes(self, document_key: str, item_key: str) -> None:
        items = self._documents[document_key].get(item_key, [])
        codes = [item.get("code") for item in items]
        if not items or any(not isinstance(code, str) or not code for code in codes):
            raise KnowledgeValidationError(f"Missing code in {document_key} registry")
        if len(codes) != len(set(codes)):
            raise KnowledgeValidationError(f"Duplicate code in {document_key} registry")

    def codes(self, registry: str) -> set[str]:
        if registry not in {"observation", "evidence", "vital_signs", "findings"}:
            raise KeyError(registry)
        return {item["code"] for item in self._documents[registry]["items"]}

    def is_known_code(self, registry: str, code: str) -> bool:
        return code in self.codes(registry)

    def evidence_rules(self) -> dict[str, dict[str, Any]]:
        return {
            item["evidence_code"]: item
            for item in self._documents["evidence_rules"]["rules"]
        }

    def sample_policy(self) -> dict[str, Any]:
        return dict(self._documents["evidence_rules"]["sample_policy"])

    def vital_formulas(self) -> dict[str, dict[str, Any]]:
        return {
            item["code"]: item
            for item in self._documents["vital_formulas"]["formulas"]
        }

    def vital_global_policy(self) -> dict[str, Any]:
        return dict(self._documents["vital_formulas"]["global_policy"])

    def finding_rules(self) -> dict[str, dict[str, Any]]:
        return {
            item["finding_code"]: item
            for item in self._documents["finding_rules"]["rules"]
        }

    def finding_global_policy(self) -> dict[str, Any]:
        return dict(self._documents["finding_rules"]["global_policy"])

    def diagnosis_codes(self) -> set[str]:
        return {item["code"] for item in self._documents["diagnosis_codes"]["items"]}

    def differential_rules(self) -> dict[str, dict[str, Any]]:
        return {
            item["diagnosis_code"]: item
            for item in self._documents["differential_rules"]["candidates"]
        }

    def differential_global_policy(self) -> dict[str, Any]:
        return dict(self._documents["differential_rules"]["global_policy"])

    def final_diagnosis_rules(self) -> dict[str, dict[str, Any]]:
        return {item["candidate_code"]: item for item in self._documents["final_diagnosis_rules"]["diagnoses"]}

    def final_diagnosis_global_policy(self) -> dict[str, Any]:
        return dict(self._documents["final_diagnosis_rules"]["global_policy"])

    def treatment_rules(self) -> list[dict[str, Any]]:
        return list(self._documents["treatment_rules"]["rules"])

    def deferred_treatment_rules(self) -> list[dict[str, Any]]:
        return list(self._documents["treatment_rules"]["deferred_rules"])

    def referral_targets(self) -> set[str]:
        return set(self._documents["referral_rules"]["targets"])

    def referral_policies(self) -> dict[str, Any]:
        return dict(self._documents["referral_rules"]["policies"])

    def pipeline_policy(self) -> dict[str, Any]:
        return dict(self._documents["pipeline_policy"])

    def classify_vital_score(self, score: int) -> str:
        if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 100:
            raise ValueError("Vital score must be an integer from 0 to 100")
        for item in self._documents["vital_signs"]["normal_ranges"]:
            if item["minimum"] <= score <= item["maximum"]:
                return item["classification"]
        raise KnowledgeValidationError("No classification found for score")
