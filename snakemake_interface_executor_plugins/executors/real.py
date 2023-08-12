__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import abstractmethod
import os
import sys
from typing import Optional
from snakemake_interface_executor_plugins import ExecutorSettingsBase
from snakemake_interface_executor_plugins.dag import DAGExecutorInterface
from snakemake_interface_executor_plugins.executors.base import AbstractExecutor
from snakemake_interface_executor_plugins.logging import LoggerExecutorInterface
from snakemake_interface_executor_plugins.persistence import StatsExecutorInterface
from snakemake_interface_executor_plugins.utils import (
    encode_target_jobs_cli_args,
    format_cli_arg,
    join_cli_args,
    lazy_property,
)
from snakemake_interface_executor_plugins.jobs import ExecutorJobInterface
from snakemake_interface_executor_plugins.workflow import WorkflowExecutorInterface


class RealExecutor(AbstractExecutor):
    def __init__(
        self,
        workflow: WorkflowExecutorInterface,
        dag: DAGExecutorInterface,
        stats: StatsExecutorInterface,
        logger: LoggerExecutorInterface,
        executor_settings: Optional[ExecutorSettingsBase],
        job_core_limit: Optional[int] = None,
    ):
        super().__init__(
            workflow,
            dag,
        )
        self.cores = job_core_limit if job_core_limit else "all"
        self.executor_settings = executor_settings
        self.stats = stats
        self.logger = logger
        self.snakefile = workflow.main_snakefile

    def register_job(self, job: ExecutorJobInterface):
        job.register()

    def _run(self, job: ExecutorJobInterface, callback=None, error_callback=None):
        super()._run(job)
        self.stats.report_job_start(job)

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
        self.stats.report_job_end(job)

    def handle_job_error(self, job: ExecutorJobInterface, upload_remote=True):
        job.postprocess(
            error=True,
        )

    def additional_general_args(self):
        """Inherit this method to add stuff to the general args.

        A list must be returned.
        """
        return []

    def get_workdir_arg(self):
        return self.workflow_property_to_arg("overwrite_workdir", flag="--directory")

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
    def get_exec_mode(self):
        ...

    def get_envvar_declarations(self):
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
        return join_cli_args(
            [
                prefix,
                self.get_envvar_declarations(),
                self.get_python_executable(),
                "-m snakemake",
                format_cli_arg("--snakefile", self.get_snakefile()),
                self.get_job_args(job),
                self.get_default_remote_provider_args(),
                self.get_default_resources_args(),
                self.get_workdir_arg(),
                self.general_args,
                self.additional_general_args(),
                format_cli_arg("--mode", self.get_exec_mode()),
                format_cli_arg("--local-groupid", self.workflow.group_settings.local_groupid, skip=self.job_specific_local_groupid),
                suffix,
            ]
        )
