from invoke import task

from .util import PROJECT_DIR, print_and_run


@task(aliases=["mypy"])
def typecheck(ctx):
    """Run mypy typechecking."""
    print_and_run(
        ("mypy"),
        pty=True,
    )

    print("🎉🦆 Type checking passed.")


@task()
def unit(ctx):
    """Run unit tests."""
    print_and_run(
        f"pytest --cov=pm_tb_data --cov-fail-under 20 -s {PROJECT_DIR}/tests/unit",
        pty=True,
    )


@task(
    pre=[
        typecheck,
        unit,
    ],
)
def ci(ctx):
    """Run tests not requiring access to external data.

    Excludes e.g., regression tests that require access to data on
    NSIDC-specific infrastructure.
    """
    ...


@task()
def pytest(ctx):
    """Run all tests with pytest.

    Includes a code-coverage check.
    """
    print_and_run(
        "pytest --cov=pm_tb_data --cov-fail-under 20 -s",
        pty=True,
    )


@task(
    pre=[
        typecheck,
        pytest,
    ],
    default=True,
)
def all(ctx):  # noqa
    """Run all of the tests."""
    ...
