__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod
from typing import List

from snakemake_interface_executor_plugins.jobs import ExecutorJobInterface
from snakemake_interface_executor_plugins.logging import LoggerExecutorInterface
from snakemake_interface_executor_plugins.utils import format_cli_arg
from snakemake_interface_executor_plugins.workflow import WorkflowExecutorInterface

class AbstractExecutor(ABC):
    def __init__(
        self,
        workflow: WorkflowExecutorInterface,
        logger: LoggerExecutorInterface,
    ):
        self.workflow = workflow
        self.dag = workflow.dag
        self.logger = logger

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
        jobs: List[ExecutorJobInterface],
        callback=None,
        submit_callback=None,
        error_callback=None,
    ):
        """Run a list of jobs that is ready at a given point in time.

        By default, this method just runs each job individually.
        This method can be overwritten to submit many jobs in a more efficient
        way than one-by-one. Note that in any case, for each job, the callback
        functions have to be called individually!
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
