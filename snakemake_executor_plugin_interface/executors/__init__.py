__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod
import asyncio
import os
import sys
import contextlib
import time
import json
import stat
import shutil
import shlex
import threading
import concurrent.futures
import subprocess
import tempfile
from functools import partial
from collections import namedtuple
import base64
import uuid
import re
import math
from snakemake.interfaces import (
    DAGExecutorInterface,
    ExecutorJobInterface,
    GroupJobExecutorInterface,
    SingleJobExecutorInterface,
    WorkflowExecutorInterface,
)
from snakemake.target_jobs import encode_target_jobs_cli_args
from fractions import Fraction

from snakemake.shell import shell
from snakemake.logging import logger
from snakemake.stats import Stats
from snakemake.utils import makedirs
from snakemake.io import get_wildcard_names, Wildcards
from snakemake.exceptions import print_exception, get_exception_origin
from snakemake.exceptions import format_error, RuleException, log_verbose_traceback
from snakemake.exceptions import (
    WorkflowError,
    SpawnedJobError,
    CacheMissException,
)
from snakemake.common import (
    Mode,
    get_container_image,
    get_uuid,
    lazy_property,
    async_lock,
)
from snakemake.executors.common import format_cli_arg, join_cli_args


async def sleep():
    # do not sleep on CI. In that case we just want to quickly test everything.
    if os.environ.get("CI") != "true":
        await asyncio.sleep(10)
    else:
        await asyncio.sleep(1)


class AbstractExecutor(ABC):
    def __init__(
        self,
        workflow: WorkflowExecutorInterface,
        dag: DAGExecutorInterface,
        printreason=False,
        quiet=False,
        printshellcmds=False,
        printthreads=True,
        keepincomplete=False,
    ):
        self.workflow = workflow
        self.dag = dag
        self.quiet = quiet
        self.printreason = printreason
        self.printshellcmds = printshellcmds
        self.printthreads = printthreads
        self.latency_wait = workflow.latency_wait
        self.keepincomplete = keepincomplete

    def get_default_remote_provider_args(self):
        return join_cli_args(
            [
                self.workflow_property_to_arg("default_remote_prefix"),
                self.workflow_property_to_arg("default_remote_provider", attr="name"),
            ]
        )

    def get_set_resources_args(self):
        return format_cli_arg(
            "--set-resources",
            [
                f"{rule}:{name}={value}"
                for rule, res in self.workflow.overwrite_resources.items()
                for name, value in res.items()
            ],
            skip=not self.workflow.overwrite_resources,
        )

    def get_default_resources_args(self, default_resources=None):
        default_resources = default_resources or self.workflow.default_resources
        return format_cli_arg("--default-resources", default_resources.args)

    def get_resource_scopes_args(self):
        return format_cli_arg(
            "--set-resource-scopes", self.workflow.overwrite_resource_scopes
        )

    def get_resource_declarations_dict(self, job: ExecutorJobInterface):
        def isdigit(i):
            s = str(i)
            # Adapted from https://stackoverflow.com/a/1265696
            if s[0] in ("-", "+"):
                return s[1:].isdigit()
            return s.isdigit()

        excluded_resources = self.workflow.resource_scopes.excluded.union(
            {"_nodes", "_cores"}
        )
        return {
            resource: value
            for resource, value in job.resources.items()
            if isinstance(value, int)
            # need to check bool seperately because bool is a subclass of int
            and isdigit(value) and resource not in excluded_resources
        }

    def get_resource_declarations(self, job: ExecutorJobInterface):
        resources = [
            f"{resource}={value}"
            for resource, value in self.get_resource_declarations_dict(job).items()
        ]
        return format_cli_arg("--resources", resources)

    def run_jobs(
        self,
        jobs: list[ExecutorJobInterface],
        callback=None,
        submit_callback=None,
        error_callback=None,
    ):
        """Run a list of jobs that is ready at a given point in time.

        By default, this method just runs each job individually.
        This method can be overwritten to submit many jobs in a more efficient way than one-by-one.
        Note that in any case, for each job, the callback functions have to be called individually!
        """
        for job in jobs:
            self.run(
                job,
                callback=callback,
                submit_callback=submit_callback,
                error_callback=error_callback,
            )

    def run(
        self,
        job: ExecutorJobInterface,
        callback=None,
        submit_callback=None,
        error_callback=None,
    ):
        """Run a specific job or group job."""
        self._run(job)
        callback(job)

    @abstractmethod
    def shutdown(self):
        ...

    @abstractmethod
    def cancel(self):
        ...

    def _run(self, job: ExecutorJobInterface):
        job.check_protected_output()
        self.printjob(job)

    def rule_prefix(self, job: ExecutorJobInterface):
        return "local " if job.is_local else ""

    def printjob(self, job: ExecutorJobInterface):
        job.log_info(skip_dynamic=True)

    def print_job_error(self, job: ExecutorJobInterface, msg=None, **kwargs):
        job.log_error(msg, **kwargs)

    @abstractmethod
    def handle_job_success(self, job: ExecutorJobInterface):
        ...

    @abstractmethod
    def handle_job_error(self, job: ExecutorJobInterface):
        ...