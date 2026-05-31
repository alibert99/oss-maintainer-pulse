# Maintainer Workflows

Maintainer Pulse is designed around short, repeatable maintenance sessions. The
report should tell a maintainer where to start, not make decisions for them.

## Weekly Triage

Run the GitHub Action every week and upload the Markdown report as an artifact.
Use the recommended maintainer block as the agenda for a short triage session.

Good outcomes:

- Every release blocker is either assigned, fixed, or explicitly deferred.
- Stuck pull requests get a review, a question, or a close decision.
- Items with no response get a first maintainer reply.
- Stale items are relabeled, revived, or closed.

## Release Planning

Before a release, run a report with the repository's normal stale threshold. Start
with the release blocker queue and review milestone grouping in the Markdown
output.

Useful checks:

- Security, regression, critical, `p0`, and `p1` labels are surfaced.
- Release blockers without milestones are visible under `No milestone`.
- The CSV output can be imported into a release checklist or spreadsheet.

## Contributor Onboarding

Use the quick-wins queue when new contributors ask where to start. The queue looks
for open issues labeled `good first issue`, `help wanted`, `documentation`, or
`starter` with low comment volume.

Before sharing an item with a contributor, maintainers should still verify that:

- The issue is still valid.
- The scope is small enough for a first contribution.
- The expected solution is clear enough to review.

## Offline Review

For private audits or reproducible tests, export GitHub issue data and run the
CLI with `--input`. In this mode, Maintainer Pulse does not call the GitHub API.

```bash
maintainer-pulse owner/repo \
  --input exported-github-items.json \
  --output maintainer-pulse-report.md
```

## Automation Boundaries

Maintainer Pulse should be safe to run in public CI:

- It only needs read permissions for issues and pull requests.
- It does not require a hosted backend.
- It does not require runtime dependencies.
- It does not write comments, labels, or repository changes.

Future write-capable features should be separate opt-in workflows with clear
permissions and tests.

