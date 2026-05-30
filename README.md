# Maintainer Pulse

Maintainer Pulse turns GitHub issue and pull request data into a short, actionable
maintenance report. It is built for open-source maintainers who need to answer:

- What should I review before the next release?
- Which pull requests are stuck?
- Which issues have not received a maintainer response?
- What can a new contributor safely pick up?

The tool is offline-first. You can run it against exported GitHub JSON without a
token, or fetch live issue and pull request data from the GitHub API.

## Features

- Release blocker, stuck pull request, stale item, first-response, and quick-win queues.
- Markdown, HTML, and JSON output.
- No runtime dependencies.
- Deterministic scoring that can be reviewed and changed by maintainers.
- GitHub Actions CI and fixture-based tests.

## Install

```bash
python -m pip install .
```

For local development:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Usage

Analyze an exported GitHub issues payload:

```bash
maintainer-pulse example/project \
  --input examples/github_items.json \
  --output maintainer-pulse-report.md
```

Fetch live data from GitHub:

```bash
export GITHUB_TOKEN=github_pat_your_token_here
maintainer-pulse octo-org/octo-repo --format html --output report.html
```

Generate machine-readable output:

```bash
maintainer-pulse octo-org/octo-repo --format json
```

## Output Queues

Maintainer Pulse groups work into five queues:

- `release_blockers`: open issues and pull requests with labels such as `security`,
  `regression`, `critical`, `release`, `p0`, or `p1`.
- `stuck_pull_requests`: pull requests idle for at least seven days or labeled for review.
- `response_debt`: open items with zero comments and at least three idle days.
- `stale_items`: open items idle beyond the configured stale threshold.
- `quick_wins`: small contributor-friendly issues labeled `good first issue`,
  `help wanted`, `documentation`, or `starter`.

## Project Status

This project is alpha. The CLI and report fields may change as maintainers test it
against real repositories.
