import sys


def test_imports_from_py37():
    assert sys.version_info >= (3, 7) and sys.version_info < (3, 8)
    from snakemake_interface_executor_plugins import (  # noqa: F401
        settings,
        jobs,
        logging,
        persistence,
        resources,
        scheduler,
        utils,
        workflow,
        dag,
        exceptions,
    )
