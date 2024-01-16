from abc import ABC, abstractmethod
from typing import Mapping


class SpawnedJobArgsFactoryExecutorInterface(ABC):
    @abstractmethod
    def general_args(
        self,
        pass_default_storage_provider_args: bool = True,
        pass_default_resources_args: bool = False,
        pass_group_args: bool = False,
    ) -> str:
        ...

    @abstractmethod
    def precommand(self) -> str:
        ...

    @abstractmethod
    def envvars(self) -> Mapping[str, str]:
        ...
