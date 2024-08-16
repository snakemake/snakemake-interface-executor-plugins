__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import abstractmethod
from typing import Dict
from snakemake_interface_executor_plugins.executors.base import (
    AbstractExecutor,
    SubmittedJobInfo,
)
from snakemake_interface_executor_plugins.logging import LoggerExecutorInterface
from snakemake_interface_executor_plugins.settings import ExecMode
from snakemake_interface_executor_plugins.utils import (
    encode_target_jobs_cli_args,
    format_cli_arg,
    join_cli_args,
)
from snakemake_interface_executor_plugins.jobs import JobExecutorInterface
from snakemake_interface_executor_plugins.workflow import WorkflowExecutorInterface


class RealExecutor(AbstractExecutor):
    def __init__(
        self,
        workflow: WorkflowExecutorInterface,
        logger: LoggerExecutorInterface,
        post_init: bool = True,
    ):
        super().__init__(
            workflow,
            logger,
        )
        self.executor_settings = self.workflow.executor_settings
        self.snakefile = workflow.main_snakefile
        if post_init:
            self.__post_init__()

    def __post_init__(self):
        """This method is called after the constructor. By default, it does nothing."""
        pass

    @property
    @abstractmethod
    def cores(self):
        # return "all" in case of remote executors,
        # otherwise self.workflow.resource_settings.cores
        ...

    def report_job_submission(
        self, job_info: SubmittedJobInfo, register_job: bool = True
    ):
        super().report_job_submission(job_info)

        if register_job:
            try:
                job_info.job.register(external_jobid=job_info.external_jobid)
            except IOError as e:
                self.logger.info(
                    f"Failed to set marker file for job started ({e}). "
                    "Snakemake will work, but cannot ensure that output files "
                    "are complete in case of a kill signal or power loss. "
                    "Please ensure write permissions for the "
                    "directory {self.workflow.persistence.path}."
                )

    def handle_job_success(self, job: JobExecutorInterface):
        pass

    def handle_job_error(self, job: JobExecutorInterface):
        pass

    def additional_general_args(self):
        """Inherit this method to add stuff to the general args.

        A list must be returned.
        """
        return []

    def get_job_args(self, job: JobExecutorInterface, **kwargs):
        unneeded_temp_files = list(self.workflow.dag.get_unneeded_temp_files(job))
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
                    skip=job.is_updated,
                ),
                # Ensure that a group uses its proper local groupid.
                format_cli_arg("--local-groupid", job.jobid, skip=not job.is_group()),
                format_cli_arg("--cores", kwargs.get("cores", self.cores)),
                format_cli_arg("--attempt", job.attempt),
                format_cli_arg("--force-use-threads", not job.is_group()),
                format_cli_arg(
                    "--unneeded-temp-files",
                    unneeded_temp_files,
                    skip=not unneeded_temp_files,
                ),
                self.get_resource_declarations(job),
            ]
        )

    @property
    def job_specific_local_groupid(self):
        return True

    def get_snakefile(self):
        return self.snakefile

    @abstractmethod
    def get_python_executable(self): ...

    @abstractmethod
    def get_exec_mode(self) -> ExecMode: ...

    @property
    def common_settings(self):
        return self.workflow.executor_plugin.common_settings

    def get_envvar_declarations(self):
        declaration = ""
        envars = self.envvars()
        if self.common_settings.pass_envvar_declarations_to_cmd and envars:
            defs = " ".join(f"{var}={value!r}" for var, value in envars)
            declaration = f"export {defs} &&"
        return declaration

    def get_job_exec_prefix(self, job: JobExecutorInterface):
        return ""

    def get_job_exec_suffix(self, job: JobExecutorInterface):
        return ""

    def format_job_exec(self, job: JobExecutorInterface) -> str:
        prefix = self.get_job_exec_prefix(job)
        if prefix:
            prefix += " &&"
        suffix = self.get_job_exec_suffix(job)
        if suffix:
            suffix = f"&& {suffix}"
        general_args = self.workflow.spawned_job_args_factory.general_args(
            executor_common_settings=self.common_settings
        )
        precommand = self.workflow.spawned_job_args_factory.precommand(
            executor_common_settings=self.common_settings
        )
        if precommand:
            precommand += " &&"

        args = join_cli_args(
            [
                prefix,
                self.get_envvar_declarations(),
                precommand,
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
        return args

    def envvars(self) -> Dict[str, str]:
        return self.workflow.spawned_job_args_factory.envvars()
