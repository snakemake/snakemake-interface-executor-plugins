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
from snakemake_executor_plugin_interface.dag import DAGExecutorInterface
from snakemake_executor_plugin_interface.exceptions import WorkflowError
from snakemake_executor_plugin_interface.executors.real import RealExecutor
from snakemake_executor_plugin_interface.jobs import ExecutorJobInterface
from snakemake_executor_plugin_interface.logging import LoggerExecutorInterface
from snakemake_executor_plugin_interface.persistence import StatsExecutorInterface
from snakemake_executor_plugin_interface.utils import ExecMode, format_cli_arg
from snakemake_executor_plugin_interface.workflow import WorkflowExecutorInterface

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
        dag: DAGExecutorInterface,
        stats: StatsExecutorInterface,
        logger: LoggerExecutorInterface,
        cores,
        jobname="snakejob.{name}.{jobid}.sh",
        printreason=False,
        quiet=False,
        printshellcmds=False,
        local_input=None,
        restart_times=None,
        assume_shared_fs=True,
        max_status_checks_per_second=1,
        disable_default_remote_provider_args=False,
        disable_default_resources_args=False,
        disable_envvar_declarations=False,
        keepincomplete=False,
    ):
        local_input = local_input or []
        super().__init__(
            workflow,
            dag,
            stats,
            logger,
            printreason=printreason,
            quiet=quiet,
            printshellcmds=printshellcmds,
            assume_shared_fs=assume_shared_fs,
            keepincomplete=keepincomplete,
        )
        self.max_status_checks_per_second = max_status_checks_per_second

        if not self.assume_shared_fs:
            # use relative path to Snakefile
            self.snakefile = os.path.relpath(workflow.main_snakefile)

        self.is_default_jobscript = False
        jobscript = workflow.jobscript
        if jobscript is None:
            jobscript = os.path.join(os.path.dirname(__file__), self.default_jobscript)
            self.is_default_jobscript = True
        try:
            with open(jobscript) as f:
                self.jobscript = f.read()
        except IOError as e:
            raise WorkflowError(e)

        if "{jobid}" not in jobname:
            raise WorkflowError(
                f'Defined jobname ("{jobname}") has to contain the wildcard {{jobid}}.'
            )

        self.jobname = jobname
        self._tmpdir = None
        self.cores = cores if cores else "all"

        self.restart_times = restart_times

        self.active_jobs = list()
        self.lock = threading.Lock()
        self.wait = True
        self.wait_thread = threading.Thread(target=self._wait_thread)
        self.wait_thread.daemon = True
        self.wait_thread.start()

        self.disable_default_remote_provider_args = disable_default_remote_provider_args
        self.disable_default_resources_args = disable_default_resources_args
        self.disable_envvar_declarations = disable_envvar_declarations

        max_status_checks_frac = Fraction(
            max_status_checks_per_second
        ).limit_denominator()
        self.status_rate_limiter = Throttler(
            rate_limit=max_status_checks_frac.numerator,
            period=max_status_checks_frac.denominator,
        )

    def get_exec_mode(self):
        return ExecMode.remote

    def get_default_remote_provider_args(self):
        if not self.disable_default_remote_provider_args:
            return super().get_default_remote_provider_args()
        else:
            return ""

    def get_default_resources_args(self, default_resources=None):
        if not self.disable_default_resources_args:
            return super().get_default_resources_args(default_resources)
        else:
            return ""

    def get_workdir_arg(self):
        if self.assume_shared_fs:
            return super().get_workdir_arg()
        return ""

    def get_envvar_declarations(self):
        if not self.disable_envvar_declarations:
            return " ".join(
                f"{var}={repr(os.environ[var])}" for var in self.workflow.envvars
            )
        else:
            return ""

    def get_python_executable(self):
        return sys.executable if self.assume_shared_fs else "python"

    def get_job_args(self, job: ExecutorJobInterface):
        waitfiles_parameter = ""
        if self.assume_shared_fs:
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

    @abstractmethod
    async def _wait_for_jobs(self):
        ...

    def _wait_thread(self):
        try:
            asyncio.run(self._wait_for_jobs())
        except Exception as e:
            print(e)
            self.workflow.scheduler.executor_error_callback(e)

    def shutdown(self):
        with self.lock:
            self.wait = False
        self.wait_thread.join()
        if not self.workflow.immediate_submit:
            # Only delete tmpdir (containing jobscripts) if not using
            # immediate_submit. With immediate_submit, jobs can be scheduled
            # after this method is completed. Hence we have to keep the
            # directory.
            shutil.rmtree(self.tmpdir)

    def cancel(self):
        self.shutdown()

    def _run(self, job: ExecutorJobInterface, callback=None, error_callback=None):
        if self.assume_shared_fs:
            job.remove_existing_output()
            job.download_remote_input()
        super()._run(job, callback=callback, error_callback=error_callback)

    @property
    def tmpdir(self):
        if self._tmpdir is None:
            self._tmpdir = tempfile.mkdtemp(dir=".snakemake", prefix="tmp.")
        return os.path.abspath(self._tmpdir)

    def get_jobname(self, job: ExecutorJobInterface):
        return job.format_wildcards(self.jobname)

    def get_jobscript(self, job: ExecutorJobInterface):
        f = self.get_jobname(job)

        if os.path.sep in f:
            raise WorkflowError(
                "Path separator ({}) found in job name {}. "
                "This is not supported.".format(os.path.sep, f)
            )

        return os.path.join(self.tmpdir, f)

    def write_jobscript(self, job: ExecutorJobInterface, jobscript):
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
                    f"{self.workflow.jobscript}: value for {e} not found.\n"
                    "Make sure that your custom jobscript is defined as "
                    "expected."
                )

        self.logger.debug(f"Jobscript:\n{content}")
        with open(jobscript, "w") as f:
            print(content, file=f)
        os.chmod(jobscript, os.stat(jobscript).st_mode | stat.S_IXUSR | stat.S_IRUSR)

    def handle_job_success(self, job: ExecutorJobInterface):
        super().handle_job_success(
            job, upload_remote=False, handle_log=False, handle_touch=False
        )

    def handle_job_error(self, job: ExecutorJobInterface):
        # TODO what about removing empty remote dirs?? This cannot be decided
        # on the cluster node.
        super().handle_job_error(job, upload_remote=False)
        self.logger.debug("Cleanup job metadata.")
        # We have to remove metadata here as well.
        # It will be removed by the CPUExecutor in case of a shared FS,
        # but we might not see the removal due to filesystem latency.
        # By removing it again, we make sure that it is gone on the host FS.
        if not self.keepincomplete:
            self.workflow.persistence.cleanup(job)
            # Also cleanup the jobs output files, in case the remote job
            # was not able to, due to e.g. timeout.
            self.logger.debug("Cleanup failed jobs output files.")
            job.cleanup()

    def print_cluster_job_error(self, job_info, jobid):
        job = job_info.job
        kind = (
            f"rule {job.rule.name}"
            if not job.is_group()
            else f"group job {job.groupid}"
        )
        self.logger.error(
            "Error executing {} on cluster (jobid: {}, external: "
            "{}, jobscript: {}). For error details see the cluster "
            "log and the log files of the involved rule(s).".format(
                kind, jobid, job_info.jobid, job_info.jobscript
            )
        )
