__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

import asyncio
import base64
from collections import UserDict
from pathlib import Path
import re
import shlex
import threading
from typing import Any, List
from urllib.parse import urlparse
from collections import namedtuple
import concurrent.futures
import contextlib

from snakemake_interface_common.settings import SettingsEnumBase
from snakemake_interface_common.utils import not_iterable


TargetSpec = namedtuple("TargetSpec", ["rulename", "wildcards_dict"])


def format_cli_arg(flag, value, quote=True, skip=False, base64_encode: bool = False):
    if not skip and value:
        if isinstance(value, bool):
            value = ""
        else:
            value = format_cli_pos_arg(value, quote=quote, base64_encode=base64_encode)
        return f"{flag} {value}"
    return ""


def format_cli_pos_arg(value, quote=True, base64_encode: bool = False):
    if isinstance(value, (dict, UserDict)):

        def fmt_item(key, value):
            expr = f"{key}={format_cli_value(value)}"
            return encode_as_base64(expr) if base64_encode else repr(expr)

        return join_cli_args(fmt_item(key, val) for key, val in value.items())
    elif not_iterable(value):
        return format_cli_value(value, base64_encode=base64_encode)
    else:
        return join_cli_args(
            format_cli_value(v, quote=True, base64_encode=base64_encode) for v in value
        )


def format_cli_value(
    value: Any, quote: bool = False, base64_encode: bool = False
) -> str:
    """Format a given value for passing it to CLI.

    If base64_encode is True, str values are encoded and flagged as being base64 encoded.
    """

    def maybe_encode(value):
        return encode_as_base64(value) if base64_encode else value

    if isinstance(value, SettingsEnumBase):
        return value.item_to_choice()
    elif isinstance(value, Path):
        return shlex.quote(str(value))
    elif isinstance(value, str):
        if is_quoted(value) and not base64_encode:
            # the value is already quoted, do not quote again
            return maybe_encode(value)
        elif quote and not base64_encode:
            return maybe_encode(repr(value))
        else:
            return maybe_encode(value)
    else:
        return repr(value)


def join_cli_args(args):
    try:
        return " ".join(arg for arg in args if arg)
    except TypeError as e:
        raise TypeError(
            f"bug: join_cli_args expects iterable of strings. Given: {args}"
        ) from e


def url_can_parse(url: str) -> bool:
    """
    returns true if urllib.parse.urlparse can parse
    scheme and netloc
    """
    return all(list(urlparse(url))[:2])


def encode_target_jobs_cli_args(
    target_jobs: List[TargetSpec],
) -> List[str]:
    items = []

    def add_quotes_if_contains_comma(s):
        if isinstance(s, str):
            if "," in s:
                return f'"{s}"'
        return s

    for spec in target_jobs:
        wildcards = ",".join(
            f"{key}={add_quotes_if_contains_comma(value)}"
            for key, value in spec.wildcards_dict.items()
        )
        items.append(f"{spec.rulename}:{wildcards}")
    return items


_pool = concurrent.futures.ThreadPoolExecutor()


@contextlib.asynccontextmanager
async def async_lock(_lock: threading.Lock):
    """Use a threaded lock form threading.Lock in an async context

    Necessary because asycio.Lock is not threadsafe, so only one thread can safely use
    it at a time.
    Source: https://stackoverflow.com/a/63425191
    """
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(_pool, _lock.acquire)
    try:
        yield  # the lock is held
    finally:
        _lock.release()


_is_quoted_re = re.compile(r"^['\"].+['\"]")


def is_quoted(value: str) -> bool:
    return _is_quoted_re.match(value) is not None


base64_prefix = "base64//"


def maybe_base64(parser_func):
    """Parse optionally base64 encoded CLI args, applying parser_func if not None."""

    def inner(args):
        def is_base64(arg):
            return arg.startswith(base64_prefix)

        def decode(arg):
            if is_base64(arg):
                return base64.b64decode(arg[len(base64_prefix) :]).decode()
            else:
                return arg

        def apply_parser(args):
            if parser_func is not None:
                return parser_func(args)
            else:
                return args

        if isinstance(args, str):
            return apply_parser(decode(args))
        elif isinstance(args, list):
            decoded = [decode(arg) for arg in args]
            return apply_parser(decoded)
        else:
            raise NotImplementedError()

    return inner


def encode_as_base64(arg: str):
    return f"{base64_prefix}{base64.b64encode(arg.encode()).decode()}"
