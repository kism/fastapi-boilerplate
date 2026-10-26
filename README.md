# my_cool_app

## Using this template

Run the rename script and answer the prompts (module name, dist name, repo):

```bash
./AAA_RENAME_TEMPLATE.sh
```

It rewrites every `my_cool_app` / `my-cool-app` / `kism/fastapi-boilerplate` reference,
renames `src/my_cool_app`, drops template-only files, resyncs the venv, rebuilds the frontend,
re-inits git with a fresh initial commit, and deletes itself (and this section) when done.

Then delete this section.

[![Check](https://github.com/kism/fastapi-boilerplate/actions/workflows/check.yml/badge.svg)](https://github.com/kism/fastapi-boilerplate/actions/workflows/check.yml)
[![CheckType](https://github.com/kism/fastapi-boilerplate/actions/workflows/check_types.yml/badge.svg)](https://github.com/kism/fastapi-boilerplate/actions/workflows/check_types.yml)
[![CheckFrontend](https://github.com/kism/fastapi-boilerplate/actions/workflows/check_frontend.yml/badge.svg)](https://github.com/kism/fastapi-boilerplate/actions/workflows/check_frontend.yml)
[![Test](https://github.com/kism/fastapi-boilerplate/actions/workflows/test.yml/badge.svg)](https://github.com/kism/fastapi-boilerplate/actions/workflows/test.yml)

See [README_dev.md](README_dev.md) for checking, testing and CI.

## This Boilerplate

I have made a few simple web apps, this is what I use as a starting point for my future projects.

Features:

- Config loads from a JSON file in the instance directory, defined and validated with pydantic
- Logging setup with a TRACE level, optionally to a file
- Example api endpoint, with frontend TypeScript on the homepage that uses it
- Pages rendered server side with Jinja templates, no SPA framework
- TypeScript client typed from the app's own OpenAPI schema, so api changes break the build not prod
- Tests with PyTest
- No database

Project features:

- Four PyPi packages (and their dependencies) for prod
- All project/tool configs in pyproject.toml
- Virtual environment, dependencies and packaging managed by uv
- Frontend bundled with esbuild via pnpm, no vite/webpack
- Checked with ruff, type checked with ty and tsc

Comments marked with KISM-BOILERPLATE are placeholder code that you will remove/replace.

This goes with a simple CSS I made which is close to classless: <https://github.com/kism/zy.css>
Have a look at <https://github.com/dbohdan/classless-css> too if you want a different css.

## Prerequisites

Install uv and uvx with the installer script <https://docs.astral.sh/uv/getting-started/installation/>

Install node and pnpm <https://pnpm.io/installation>, it's only needed to change
the frontend, the built javascript is committed.

## Run

### Setup

```bash
uv venv
source .venv/bin/activate
uv sync --all-groups # Omit --all-groups for prod
```

### Run Dev

```bash
python -m my_cool_app
```

Or with reload, note that this bypasses the argparse entrypoint:

```bash
uvicorn --factory my_cool_app:create_app --reload --port 5000
```

### Run Prod

```bash
uv sync
.venv/bin/my-cool-app --host 127.0.0.1 --port 5000
```

Put it behind nginx/caddy for TLS and to serve as a reverse proxy.

## Config

`config.json` lives in the instance directory ('./instance' by default, override with `--instance-path`).
It is created with defaults on first run, and rewritten on every load with any missing fields filled in.
Defaults, definitions and validation are all in `src/my_cool_app/config.py`.

```json
{
  "app": {
    "my_message": "Hello, World!"
  },
  "logging": {
    "level": "INFO",
    "path": null
  }
}
```
