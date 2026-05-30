# PyPI Publishing

Maintainer Pulse is packaged as `oss-maintainer-pulse`.

## Local Build Check

```bash
python -m pip install -e ".[dev]"
python -m build
python -m twine check dist/*
```

## Trusted Publishing Setup

Use PyPI trusted publishing instead of storing a long-lived API token in GitHub.

1. Create the project on PyPI as `oss-maintainer-pulse`.
2. Add a trusted publisher for this GitHub repository:
   - Owner: `alibert99`
   - Repository: `oss-maintainer-pulse`
   - Workflow: `publish-pypi.yml`
   - Environment: `pypi`
3. In GitHub, create the `pypi` environment.
4. Run the `Publish to PyPI` workflow for a tagged release such as `v0.1.3`.

The workflow is manual on purpose so package publishing does not fail before
trusted publishing is configured.
