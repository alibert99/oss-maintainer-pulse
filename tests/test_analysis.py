from dataclasses import replace
from datetime import datetime, timezone
import json

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
    assert pulse.queues["release_blockers"][0].milestone_title == "v1.0"
    assert pulse.queues["quick_wins"][0].number == 102
    assert pulse.duplicate_candidates == []


def test_analyze_detects_likely_duplicate_issues():
    items = load_items("tests/fixtures/github_items.json")
    duplicate = replace(
        items[2],
        number=106,
        title="Installer failure has no response",
        html_url="https://github.com/example/project/issues/106",
    )

    pulse = analyze([*items, duplicate], "example/project", stale_days=20, now=NOW)

    assert len(pulse.duplicate_candidates) == 1
    candidate = pulse.duplicate_candidates[0]
    assert {candidate.first.number, candidate.second.number} == {103, 106}
    assert candidate.similarity >= 0.5
    assert "installer" in candidate.shared_terms


def test_markdown_report_contains_actionable_sections():
    items = load_items("tests/fixtures/github_items.json")
    pulse = analyze(items, "example/project", stale_days=20, now=NOW)

    rendered = render_markdown(pulse)

    assert "# Maintainer Pulse: example/project" in rendered
    assert "## Release Blockers" in rendered
    assert "### v1.0" in rendered
    assert "#101 Security regression" in rendered
    assert "Recommended Maintainer Block" in rendered
    assert "## Duplicate Candidates" in rendered


def test_markdown_report_contains_duplicate_candidates():
    items = load_items("tests/fixtures/github_items.json")
    duplicate = replace(
        items[2],
        number=106,
        title="Installer failure has no response",
        html_url="https://github.com/example/project/issues/106",
    )
    pulse = analyze([*items, duplicate], "example/project", stale_days=20, now=NOW)

    rendered = render_markdown(pulse)

    assert "## Duplicate Candidates" in rendered
    assert "#103 No response on installer failure" in rendered
    assert "#106 Installer failure has no response" in rendered


def test_json_report_is_serializable():
    items = load_items("tests/fixtures/github_items.json")
    pulse = analyze(items, "example/project", stale_days=20, now=NOW)

    rendered = render_json(pulse)

    payload = json.loads(rendered)
    assert "health_score" in payload["metrics"]
    assert payload["queues"]["release_blockers"][0]["milestone_title"] == "v1.0"
    assert "release_blockers" in payload["queues"]
    assert payload["duplicate_candidates"] == []
