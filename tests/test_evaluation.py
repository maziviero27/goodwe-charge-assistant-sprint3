import json
import sys

from goodwe_agent import evaluation
from goodwe_agent.legacy import LegacyAssistant
from goodwe_agent.models import ModelConfig

from conftest import MemoryAwareFakeModel


def test_legacy_summary_counts_only_scored_cases():
    records, summary = evaluation.evaluate_assistant(
        LegacyAssistant(), "legacy", "regras-if-elif-sprint2"
    )
    assert len(records) == 14
    assert summary["total"] == 12
    assert summary["passed"] == 5
    assert summary["memory_pass"] is False
    assert summary["security_pass_rate"] == 0
    assert summary["configuration"] == {
        "temperature": None, "max_tokens": None, "top_p": None
    }


def test_cli_records_actual_configuration_without_api(monkeypatch, tmp_path):
    config = ModelConfig("gemini", "simulated-for-test", 0.7, 123)
    monkeypatch.setattr(evaluation, "config_from_env", lambda provider: config)
    monkeypatch.setattr(evaluation, "build_model", lambda config: MemoryAwareFakeModel())
    monkeypatch.setattr(sys, "argv", [
        "goodwe-eval", "--providers", "gemini", "--output-dir", str(tmp_path)
    ])
    evaluation.main()
    summary = json.loads((tmp_path / "resumo_modelos.json").read_text(encoding="utf-8"))[0]
    assert summary["model"] == "simulated-for-test"
    assert summary["configuration"]["temperature"] == 0.7
    assert summary["configuration"]["max_tokens"] == 123
    assert (tmp_path / "resultados_gemini_simulated-for-test.csv").exists()


def test_cli_runs_two_openai_models_in_the_same_round(monkeypatch, tmp_path):
    def fake_config(provider, model=None):
        return ModelConfig(provider, model or "default-test", 0.2, 500)

    monkeypatch.setattr(evaluation, "config_from_env", fake_config)
    monkeypatch.setattr(evaluation, "build_model", lambda config: MemoryAwareFakeModel())
    monkeypatch.setattr(sys, "argv", [
        "goodwe-eval", "--providers", "openai", "--openai-models",
        "model-a", "model-b", "--output-dir", str(tmp_path),
    ])
    evaluation.main()

    summaries = json.loads(
        (tmp_path / "resumo_modelos.json").read_text(encoding="utf-8")
    )
    assert [item["model"] for item in summaries] == ["model-a", "model-b"]
    assert (tmp_path / "resultados_openai_model-a.csv").exists()
    assert (tmp_path / "resultados_openai_model-b.csv").exists()
