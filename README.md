# cmpe273-assignment1-config

Configuration repository for Part II of Assignment 1 in **CMPE 273, Enterprise Distributed Systems** (Spring 2017, San José State University, Prof. Sithu Aung).

The assignment used two GitHub repositories. [pranavprem/cmpe273-assignment1](https://github.com/pranavprem/cmpe273-assignment1) is the Dockerized Flask application. This repository is the configuration that application reads from GitHub on each request. Pranav Prem created it on March 12, 2017 and last edited it on March 17, 2017.

[![Validate configs](https://github.com/pranavprem/cmpe273-assignment1-config/actions/workflows/validate-configs.yml/badge.svg)](https://github.com/pranavprem/cmpe273-assignment1-config/actions/workflows/validate-configs.yml)

## Original context

Part I of the assignment was a Flask process that returned a fixed hello string from a `python:2.7.13` image. Part II required that process to load configuration from a second GitHub repository, so a commit in this repo would show up on the next HTTP response without rebuilding the image.

The write-up lives in the course repo under [assignment1](https://github.com/sithu/cmpe273-spring17/tree/master/assignment1). The professor's sample config repo, [sithu/assignment1-config-example](https://github.com/sithu/assignment1-config-example), uses files named `{environment}-config.yml`. This repo follows that layout and also stores JSON copies, which the companion app learned to serve.

The files were edited during the assignment to prove the app noticed new commits:

| File | History |
| --- | --- |
| `dev-config.yml` | Added March 12, message edited to confirm a live update, then deleted March 17. |
| `dev-config.json` | Added March 17. Later that evening an extra `"something": "test"` key was committed. |
| `test-config.yml` | Added March 12 and left in place. |
| `test-config.json` | Added March 17. The welcome string was then changed to end with `testing changes`. |

Those strings are the assignment data. This refresh leaves them as they were committed.

## How it works

The companion app takes this repository's URL as its command-line argument, opens it with [PyGithub](https://github.com/PyGithub/PyGithub), and exposes one route:

```text
GET /v1/<config_file>
```

`<config_file>` is a file name at the root of this repo, for example `dev-config.json` or `test-config.yml`. When that file exists, the response body is the file as stored in Git. When the requested extension is absent, the app reads the sibling extension (`.json` or `.yml`) and converts it.

Deleting `dev-config.yml` still leaves a YAML answer for dev: a request for `dev-config.yml` is filled by converting `dev-config.json`. A request for `test-config.yml` returns the YAML file itself, because that file is still here.

| File | `welcome_message` | Other keys |
| --- | --- | --- |
| `dev-config.json` | `Hello from Dockerized Flask App` | `something`: `test` |
| `test-config.json` | `Hello from Dockerized Flask App Test testing changes` | none |
| `test-config.yml` | `Hello from Dockerized Flask App Test` | none |

## Interface

The assignment's visible output is the HTTP body from the companion Flask app. This repository only stores the documents that body is built from, so there is no page or screen recording to add here.

## How to run it today

This repository is the configuration the companion reads. Run the checks below, or point the companion app at it.

**Read a file directly**

```sh
curl -fsSL https://raw.githubusercontent.com/pranavprem/cmpe273-assignment1-config/master/dev-config.json
curl -fsSL https://raw.githubusercontent.com/pranavprem/cmpe273-assignment1-config/master/test-config.yml
```

**Serve it the way the assignment did**

Clone the companion app and pass this repo's URL. The image's default command points at the application repository, so pass the config URL yourself:

```sh
git clone https://github.com/pranavprem/cmpe273-assignment1
cd cmpe273-assignment1
python app.py https://github.com/pranavprem/cmpe273-assignment1-config
```

```sh
curl http://127.0.0.1:5000/v1/dev-config.json
curl http://127.0.0.1:5000/v1/test-config.yml
```

With Docker, from that other repository:

```sh
docker build -t assignment1-flask-app:latest .
docker run --rm -p 5000:5000 assignment1-flask-app \
  https://github.com/pranavprem/cmpe273-assignment1-config
```

The companion is the Spring 2017 code: Python 2.7, unpinned `flask`, `pygithub`, and `pyyaml`, and an unauthenticated GitHub client limited to 60 requests per hour. It is a separate repository and was left as it was. Plan on Python 2 and old-dependency work before that process stays up on a current machine.

**Check these files locally**

The checks here use Python 3.12 or newer. They confirm each config parses and contains a non-empty `welcome_message` string. Editing the message text, which is what the assignment was demonstrating, still passes.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
ruff check tests
ruff format --check tests
python -m pytest
```

GitHub Actions runs those commands on pushes to `master` and on pull requests (`.github/workflows/validate-configs.yml`).

## Tech stack

| Piece | Choice |
| --- | --- |
| Config documents | JSON, and YAML 1.1 as read by PyYAML `safe_load` |
| Filenames | `{environment}-config.json` and `{environment}-config.yml` at the repository root |
| Companion app (other repo) | Python 2.7.13, Flask, PyGithub, PyYAML, Docker |
| Checks in this repo | Python 3.12, pytest 9.1.1, PyYAML 6.0.3, Ruff 0.17.0 |

## Project structure

```text
.
├── dev-config.json                         # dev environment, JSON
├── test-config.json                        # test environment, JSON
├── test-config.yml                         # test environment, YAML
├── tests/test_configs.py                   # shape checks for the files above
├── requirements-dev.txt                    # pinned checker dependencies
├── pyproject.toml                          # Ruff settings
├── .github/workflows/validate-configs.yml  # CI
├── AGENTS.md                               # guide for coding agents
└── CLAUDE.md                               # pointer to AGENTS.md
```

## Maintainer notes

Whitespace, key order, and the extra `something` field are part of the HTTP body whenever the companion returns a file that exists. Keep formatters off the three config files.

Adding a license is the owner's decision; this refresh does not add one.
