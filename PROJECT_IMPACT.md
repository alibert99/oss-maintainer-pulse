# Project Impact

Maintainer Pulse is an open-source maintenance assistant for projects that need
better issue and pull request visibility without adding a hosted service or a bot
with write permissions.

## Problem

Many open-source projects accumulate review debt because maintainers have to scan
issues, pull requests, labels, milestones, comments, and timestamps by hand. That
manual scan is slow, easy to postpone, and hard to hand off to new contributors.

Maintainer Pulse turns that scan into a repeatable report that answers a focused
question: what should a maintainer look at first?

## Maintainer Value

- Release planning: group release blockers and security/regression-labeled work.
- Pull request review: find PRs idle for seven or more days or marked for review.
- Community response: surface open items with no maintainer response.
- Queue hygiene: identify items idle past the stale threshold.
- Contributor onboarding: list small labeled issues that are likely quick wins.
- Duplicate review: surface likely duplicate issue pairs from similar titles.
- Optional AI support: generate a concise maintainer agenda when a maintainer
  explicitly enables the OpenAI summary feature.

The report is deterministic and reviewable. Maintainers can see the exact labels,
timestamps, and thresholds that caused an item to appear in a queue.

## Current Evidence

- Distributed as a Python package on PyPI.
- Distributed as a reusable GitHub Action.
- CI covers Python 3.10, 3.11, and 3.12.
- Package build checks run in GitHub Actions.
- The repository includes issue templates, a pull request template, a security
  policy, contribution guidelines, releases, and generated examples.
- Real-world example reports are kept in
  [examples/real-world](examples/real-world).

## Adoption Plan

The project is early. The next goal is to collect feedback from maintainers with
busy queues and convert that feedback into small, auditable scoring changes.

Near-term adoption work:

- Publish the GitHub Action listing.
- Share the project with Python and open-source maintainer communities.
- Add more real-world reports from public repositories.
- Document maintainer feedback as issues with labels and milestones.
- Keep releases tied to visible roadmap items.

## Responsible Automation

Maintainer Pulse is read-only by default. It does not comment on issues, label
items, close issues, merge pull requests, or write to a repository unless a future
feature is explicitly designed and enabled by the maintainer.

Optional AI-assisted summaries are available as an opt-in feature. Any AI-backed
feature should preserve these rules:

- No API calls unless a maintainer provides an API key.
- No hidden writes to GitHub.
- Reports must identify which output is deterministic and which output is
  generated assistance.
- Maintainers keep final judgment over release and triage decisions.
