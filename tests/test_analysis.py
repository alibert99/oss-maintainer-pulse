from datetime import datetime, timezone

from maintainer_pulse.analysis import analyze
from maintainer_pulse.github import load_items
from maintainer_pulse.report import render_json, render_markdown


NOW = datetime(2026, 5, 30, 12, 0, tzinfo=timezone.utc)


def test_analyze_prioritizes_maintenance_queues():
    items = load_items("tests/fixtures/github_items.json")

    pulse = analyze(items, "example/project", stale_days=20, now=NOW)

    assert pulse.metrics.open_issues == 3
    assert pulse.metrics.open_pull_requests == 1
    assert pulse.metrics.release_blockers == 1
    assert pulse.metrics.response_debt == 1
    assert pulse.metrics.stuck_pull_requests == 1
    assert pulse.metrics.stale_items == 2
    assert pulse.queues["release_blockers"][0].number == 101
    assert pulse.queues["quick_wins"][0].number == 102


def test_markdown_report_contains_actionable_sections():
    items = load_items("tests/fixtures/github_items.json")
    pulse = analyze(items, "example/project", stale_days=20, now=NOW)

    rendered = render_markdown(pulse)

    assert "# Maintainer Pulse: example/project" in rendered
    assert "## Release Blockers" in rendered
    assert "#101 Security regression" in rendered
    assert "Recommended Maintainer Block" in rendered


def test_json_report_is_serializable():
    items = load_items("tests/fixtures/github_items.json")
    pulse = analyze(items, "example/project", stale_days=20, now=NOW)

    rendered = render_json(pulse)

    assert '"health_score"' in rendered
    assert '"release_blockers"' in rendered
