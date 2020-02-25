This repository contains an example Python project for use on GitHub.

# Local Usage
[Nox](https://nox.thea.codes/) is used to run checks against the code. The
following sessions are supported:
- `test` (using [pytest](https://docs.pytest.org/) and
          [coverage.py](https://coverage.readthedocs.io/))
- `lint` (using [pre-commit](https://pre-commit.com/) for
          [Black](https://black.readthedocs.io/), [mypy](http://mypy-lang.org/),
          and various file format checks; [Poetry](https://python-poetry.org)
          for package readiness)

# On GitHub
CI is set up on `push` and `pull_request` to run the specified nox sessions.

# XXX TODO
- Bump version number based on PR label
- Update changelog based on commit message of PR
- Push to PyPI
- Create release
- Require a version bump label
- Automatically add appropriate "thanks" to changelog entry
- Attach artifacts to GH release
