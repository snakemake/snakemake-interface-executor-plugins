from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Sequence, Set

from snakemake_interface_common.settings import SettingsEnumBase, TSettingsEnumBase


import snakemake_interface_common.plugin_registry.plugin


@dataclass
class CommonSettings:
    """Common Snakemake settings shared between executors that can be specified
    by executor plugins.

    The plugin has to specify an instance of this class as the value of the
    common_settings attribute.

    Attributes
    ----------
    non_local_exec : bool
        Whether to execute jobs locally or on a cluster.
    implies_no_shared_fs : bool
        Whether the executor implies to not have a shared file system.
    dryrun_exec : bool
        Whether jobs will be executed in dry-run mode.
    job_deploy_sources : bool
        Whether to deploy workflow sources before job execution. This is e.g.
        needed when remote jobs are guaranteed to be not executed on a shared
        filesystem. For example, this is True in the kubernetes executor plugin.
    touch_exec : bool
        Whether job outputs will be touched only.
    use_threads : bool
        Whether to use threads instead of processes.
    pass_default_storage_provider_args : bool
        Whether to pass default storage provider arguments to spawned jobs.
    pass_default_resources_args : bool
        Whether to pass default resources arguments to spawned jobs.
    pass_envvar_declarations_to_cmd : bool
        Whether envvars shall be declared in the job command. If false, envvars
        have to be declared in a different way by the executor, e.g. by passing
        them as secrets (see snakemake-executor-plugin-kubernetes).
    auto_deploy_default_storage_provider : bool
        Whether to automatically deploy the default storage provider in the spawned
        job via pip. This is usually needed in case the executor does not have a
        shared file system.
    init_seconds_before_status_checks : int
        Number of seconds to wait before starting to check the status of spawned jobs.
    pass_group_args : bool
        Whether to pass group arguments to spawned jobs.
    spawned_jobs_assume_shared_fs: bool
        Whether spawned jobs in the executor should always assume a shared FS regardless
        of the user provided settings. This should be True if the executor spawns
        another non-local executor that runs jobs on the same node.
        For example, it is used in snakemake-executor-plugin-slurm-jobstep.
    can_transfer_local_files: bool
        Indicates whether the plugin can transfer local files to the remote executor when
        run without a shared FS. If true, it's the plugin's responsibility and not
        Snakemake's to manage file transfers.
    """

    non_local_exec: bool
    implies_no_shared_fs: bool
    job_deploy_sources: bool
    dryrun_exec: bool = False
    touch_exec: bool = False
    use_threads: bool = False
    pass_default_storage_provider_args: bool = True
    pass_default_resources_args: bool = True
    pass_envvar_declarations_to_cmd: bool = True
    auto_deploy_default_storage_provider: bool = True
    init_seconds_before_status_checks: int = 0
    pass_group_args: bool = False
    spawned_jobs_assume_shared_fs: bool = False
    can_transfer_local_files: bool = False

    @property
    def local_exec(self):
        return not self.non_local_exec


@dataclass
class ExecutorSettingsBase(
    snakemake_interface_common.plugin_registry.plugin.SettingsBase
):
    """Base class for executor settings.

    Executor plugins can define a subclass of this class,
    named 'ExecutorSettings'.
    """

    pass


class RemoteExecutionSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def jobname(self) -> str: ...

    @property
    @abstractmethod
    def jobscript(self) -> str: ...

    @property
    @abstractmethod
    def immediate_submit(self) -> bool: ...

    @property
    @abstractmethod
    def envvars(self) -> Sequence[str]: ...

    @property
    @abstractmethod
    def max_status_checks_per_second(self) -> float: ...

    @property
    @abstractmethod
    def seconds_between_status_checks(self) -> int: ...


class ExecMode(SettingsEnumBase):
    """
    Enum for execution mode of Snakemake.
    This handles the behavior of e.g. the logger.
    """

    DEFAULT = 0
    SUBPROCESS = 1
    REMOTE = 2


class ExecutionSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def keep_incomplete(self) -> bool: ...


class SharedFSUsage(SettingsEnumBase):
    PERSISTENCE = 0
    INPUT_OUTPUT = 1
    SOFTWARE_DEPLOYMENT = 2
    SOURCES = 3
    STORAGE_LOCAL_COPIES = 4
    SOURCE_CACHE = 5

    @classmethod
    def choices(cls) -> List[str]:
        return super().choices() + ["none"]

    @classmethod
    def _parse_choices_into(cls, choices: str, container) -> List[TSettingsEnumBase]:
        if "none" in choices:
            if len(choices) > 1:
                raise ValueError(
                    "Cannot specify 'none' together with other shared filesystem usages."
                )
            return container([])
        else:
            return container(cls.parse_choice(choice) for choice in choices)


class StorageSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def shared_fs_usage(self) -> Set[SharedFSUsage]: ...

    @property
    def assume_common_workdir(self) -> bool:
        return any(
            usage in self.shared_fs_usage
            for usage in (
                SharedFSUsage.PERSISTENCE,
                SharedFSUsage.INPUT_OUTPUT,
                SharedFSUsage.SOFTWARE_DEPLOYMENT,
            )
        )


class DeploymentMethod(SettingsEnumBase):
    CONDA = 0
    APPTAINER = 1
    ENV_MODULES = 2


class DeploymentSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def deployment_method(self) -> Set[DeploymentMethod]: ...


class GroupSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def local_groupid(self) -> str: ...
