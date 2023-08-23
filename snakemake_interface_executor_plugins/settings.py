from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Self, Set

from snakemake_interface_executor_plugins.resources import DefaultResourcesExecutorInterface


class ParseChoicesType(Enum):
    SET = 0
    LIST = 1


class SettingsEnumBase(Enum):
    parse_choices_type: ParseChoicesType = ParseChoicesType.SET

    @classmethod
    def choices(cls) -> List[str]:
        return sorted(item.item_to_choice() for item in cls)
    
    @classmethod
    def all(cls) -> Set[Self]:
        return {item for item in cls}
    
    @classmethod
    def parse_choices(cls, choices: str) -> List[Self]:
        container = set if cls.parse_choices_type == ParseChoicesType.SET else list
        return container(cls.parse_choice(choice) for choice in choices)
    
    @classmethod
    def parse_choice(cls, choice: str) -> Self:
        return choice.replace("-", "_").upper()
    
    def item_to_choice(self) -> str:
        return self.name.replace("_", "-").lower()
    
    def __str__(self):
        return self.item_to_choice()


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
