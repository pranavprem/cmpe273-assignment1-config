# Agent guide

This repository stores configuration for a Spring 2017 class assignment. It is not an application. Read this file before editing.

## Architecture

[pranavprem/cmpe273-assignment1](https://github.com/pranavprem/cmpe273-assignment1) is the Flask app. This repo is the GitHub URL that app is given on startup. On `GET /v1/<config_file>` the app fetches `<config_file>` from the root of this repo through the GitHub Contents API.

- If the file exists, the response body is the raw file contents.
- If it does not, the app tries the other extension (`.json` ↔ `.yml`) and converts.

Config files therefore belong at the repository root, named `{environment}-config.json` or `{environment}-config.yml`. The app only swaps those two extensions. `.yaml` is invisible to it.

Required shape: a mapping with a non-empty string `welcome_message`. Extra keys are allowed. `dev-config.json` has `"something": "test"` from a March 17, 2017 experiment.

## Commands

Python 3.12 or newer (see `.python-version`).

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
ruff check tests
ruff format --check tests
python -m pytest
```

CI is `.github/workflows/validate-configs.yml`. It runs the same three commands. Dependencies are pinned in `requirements-dev.txt`.

## Conventions

- Leave the three config documents byte-for-byte alone unless the owner asks to change the data. The app serves existing files verbatim, so whitespace and key order are user-visible.
- Tests check shape, not the welcome text. A message edit should keep passing.
- New environments get a new root file that matches `{environment}-config.json` or `{environment}-config.yml`, with a string `welcome_message`.
- Ruff formats `tests/` only. Do not run a JSON or YAML rewriter over the config files.
- Default branch is `master`.
- Do not add a license file.
- Do not commit `.venv/`, caches, or secrets. There are no credentials in this repo.

## Gotchas

- `dev-config.yml` was deleted on purpose on March 17, 2017. Leave it deleted. Requests for that name are answered by converting `dev-config.json`. Restoring the YAML file would change the body the app returns.
- `test-config.json` and `test-config.yml` disagree on the welcome string. That split is from the live-update experiment. Keep both texts.
- The companion targets Python 2.7 (`basestring`, `str.decode("base64")` on the PyGithub payload). Updating the checkers here does not make that app run on Python 3.
- The companion constructs `Github()` with no token, so it shares the unauthenticated 60-request hourly limit. Rate-limit errors come from that client, not from these files.
- When the app synthesizes YAML from JSON it slices the dumped string (`response[1:-2]`). A generated `dev-config.yml` body is therefore mangled. That bug is in the other repository.
- The companion Dockerfile's default command URL is the application repo, not this one. Callers pass `https://github.com/pranavprem/cmpe273-assignment1-config` explicitly.

## Where to look

| Path | Role |
| --- | --- |
| `dev-config.json`, `test-config.json`, `test-config.yml` | The assignment data |
| `tests/test_configs.py` | Parse and shape checks |
| `requirements-dev.txt` | Pinned pytest, PyYAML, and Ruff |
| `pyproject.toml` | Ruff configuration |
| `README.md` | History and how to run the companion |
