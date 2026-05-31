# Real-World Example Reports

These reports show Maintainer Pulse running against live public GitHub issue and
pull request metadata.

The examples are snapshots, not official assessments of the listed projects.
They are generated with a small `--max-pages` value so the files stay readable in
the repository. For a full maintenance session, maintainers should choose a page
depth that matches their repository size.

## Included Reports

| Repository | Report |
| --- | --- |
| `pallets/flask` | [pallets-flask.md](pallets-flask.md) |
| `psf/requests` | [psf-requests.md](psf-requests.md) |
| `pytest-dev/pytest` | [pytest-dev-pytest.md](pytest-dev-pytest.md) |

## Rebuild

```bash
export GITHUB_TOKEN=github_pat_your_token_here
maintainer-pulse psf/requests --output examples/real-world/psf-requests.md --max-pages 2
maintainer-pulse pallets/flask --output examples/real-world/pallets-flask.md --max-pages 2
maintainer-pulse pytest-dev/pytest --output examples/real-world/pytest-dev-pytest.md --max-pages 2
```

