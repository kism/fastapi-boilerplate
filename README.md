# KiSM's Flask Boilerplate

![Lint](https://github.com/kism/flask-boilerplate/actions/workflows/lint.yml/badge.svg)
![Test](https://github.com/kism/flask-boilerplate/actions/workflows/check_types.yml/badge.svg)
![Test](https://github.com/kism/flask-boilerplate/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/github/kism/flask-boilerplate/graph/badge.svg?token=NARIB5JF9M)](https://codecov.io/github/kism/flask-boilerplate)

## Why this boilerplate?

I have made a few simple web apps, this is what I use as a starting point for my future projects.

App features:

- App config loads from a TOML file
  - I don't like using app.config, config.py makes configuration much more flexible.
- Logging configuration, including logging to file
- Example api call
  - Frontend javascript on the homepage that utilises it
- 100% test coverage with PyTest
- No database
  - Maybe i'll make it optional in the future

Project features:

- Only Four PyPi packages (and their dependencies) for prod
- Close to all project/tool configs in pyproject.toml
- Virtual environment and dependencies managed by uv
- Configuration object using pydantic-settings

Boilerplate features:

- Template the repo with cookiecutter
- Comments marked with KISM-BOILERPLATE where there is placeholder code that you will remove/replace.
- New repo has a README.md file with instructions for running the web app
- This repo has a test workflow to ensure that it works and tests pass after generating.

This goes with a simple CSS I made which is close to classless: <https://github.com/kism/zy.css> Cookie cutter grabs this and puts it in the right place. Have a look at <https://github.com/dbohdan/classless-css> too if you want a different css.

## Get started

```bash
pipx run cookiecutter gh:kism/flask-boilerplate
```

After some prompts, this will create the new project directory in the current directory, with the name you specified.

## Development

Wahoo

`cd ~/src && cookiecutter --overwrite-if-exists --default-config flask-boilerplate && cd ~/src/my-cool-app && uv venv && source .venv/bin/activate && uv sync`
