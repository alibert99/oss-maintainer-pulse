# Optional AI Summaries

Maintainer Pulse can add an OpenAI-generated maintainer summary to Markdown,
HTML, and JSON reports. This feature is disabled by default.

The deterministic report still runs without an API key. Maintainer Pulse only
calls OpenAI when `--ai-summary` is present.

## CLI Usage

```bash
export OPENAI_API_KEY=sk_your_key_here
maintainer-pulse owner/repo \
  --ai-summary \
  --openai-model gpt-5-mini \
  --output maintainer-pulse-report.md
```

Useful flags:

| Flag | Default | Description |
| --- | --- | --- |
| `--ai-summary` | off | Enables the OpenAI summary call. |
| `--openai-model` | `gpt-5-mini` | Model used for the summary. |
| `--openai-api-key-env` | `OPENAI_API_KEY` | Environment variable containing the API key. |
| `--openai-timeout` | `30` | OpenAI API timeout in seconds. |

## What Gets Sent

The request includes the generated Maintainer Pulse report data: metrics, queue
items, recommendations, and duplicate candidates. It does not send source code,
repository contents, secrets, comments beyond GitHub's comment counts, or write
any data back to GitHub.

## Output

The AI summary is labeled in the report with provider and model metadata. It is
advisory and should be verified by a maintainer before any release, triage, or
close decision.

## Boundaries

- No API call happens unless `--ai-summary` is explicitly set.
- No OpenAI dependency is installed; the integration uses the Python standard
  library.
- No GitHub write permission is required.
- No issue comments, labels, closures, or merges are performed.
- The deterministic queues remain available even if the AI call is not used.
