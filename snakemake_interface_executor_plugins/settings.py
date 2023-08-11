from abc import ABC, abstractmethod
from typing import Dict, Optional


class RemoteExecutionSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def jobscript(self) -> str:
        ...

    @property
    @abstractmethod
    def immediate_submit(self) -> bool:
        ...

class ExecutionSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def cleanup_scripts(self) -> bool:
        ...


class ResourceSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def overwrite_resources(self) -> Dict[str, Dict[str, int]]:
        ...
    
    @property
    @abstractmethod
    def overwrite_threads(self) -> Dict[str, int]:
        ...


class StorageSettingsExecutorInterface(ABC):
    ...


class DeploymentSettingsExecutorInterface(ABC):
    ...


class ConfigSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def config_args(self) -> Optional[str]:
        ...


class OutputSettingsExecutorInterface(ABC):
    ...