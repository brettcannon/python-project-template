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
