# Development

Setup and running are in [README.md](README.md).

## Checking

Run `ruff check` or get the vscode ruff extension, the rules are defined in pyproject.toml.

Run `pnpm exec biome check --write` for everything else, biome formats and lints the TypeScript, JSON, markdown and
yaml. Config is in biome.json, gitignored files, the generated client, the static bundles and pnpm-lock.yaml are
skipped.

## Type Checking

Run `ty check`

## Frontend

Pages are rendered server side with Jinja templates, only the scripts are TypeScript, bundled with esbuild.

One entrypoint per template: `frontend/pages/home.ts` builds to `static/home.js`, which `home.html.j2` loads with
`<script type="module">`. Shared code goes in `frontend/` and is bundled into whichever pages import it, so a new
page never grows the bundles of the others.

```bash
pnpm install
pnpm run codegen # Dump the app's OpenAPI schema to frontend/openapi.json, generate frontend/generated/ from it
pnpm run check   # tsc --noEmit, esbuild strips types without checking them
pnpm run build   # Bundle each frontend/pages/*.ts to src/my_cool_app/static/, minified
pnpm run all     # All three, in order
```

Run `pnpm run all` after any api change, the typed client in `frontend/generated/` (@hey-api/openapi-ts, configured
in openapi-ts.config.ts) is what makes a renamed endpoint or a changed response model a compile error instead of an
`undefined` at runtime.

All generated files (`frontend/openapi.json`, `frontend/generated/` and the static bundles) are committed, since
the package ships `src/my_cool_app/static/` and prod installs won't have node. CI regenerates them and fails on a
diff, so don't hand edit them.

## Testing

Run `pytest`, it will get its config from pyproject.toml

`scripts/run-ci-local.sh` runs the lot: ty, ruff, pnpm and pytest.

## Test Coverage

```bash
scripts/run-coverage.sh
python -m http.server -b 127.0.0.1 8000 -d htmlcov
```

## Workflows

The '.github' folder has Check, Type Check, Check Frontend and Test workflows.

esbuild is pinned to an exact version in package.json, since its output is only byte identical within a version
and an unpinned esbuild would fail the 'generated files are up to date' diff on every esbuild release.

To get the workflow passing badges on your repo, have a look at <https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge>
