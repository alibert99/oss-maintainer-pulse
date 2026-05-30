# Maintainer Pulse

Maintainer Pulse turns GitHub issue and pull request data into a short, actionable
maintenance report. It is built for open-source maintainers who need to answer:

- What should I review before the next release?
- Which pull requests are stuck?
- Which issues have not received a maintainer response?
- What can a new contributor safely pick up?

The tool is offline-first. You can run it against exported GitHub JSON without a
token, or fetch live issue and pull request data from the GitHub API.

[![CI](https://github.com/alibert99/oss-maintainer-pulse/actions/workflows/ci.yml/badge.svg)](https://github.com/alibert99/oss-maintainer-pulse/actions/workflows/ci.yml)
[![Maintainer Pulse](https://github.com/alibert99/oss-maintainer-pulse/actions/workflows/maintainer-pulse.yml/badge.svg)](https://github.com/alibert99/oss-maintainer-pulse/actions/workflows/maintainer-pulse.yml)

## Features

- Release blocker, stuck pull request, stale item, first-response, and quick-win queues.
- Markdown, HTML, and JSON output.
- Reusable GitHub Action for scheduled reports.
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

See [examples/sample-report.md](examples/sample-report.md) for a generated report.

## GitHub Action

Run Maintainer Pulse weekly and upload a report artifact:

```yaml
name: Maintainer Pulse

on:
  workflow_dispatch:
  schedule:
    - cron: "17 9 * * 1"

permissions:
  contents: read
  issues: read
  pull-requests: read

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: alibert99/oss-maintainer-pulse@v0.1.0
        id: pulse
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          output: maintainer-pulse-report.md
      - uses: actions/upload-artifact@v4
        with:
          name: maintainer-pulse-report
          path: ${{ steps.pulse.outputs.report-path }}
```

See [docs/github-action.md](docs/github-action.md) for all inputs.

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
