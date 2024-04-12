__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod
import asyncio
from fractions import Fraction
import os
import shutil
import stat
import sys
import tempfile
import threading
from typing import Generator, List
from snakemake_interface_common.exceptions import WorkflowError
from snakemake_interface_executor_plugins.executors.base import SubmittedJobInfo
from snakemake_interface_executor_plugins.executors.real import RealExecutor
from snakemake_interface_executor_plugins.jobs import JobExecutorInterface
from snakemake_interface_executor_plugins.logging import LoggerExecutorInterface
from snakemake_interface_executor_plugins.settings import ExecMode, SharedFSUsage
from snakemake_interface_executor_plugins.utils import async_lock, format_cli_arg
from snakemake_interface_executor_plugins.workflow import WorkflowExecutorInterface

from throttler import Throttler


class RemoteExecutor(RealExecutor, ABC):
    """Backend for distributed execution.

    The key idea is that a job is converted into a script that invokes
    Snakemake again, in whatever environment is targeted. The script
    is submitted to some job management platform (e.g. a cluster scheduler
    like slurm).
    This class can be specialized to generate more specific backends,
    also for the cloud.
    """

    default_jobscript = "jobscript.sh"

    def __init__(
        self,
        workflow: WorkflowExecutorInterface,
        logger: LoggerExecutorInterface,
    ):
        super().__init__(
            workflow,
            logger,
            post_init=False,  # we call __post_init__ ourselves
        )
        self._next_seconds_between_status_checks = None
        self.max_status_checks_per_second = (
            self.workflow.remote_execution_settings.max_status_checks_per_second
        )
        self.jobname = self.workflow.remote_execution_settings.jobname

        if SharedFSUsage.SOURCES not in self.workflow.storage_settings.shared_fs_usage:
            # use relative path to Snakefile
            self.snakefile = os.path.relpath(workflow.main_snakefile)

        self.is_default_jobscript = False
        jobscript = workflow.remote_execution_settings.jobscript
        if jobscript is None:
            jobscript = os.path.join(os.path.dirname(__file__), self.default_jobscript)
            self.is_default_jobscript = True
        try:
            with open(jobscript) as f:
                self.jobscript = f.read()
        except IOError as e:
            raise WorkflowError(e)

        if "{jobid}" not in self.jobname:
            raise WorkflowError(
                f'Defined jobname ("{self.jobname}") has '
                f"to contain the wildcard {{jobid}}."
            )

        self._tmpdir = None

        self.active_jobs = list()
        self.lock = threading.Lock()
        self.wait = True
        self.wait_thread = threading.Thread(target=self._wait_thread)
        self.wait_thread.daemon = True
        self.wait_thread.start()

        max_status_checks_frac = Fraction(
            self.max_status_checks_per_second
        ).limit_denominator()
        self.status_rate_limiter = Throttler(
            rate_limit=max_status_checks_frac.numerator,
            period=max_status_checks_frac.denominator,
        )

        self.__post_init__()

    @property
    def cores(self):
        cores = self.workflow.resource_settings.cores
        # if constrained, pass this info to the job
        if cores is not None and cores != sys.maxsize:
            return cores
        # otherwise, use whatever the node provides
        return "all"

    def cancel(self):
        with self.lock:
            active_jobs = list(self.active_jobs)
        self.cancel_jobs(active_jobs)
        self.shutdown()

    @abstractmethod
    def cancel_jobs(self, active_jobs: List[SubmittedJobInfo]):
        """Cancel the given jobs.

        This method is called when the workflow is cancelled.
        """
        ...

    def get_exec_mode(self) -> ExecMode:
        return ExecMode.REMOTE

    def get_python_executable(self):
        return (
            sys.executable
            if SharedFSUsage.SOFTWARE_DEPLOYMENT
            in self.workflow.storage_settings.shared_fs_usage
            else "python"
        )

    def get_job_args(self, job: JobExecutorInterface):
        waitfiles_parameter = ""
        if SharedFSUsage.INPUT_OUTPUT in self.workflow.storage_settings.shared_fs_usage:
            wait_for_files = []
            wait_for_files.append(self.tmpdir)
            wait_for_files.extend(job.get_wait_for_files())

            # Only create extra file if we have more than 20 input files.
            # This should not require the file creation in most cases.
            if len(wait_for_files) > 20:
                wait_for_files_file = self.get_jobscript(job) + ".waitforfilesfile.txt"
                with open(wait_for_files_file, "w") as fd:
                    print(*wait_for_files, sep="\n", file=fd)

                waitfiles_parameter = format_cli_arg(
                    "--wait-for-files-file", wait_for_files_file
                )
            else:
                waitfiles_parameter = format_cli_arg("--wait-for-files", wait_for_files)

        return f"{super().get_job_args(job)} {waitfiles_parameter}"

    def report_job_submission(
        self, job_info: SubmittedJobInfo, register_job: bool = True
    ):
        super().report_job_submission(job_info, register_job=register_job)
        with self.lock:
            self.active_jobs.append(job_info)

    @abstractmethod
    async def check_active_jobs(
        self, active_jobs: List[SubmittedJobInfo]
    ) -> Generator[SubmittedJobInfo, None, None]:
        """Check the status of active jobs.

        You have to iterate over the given list active_jobs.
        For jobs that have finished successfully, you have to call
        self.report_job_success(job).
        For jobs that have errored, you have to call
        self.report_job_error(job).
        Jobs that are still running have to be yielded.
        """
        ...

    async def _wait_for_jobs(self):
        await asyncio.sleep(
            self.workflow.executor_plugin.common_settings.init_seconds_before_status_checks
        )
        while True:
            async with async_lock(self.lock):
                if not self.wait:
                    return
                active_jobs = list(self.active_jobs)
                self.active_jobs.clear()
            still_active_jobs = [
                job_info async for job_info in self.check_active_jobs(active_jobs)
            ]
            async with async_lock(self.lock):
                # re-add the remaining jobs to active_jobs
                self.active_jobs.extend(still_active_jobs)
            await self.sleep()

    def _wait_thread(self):
        try:
            asyncio.run(self._wait_for_jobs())
        except Exception as e:
            print(e)
            if self.workflow.scheduler is not None:
                self.workflow.scheduler.executor_error_callback(e)

    def shutdown(self):
        with self.lock:
            self.wait = False
        self.wait_thread.join()
        if not self.workflow.remote_execution_settings.immediate_submit:
            # Only delete tmpdir (containing jobscripts) if not using
            # immediate_submit. With immediate_submit, jobs can be scheduled
            # after this method is completed. Hence we have to keep the
            # directory.
            shutil.rmtree(self.tmpdir, ignore_errors=True)

    @property
    def tmpdir(self):
        if self._tmpdir is None:
            self._tmpdir = tempfile.mkdtemp(dir=".snakemake", prefix="tmp.")
        return os.path.abspath(self._tmpdir)

    def get_jobname(self, job: JobExecutorInterface):
        return job.format_wildcards(self.jobname)

    def get_jobscript(self, job: JobExecutorInterface):
        f = self.get_jobname(job)

        if os.path.sep in f:
            raise WorkflowError(
                "Path separator ({}) found in job name {}. "
                "This is not supported.".format(os.path.sep, f)
            )

        return os.path.join(self.tmpdir, f)

    def write_jobscript(self, job: JobExecutorInterface, jobscript):
        exec_job = self.format_job_exec(job)

        try:
            content = self.jobscript.format(
                properties=job.properties(),
                exec_job=exec_job,
            )
        except KeyError as e:
            if self.is_default_jobscript:
                raise e
            else:
                raise WorkflowError(
                    "Error formatting custom jobscript "
                    f"{self.jobscript}: value for {e} not found.\n"
                    "Make sure that your custom jobscript is defined as "
                    "expected."
                )

        self.logger.debug(f"Jobscript:\n{content}")
        with open(jobscript, "w") as f:
            print(content, file=f)
        os.chmod(jobscript, os.stat(jobscript).st_mode | stat.S_IXUSR | stat.S_IRUSR)

    def handle_job_success(self, job: JobExecutorInterface):
        super().handle_job_success(job)

    def print_job_error(self, job_info: SubmittedJobInfo, msg=None, **kwargs):
        msg = msg or ""
        msg += (
            "For further error details see the cluster/cloud "
            "log and the log files of the involved rule(s)."
        )
        if job_info.external_jobid is not None:
            kwargs["external_jobid"] = job_info.external_jobid
        super().print_job_error(job_info, msg=msg, **kwargs)

    async def sleep(self):
        duration = (
            self.workflow.remote_execution_settings.seconds_between_status_checks
            if self.next_seconds_between_status_checks is None
            else self.next_seconds_between_status_checks
        )
        await asyncio.sleep(duration)

    @property
    def next_seconds_between_status_checks(self):
        if self._next_seconds_between_status_checks is None:
            return self.workflow.remote_execution_settings.seconds_between_status_checks
        else:
            return self._next_seconds_between_status_checks

    @next_seconds_between_status_checks.setter
    def next_seconds_between_status_checks(self, value):
        self._next_seconds_between_status_checks = value
