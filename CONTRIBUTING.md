# Contributing

Thanks for improving Maintainer Pulse. The project is intentionally small and
dependency-light, so changes should keep the command easy to audit and run in CI.

## Local Setup

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Pull Request Guidelines

- Add or update tests for queueing, scoring, and rendering behavior.
- Keep GitHub API handling in `src/maintainer_pulse/github.py`.
- Keep report formatting in `src/maintainer_pulse/report.py`.
- Avoid adding runtime dependencies unless they remove substantial complexity.

## Good First Contributions

- Add report examples for real public repositories.
- Improve label matching for common maintainer workflows.
- Add CSV output for teams that track triage in spreadsheets.

