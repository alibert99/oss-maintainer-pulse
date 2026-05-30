# Security

Maintainer Pulse reads GitHub issue and pull request metadata and can optionally
send authenticated requests to the GitHub API. It does not need repository write
permissions.

## Reporting a Vulnerability

Please open a private security advisory on GitHub if the repository supports it,
or email the maintainer listed in the repository profile.

## Token Handling

- Prefer a read-only GitHub token.
- Pass tokens through environment variables.
- Do not commit generated reports if they include private repository metadata.

