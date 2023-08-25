from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Self, Set

from snakemake_interface_common.settings import SettingsEnumBase

class RemoteExecutionSettingsExecutorInterface(ABC):
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
    def max_status_checks_per_second(self) -> int:
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

    @property
    @abstractmethod
    def debug(self) -> bool:
        ...
    
    @property
    @abstractmethod
    def cleanup_scripts(self) -> bool:
        ...

    @property
    @abstractmethod
    def edit_notebook(self) -> Optional[Path]:
        ...


class ResourceSettingsExecutorInterface(ABC):
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


class ConfigSettingsExecutorInterface(ABC):
    ...


class OutputSettingsExecutorInterface(ABC):
    ...
