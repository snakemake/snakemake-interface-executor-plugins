__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import abstractmethod
import os
from snakemake_interface_executor_plugins.executors.base import AbstractExecutor
from snakemake_interface_executor_plugins.logging import LoggerExecutorInterface
from snakemake_interface_executor_plugins.settings import ExecMode
from snakemake_interface_executor_plugins.utils import (
    encode_target_jobs_cli_args,
    format_cli_arg,
    join_cli_args,
)
from snakemake_interface_executor_plugins.jobs import ExecutorJobInterface
from snakemake_interface_executor_plugins.workflow import WorkflowExecutorInterface


class RealExecutor(AbstractExecutor):
    def __init__(
        self,
        workflow: WorkflowExecutorInterface,
        logger: LoggerExecutorInterface,
        pass_default_remote_provider_args: bool = True,
        pass_default_resources_args: bool = True,
        pass_envvar_declarations_to_cmd: bool = True,
    ):
        super().__init__(
            workflow,
            logger,
        )
        self.executor_settings = self.workflow.executor_settings
        self.snakefile = workflow.main_snakefile
        self.pass_default_remote_provider_args = pass_default_remote_provider_args
        self.pass_default_resources_args = pass_default_resources_args
        self.pass_envvar_declarations_to_cmd = pass_envvar_declarations_to_cmd

    @property
    @abstractmethod
    def cores(self):
        # return "all" in case of remote executors,
        # otherwise self.workflow.resource_settings.cores
        ...

    def register_job(self, job: ExecutorJobInterface):
        job.register()

    def _run(self, job: ExecutorJobInterface, callback=None, error_callback=None):
        super()._run(job)

        try:
            self.register_job(job)
        except IOError as e:
            self.logger.info(
                "Failed to set marker file for job started ({}). "
                "Snakemake will work, but cannot ensure that output files "
                "are complete in case of a kill signal or power loss. "
                "Please ensure write permissions for the "
                "directory {}".format(e, self.workflow.persistence.path)
            )

    def handle_job_success(
        self,
        job: ExecutorJobInterface,
        upload_remote=True,
        handle_log=True,
        handle_touch=True,
        ignore_missing_output=False,
    ):
        job.postprocess(
            upload_remote=upload_remote,
            handle_log=handle_log,
            handle_touch=handle_touch,
            ignore_missing_output=ignore_missing_output,
        )

    def handle_job_error(self, job: ExecutorJobInterface, upload_remote=True):
        job.postprocess(
            error=True,
        )

    def additional_general_args(self):
        """Inherit this method to add stuff to the general args.

        A list must be returned.
        """
        return []

    def get_job_args(self, job: ExecutorJobInterface, **kwargs):
        return join_cli_args(
            [
                format_cli_arg(
                    "--target-jobs", encode_target_jobs_cli_args(job.get_target_spec())
                ),
                # Restrict considered rules for faster DAG computation.
                # This does not work for updated jobs because they need
                # to be updated in the spawned process as well.
                format_cli_arg(
                    "--allowed-rules",
                    job.rules,
                    quote=False,
                    skip=job.is_branched or job.is_updated,
                ),
                # Ensure that a group uses its proper local groupid.
                format_cli_arg("--local-groupid", job.jobid, skip=not job.is_group()),
                format_cli_arg("--cores", kwargs.get("cores", self.cores)),
                format_cli_arg("--attempt", job.attempt),
                format_cli_arg("--force-use-threads", not job.is_group()),
                self.get_resource_declarations(job),
            ]
        )

    @property
    def job_specific_local_groupid(self):
        return True

    def get_snakefile(self):
        return self.snakefile

    @abstractmethod
    def get_python_executable(self):
        ...

    @abstractmethod
    def get_exec_mode(self) -> ExecMode:
        ...

    def get_envvar_declarations(self):
        if self.pass_envvar_declarations_to_cmd:
            return " ".join(
                f"{var}={repr(os.environ[var])}"
                for var in self.workflow.remote_execution_settings.envvars
            )
        else:
            return ""

    def get_job_exec_prefix(self, job: ExecutorJobInterface):
        return ""

    def get_job_exec_suffix(self, job: ExecutorJobInterface):
        return ""

    def format_job_exec(self, job: ExecutorJobInterface):
        prefix = self.get_job_exec_prefix(job)
        if prefix:
            prefix += " &&"
        suffix = self.get_job_exec_suffix(job)
        if suffix:
            suffix = f"&& {suffix}"
        general_args = self.workflow.spawned_job_args_factory.general_args(
            pass_default_remote_provider_args=self.pass_default_remote_provider_args,
            pass_default_resources_args=self.pass_default_resources_args,
        )
        return join_cli_args(
            [
                prefix,
                self.get_envvar_declarations(),
                self.get_python_executable(),
                "-m snakemake",
                format_cli_arg("--snakefile", self.get_snakefile()),
                self.get_job_args(job),
                general_args,
                self.additional_general_args(),
                format_cli_arg("--mode", self.get_exec_mode().item_to_choice()),
                format_cli_arg(
                    "--local-groupid",
                    self.workflow.group_settings.local_groupid,
                    skip=self.job_specific_local_groupid,
                ),
                suffix,
            ]
        )
