__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod

from snakemake_interface_executor_plugins.dag import DAGExecutorInterface
from snakemake_interface_executor_plugins.jobs import ExecutorJobInterface
from snakemake_interface_executor_plugins.utils import format_cli_arg, join_cli_args
from snakemake_interface_executor_plugins.workflow import WorkflowExecutorInterface


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
        self.keepincomplete = workflow.keep_incomplete

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
