import json
import re

import nox


PACKAGE_NAME = "pkg"  # XXX


@nox.session(python=["3.8"])
def test(session):
    session.install("pytest", "coverage[toml]", "pytest-cov")
    session.run("python", "-m", "pytest", f"--cov={PACKAGE_NAME}", "tests")


@nox.session
def lint(session):
    session.install("pre-commit", "poetry")
    session.run("pre-commit", "run", "--all-files")
    session.run("poetry", "build")


@nox.session
def docs(session):
    pass


def bump_version(session, event):
    labels = {label["name"] for label in event["pull_request"]["labels"]}

    #session.install("tomlkit")
    import tomlkit

    with open("pyproject.toml", encoding="utf-8") as file:
        toml_data = tomlkit.loads(file.read())

    #session.install("packaging")
    import packaging.version

    version = packaging.version.Version(toml_data["tool"]["poetry"]["version"])
    major, minor, micro, post = (
        version.major,
        version.minor,
        version.micro,
        version.post,
    )
    if "impact:breaking" in labels:
        new_version = f"{major + 1}.0.0"
    elif "impact:feature" in labels:
        new_version = f"{major}.{minor + 1}.0"
    elif "impact:bugfix" in labels:
        new_version = f"{major}.{minor}.{micro + 1}"
    elif "impact:post-release" in labels:
        post = (post or 0) + 1
        new_version = f"{major}.{minor}.{micro}.post{post}"
    else:
        return None

    toml_data["tool"]["poetry"]["version"] = new_version
    with open("pyproject.toml", "w", encoding="utf-8") as file:
        file.write(tomlkit.dumps(toml_data))

    return new_version


CHANGLELOG_TEMPLATE = """# {version}
{message} ([#{pr_number}]({pr_url}); thanks [{author_name}]({author_url}))

"""


def update_changelog(session, event, new_version):
    #session.install("httpx")
    import httpx

    message = event["pull_request"]["title"]
    pr_number = event["number"]
    pr_url = event["pull_request"]["html_url"]
    author_data = httpx.get(event["pull_request"]["user"]["url"]).json()
    author_name = author_data["name"]
    author_url = author_data["html_url"]
    entry = CHANGLELOG_TEMPLATE.format(
        version=new_version,
        message=message,
        pr_number=pr_number,
        pr_url=pr_url,
        author_name=author_name,
        author_url=author_url,
    )
    with open("CHANGELOG.md", encoding="utf-8") as file:
        original_changelog = file.read()
    with open("CHANGELOG.md", "w", encoding="utf-8") as file:
        file.write(entry)
        file.write(original_changelog)
    return entry


@nox.session
def release(session):
    with open(session.env["GITHUB_EVENT_PATH"], encoding="utf-8") as file:
        event = json.loads(file.read())
    assert event["pull_request"]["merged"]
    if not (new_version := bump_version(session, event)):
        return  # Nothing to do.
    entry = update_changelog(session, event, new_version)
    session.run("git", "commit", "-a", "-m", f"Updates for v{new_version}")
    session.run("git", "push")
    session.run("git", "tag", "-a", f"v{new_version}", "-m", entry)
    session.run("git", "push", "--tags")
