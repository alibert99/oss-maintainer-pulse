from pathlib import Path


ACTION = Path(__file__).parents[1] / "action.yml"


def test_action_metadata_exposes_core_inputs():
    text = ACTION.read_text(encoding="utf-8")

    assert "using: composite" in text
    assert "github-token:" in text
    assert "stale-days:" in text
    assert "ai-summary:" in text
    assert "openai-api-key:" in text
    assert "--ai-summary" in text
    assert "report-path:" in text
    assert "maintainer-pulse" in text
