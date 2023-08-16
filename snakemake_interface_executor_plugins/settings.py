from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional

from snakemake_interface_executor_plugins.resources import DefaultResourcesExecutorInterface


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


class DeploymentSettingsExecutorInterface(ABC):
    ...


class ConfigSettingsExecutorInterface(ABC):
    ...


class OutputSettingsExecutorInterface(ABC):
    ...