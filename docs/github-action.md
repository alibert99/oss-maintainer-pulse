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
      - uses: alibert99/oss-maintainer-pulse@v0.1.5
        id: pulse
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          output: maintainer-pulse-report.md
      - uses: actions/upload-artifact@v7
        with:
          name: maintainer-pulse-report
          path: ${{ steps.pulse.outputs.report-path }}
```

## Optional AI Summary

AI summaries are disabled by default. To enable them, pass an OpenAI API key from
repository secrets and set `ai-summary` to `true`.

```yaml
name: Maintainer Pulse

on:
  workflow_dispatch:

permissions:
  contents: read
  issues: read
  pull-requests: read

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: alibert99/oss-maintainer-pulse@v0.1.5
        id: pulse
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          ai-summary: "true"
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          openai-model: gpt-5-mini
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
| `format` | `markdown` | Report format: `markdown`, `html`, `json`, or `csv`. Markdown release blockers are grouped by milestone when available. |
| `output` | `maintainer-pulse-report.md` | Report output path. |
| `stale-days` | `30` | Idle-day threshold for stale items. |
| `max-pages` | `2` | Maximum GitHub API pages to fetch. |
| `summary` | `true` | Append Markdown reports to the job summary. |
| `ai-summary` | `false` | Generate an optional OpenAI maintainer summary. |
| `openai-api-key` | empty | OpenAI API key used only when `ai-summary` is `true`. |
| `openai-model` | `gpt-5-mini` | OpenAI model for optional summaries. |
| `openai-timeout` | `30` | OpenAI API timeout in seconds. |
