# KiSM's FastAPI Boilerplate

[![Check](https://github.com/kism/fastapi-boilerplate/actions/workflows/check.yml/badge.svg)](https://github.com/kism/fastapi-boilerplate/actions/workflows/check.yml)
[![CheckType](https://github.com/kism/fastapi-boilerplate/actions/workflows/check_types.yml/badge.svg)](https://github.com/kism/fastapi-boilerplate/actions/workflows/check_types.yml)
[![Test](https://github.com/kism/fastapi-boilerplate/actions/workflows/test.yml/badge.svg)](https://github.com/kism/fastapi-boilerplate/actions/workflows/test.yml)

See [README_dev.md](README_dev.md) for checking, testing and CI.

## Using this template

Rename the app and repo references (replace `your_app` and `youruser/your-repo`):

```bash
NEW_MODULE=your_app                 # python module name, snake_case
NEW_DIST=your-app                   # package/dist name, kebab-case
NEW_REPO=youruser/your-repo         # github <user>/<repo>

git grep -lz -e my_cool_app -e my-cool-app -e kism/fastapi-boilerplate | \
  xargs -0 sed -i "s|my_cool_app|$NEW_MODULE|g; s|my-cool-app|$NEW_DIST|g; s|kism/fastapi-boilerplate|$NEW_REPO|g"
git mv src/my_cool_app "src/$NEW_MODULE"
git mv "src/$NEW_MODULE/static/my_cool_app.js" "src/$NEW_MODULE/static/$NEW_MODULE.js"
rm -rf .venv *.egg-info && uv sync --all-extras
```

Then delete this section.

## This Boilerplate

I have made a few simple web apps, this is what I use as a starting point for my future projects.

Features:

- Config loads from a JSON file in the instance directory, defined and validated with pydantic
- Logging setup with a TRACE level, optionally to a file
- Example api endpoint, with frontend javascript on the homepage that uses it
- Tests with PyTest
- No database

Project features:

- Four PyPi packages (and their dependencies) for prod
- All project/tool configs in pyproject.toml
- Virtual environment, dependencies and packaging managed by uv
- Checked with ruff, type checked with ty

Comments marked with KISM-BOILERPLATE are placeholder code that you will remove/replace.

This goes with a simple CSS I made which is close to classless: <https://github.com/kism/zy.css>
Have a look at <https://github.com/dbohdan/classless-css> too if you want a different css.

## Prerequisites

Install uv and uvx with the installer script <https://docs.astral.sh/uv/getting-started/installation/>

## Run

### Setup

```bash
uv venv
source .venv/bin/activate
uv sync --all-extras # Omit --all-extras for prod
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
uv sync --no-dev
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
