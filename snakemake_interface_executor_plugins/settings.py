from abc import ABC, abstractmethod
from typing import Dict, List, Optional


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

class ExecutionSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def keep_incomplete(self) -> bool:
        ...


class ResourceSettingsExecutorInterface(ABC):
    ...


class StorageSettingsExecutorInterface(ABC):
    @property
    @abstractmethod
    def default_remote_prefix(self) -> Optional[str]:
        ...

    @property
    @abstractmethod
    def default_remote_provider(self) -> Optional[str]:
        ...
    
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