from pathlib import Path
import json

from src.doctor.diagnostic_rules import DiagnosticRuleRegistry


ROOT = Path(__file__).resolve().parents[2]


def test_loads_rule_registry():
    registry = DiagnosticRuleRegistry.from_file(
        ROOT / "knowledge/diagnostic_rules/core_diagnostic_rules_v1.json"
    )
    assert len(registry.enabled_rules()) == 3
    assert registry.enabled_rules()[0].rule_id == "DR-CTR-001"
