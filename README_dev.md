# Development

Setup and running are in [README.md](README.md).

## Checking

Run `ruff check` or get the vscode ruff extension, the rules are defined in pyproject.toml.

## Type Checking

Run `ty check`

## Frontend

Pages are rendered server side with Jinja templates, only the scripts are TypeScript, bundled with bun.

```bash
bun install
bun run codegen  # Dump the app's OpenAPI schema and generate frontend/generated/openapi.d.ts from it
bun run check    # tsc --noEmit, bun build strips types without checking them
bun run build    # Bundle frontend/*.ts to src/my_cool_app/static/
bun run all      # All three, in order
```

Run `bun run all` after any api change, `frontend/generated/openapi.d.ts` is what makes a renamed endpoint or a
changed response model a compile error instead of an `undefined` at runtime.

Both generated files (`frontend/generated/openapi.d.ts` and the static bundle) are committed, since the package
ships `src/my_cool_app/static/` and prod installs won't have bun. CI regenerates them and fails on a
diff, so don't hand edit them.

## Testing

Run `pytest`, it will get its config from pyproject.toml

`scripts/run-ci-local.sh` runs the lot: ty, ruff, bun and pytest.

## Test Coverage

```bash
scripts/run-coverage.sh
python -m http.server -b 127.0.0.1 8000 -d htmlcov
```

## Workflows

The '.github' folder has Check, Type Check, Check Frontend and Test workflows.

Check Frontend pins a bun version, since bun's bundler output is only byte identical within a version
and an unpinned bun would fail the 'generated files are up to date' diff on every bun release.

To get the workflow passing badges on your repo, have a look at <https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge>
