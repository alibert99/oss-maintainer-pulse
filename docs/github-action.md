# GitHub Action

Maintainer Pulse can run as a scheduled repository health report. The action
fetches open and closed issues from GitHub, scores the maintenance queue, writes
a report artifact, and can append the Markdown report to the workflow summary.

## Example Workflow

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
      - uses: alibert99/oss-maintainer-pulse@v0.1.4
        id: pulse
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          output: maintainer-pulse-report.md
      - uses: actions/upload-artifact@v7
        with:
          name: maintainer-pulse-report
          path: ${{ steps.pulse.outputs.report-path }}
```

## Inputs

| Input | Default | Description |
| --- | --- | --- |
| `repository` | current repo | Repository to analyze as `owner/name`. |
| `github-token` | empty | Token for GitHub API requests. |
| `input-json` | empty | Offline JSON payload to analyze instead of calling GitHub. |
| `format` | `markdown` | Report format: `markdown`, `html`, `json`, or `csv`. |
| `output` | `maintainer-pulse-report.md` | Report output path. |
| `stale-days` | `30` | Idle-day threshold for stale items. |
| `max-pages` | `2` | Maximum GitHub API pages to fetch. |
| `summary` | `true` | Append Markdown reports to the job summary. |
