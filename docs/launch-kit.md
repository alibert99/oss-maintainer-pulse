# Launch Kit

Maintainer Pulse needs real maintainer feedback. Use this copy when sharing the
project in developer communities.

Project links:

- GitHub: <https://github.com/alibert99/oss-maintainer-pulse>
- PyPI: <https://pypi.org/project/oss-maintainer-pulse/>
- Latest release: <https://github.com/alibert99/oss-maintainer-pulse/releases/latest>

## Short Post

```text
I built Maintainer Pulse, an offline-first CLI and GitHub Action for OSS
maintainers.

It turns GitHub issue/PR metadata into a weekly report:
- release blockers grouped by milestone
- stuck pull requests
- issues needing first response
- stale queue
- good first issue quick wins

Install:
pip install oss-maintainer-pulse

GitHub Action:
uses: alibert99/oss-maintainer-pulse@v0.1.5

Feedback from maintainers with busy issue queues would be useful:
https://github.com/alibert99/oss-maintainer-pulse
```

## Show HN Draft

Title:

```text
Show HN: Maintainer Pulse, a GitHub issue and PR health report for maintainers
```

Body:

```text
I built Maintainer Pulse because maintainers often need a quick answer to:
what should I review before the next release?

It is a no-runtime-dependency Python CLI and reusable GitHub Action. It reads
GitHub issue/PR metadata and generates Markdown, HTML, JSON, or CSV reports with:

- release blockers grouped by milestone
- stuck pull requests
- first-response debt
- stale issues/PRs
- contributor-friendly quick wins

It is installable from PyPI:
pip install oss-maintainer-pulse

It can also run weekly as a GitHub Action and upload the report artifact.

Repo:
https://github.com/alibert99/oss-maintainer-pulse

I would like feedback from maintainers with real issue queues, especially on
which signals should be added or removed.
```

## Reddit / Dev.to Draft

```text
I made a small OSS maintainer tool: Maintainer Pulse.

It is a Python CLI and GitHub Action that generates issue/PR health reports for
open-source repositories. The report shows release blockers, stuck PRs, stale
items, issues that never got a maintainer response, and good-first-issue quick
wins. Markdown reports also group release blockers by GitHub milestone.

Install:
pip install oss-maintainer-pulse

Example:
maintainer-pulse owner/repo --format markdown --output maintainer-pulse-report.md

GitHub Action:
uses: alibert99/oss-maintainer-pulse@v0.1.5

I am looking for maintainer feedback and real repos to test against:
https://github.com/alibert99/oss-maintainer-pulse
```

## Where To Share

- Hacker News: Show HN.
- Reddit: `r/opensource`, `r/github`, `r/Python`.
- Dev.to or Hashnode: publish the long version with the terminal preview image.
- X / LinkedIn: use the short post.
- Python and OSS maintainer Discord/Slack communities where self-promotion is
  allowed.

## What To Ask For

- Maintainer feedback on the queue logic.
- Real issue/PR payload examples.
- Repositories willing to try the scheduled GitHub Action.
- Feature requests for release planning and review queues.

## What Not To Do

- Do not buy stars.
- Do not use star-exchange groups.
- Do not claim adoption that does not exist.
- Do not ask people to star unless they find the project useful.

