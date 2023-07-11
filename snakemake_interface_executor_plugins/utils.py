__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

import asyncio
import os
from collections import UserDict
import typing
from urllib.parse import urlparse
import collections
from collections import namedtuple


class ExecMode:
    """
    Enum for execution mode of Snakemake.
    This handles the behavior of e.g. the logger.
    """

    default = 0
    subprocess = 1
    remote = 2


def not_iterable(value):
    return (
        isinstance(value, str)
        or isinstance(value, dict)
        or not isinstance(value, collections.abc.Iterable)
    )


TargetSpec = namedtuple("TargetSpec", ["rulename", "wildcards_dict"])


async def sleep():
    # do not sleep on CI. In that case we just want to quickly test everything.
    if os.environ.get("CI") != "true":
        await asyncio.sleep(10)
    else:
        await asyncio.sleep(1)


def format_cli_arg(flag, value, quote=True, skip=False):
    if not skip and value:
        if isinstance(value, bool):
            value = ""
        else:
            value = format_cli_pos_arg(value, quote=quote)
        return f"{flag} {value}"
    return ""


def format_cli_pos_arg(value, quote=True):
    if isinstance(value, (dict, UserDict)):
        return join_cli_args(repr(f"{key}={val}") for key, val in value.items())
    elif not_iterable(value):
        return repr(value)
    else:
        return join_cli_args(repr(v) for v in value)


def join_cli_args(args):
    return " ".join(arg for arg in args if arg)


def url_can_parse(url: str) -> bool:
    """
    returns true if urllib.parse.urlparse can parse
    scheme and netloc
    """
    return all(list(urlparse(url))[:2])


def encode_target_jobs_cli_args(
    target_jobs: typing.List[TargetSpec],
) -> typing.List[str]:
    items = []
    for spec in target_jobs:
        wildcards = ",".join(
            f"{key}={value}" for key, value in spec.wildcards_dict.items()
        )
        items.append(f"{spec.rulename}:{wildcards}")
    return items


class lazy_property(property):
    __slots__ = ["method", "cached", "__doc__"]

    @staticmethod
    def clean(instance, method):
        delattr(instance, method)

    def __init__(self, method):
        self.method = method
        self.cached = f"_{method.__name__}"
        super().__init__(method, doc=method.__doc__)

    def __get__(self, instance, owner):
        cached = (
            getattr(instance, self.cached) if hasattr(instance, self.cached) else None
        )
        if cached is not None:
            return cached
        value = self.method(instance)
        setattr(instance, self.cached, value)
        return value
