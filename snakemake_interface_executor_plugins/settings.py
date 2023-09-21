from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Set

from snakemake_interface_common.settings import SettingsEnumBase


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
    force_no_shared_fs : bool
        Whether to the executor implies to not have a shared file system.
    dryrun_exec : bool
        Whether to jobs will be executed in dry-run mode.
    touch_exec : bool
        Whether job outputs will be touched only.
    use_threads : bool
        Whether to use threads instead of processes.
    """

    non_local_exec: bool
    implies_no_shared_fs: bool
    dryrun_exec: bool = False
    touch_exec: bool = False
    use_threads: bool = False

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
    def jobname(self) -> str:
        ...

    @property
    @abstractmethod
    def jobscript(self) -> str:
        ...

    @property
    @abstractmethod
    def immediate_submit(self) -> bool:
        ...

    @property
    @abstractmethod
    def envvars(self) -> Optional[List[str]]:
        ...

    @property
    @abstractmethod
    def max_status_checks_per_second(self) -> float:
        ...

    @property
    @abstractmethod
    def seconds_between_status_checks(self) -> int:
        ...


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
    def keep_incomplete(self) -> bool:
        ...


class StorageSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def assume_shared_fs(self) -> bool:
        ...


class DeploymentMethod(SettingsEnumBase):
    CONDA = 0
    APPTAINER = 1
    ENV_MODULES = 2


class DeploymentSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def deployment_method(self) -> Set[DeploymentMethod]:
        ...


class GroupSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def local_groupid(self) -> str:
        ...
