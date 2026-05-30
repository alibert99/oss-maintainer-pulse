# PyPI Publishing

Maintainer Pulse is published as `oss-maintainer-pulse`:

<https://pypi.org/project/oss-maintainer-pulse/>

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
4. Run the `Publish to PyPI` workflow for a tagged release such as `v0.1.5`.

Trusted publishing is configured for this repository. The workflow is manual on
purpose so maintainers control exactly which tag is uploaded.
