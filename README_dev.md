# Development

Setup and running are in [README.md](README.md).

## Checking

Run `ruff check` or get the vscode ruff extension, the rules are defined in pyproject.toml.

## Type Checking

Run `ty check`

## Testing

Run `pytest`, it will get its config from pyproject.toml

`scripts/run-ci-local.sh` runs the lot: ty, ruff and pytest.

## Test Coverage

```bash
scripts/run-coverage.sh
python -m http.server -b 127.0.0.1 8000 -d htmlcov
```

## Workflows

The '.github' folder has Check, Type Check and Test workflows.

To get the workflow passing badges on your repo, have a look at <https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge>
