import json
from pathlib import Path

from maintainer_pulse.cli import main


FIXTURE = Path(__file__).parent / "fixtures" / "github_items.json"


def test_cli_writes_markdown_report(tmp_path):
    output = tmp_path / "reports" / "pulse.md"

    exit_code = main(
        [
            "example/project",
            "--input",
            str(FIXTURE),
            "--output",
            str(output),
            "--stale-days",
            "20",
        ]
    )

    assert exit_code == 0
    text = output.read_text(encoding="utf-8")
    assert "# Maintainer Pulse: example/project" in text
    assert "## Release Blockers" in text


def test_cli_writes_json_report(tmp_path):
    output = tmp_path / "pulse.json"

    exit_code = main(
        [
            "example/project",
            "--input",
            str(FIXTURE),
            "--output",
            str(output),
            "--format",
            "json",
        ]
    )

    assert exit_code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["repository"] == "example/project"
    assert "health_score" in payload["metrics"]


def test_cli_writes_csv_report(tmp_path):
    output = tmp_path / "pulse.csv"

    exit_code = main(
        [
            "example/project",
            "--input",
            str(FIXTURE),
            "--output",
            str(output),
            "--format",
            "csv",
            "--stale-days",
            "20",
        ]
    )

    assert exit_code == 0
    text = output.read_text(encoding="utf-8")
    assert text.startswith("queue,number,title,type,state,labels")
    assert "release_blockers,101,Security regression in token refresh,issue,open" in text
    assert "stuck_pull_requests,104,Add release checklist output,pull_request,open" in text
