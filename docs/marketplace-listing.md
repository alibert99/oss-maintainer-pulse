# GitHub Marketplace Listing Draft

Maintainer Pulse is ready to list as a GitHub Action because the repository has
a root `action.yml`, branding metadata, usage docs, and versioned releases.

## Name

Maintainer Pulse

## Short Description

Generate issue and pull request health reports for open-source maintainers.

## Categories

- Project management
- Code review
- Utilities

## Listing Description

Maintainer Pulse helps maintainers see what needs attention before the next
release. It reads GitHub issue and pull request metadata, scores queue health,
and writes Markdown, HTML, or JSON reports.

Use it to surface release blockers, stuck pull requests, issues with no
maintainer response, stale items, and contributor-friendly quick wins. It can run
as a scheduled GitHub Action or as an offline-first CLI against exported GitHub
JSON.

## Example

```yaml
- uses: alibert99/oss-maintainer-pulse@v0.1.2
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    output: maintainer-pulse-report.md
```

## Release Checklist

- Confirm `action.yml` is valid and has branding.
- Confirm README includes a workflow example.
- Publish a semantic version tag.
- Create a GitHub release for that tag.
- In the GitHub repository UI, open the release and choose the Marketplace
  publishing option if available for the action.
