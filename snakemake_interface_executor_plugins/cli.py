from abc import ABC, abstractmethod
from typing import Mapping

from snakemake_interface_executor_plugins.settings import CommonSettings


class SpawnedJobArgsFactoryExecutorInterface(ABC):
    @abstractmethod
    def general_args(
        self,
        executor_common_settings: CommonSettings,
    ) -> str: ...

    @abstractmethod
    def precommand(self, executor_common_settings: CommonSettings) -> str: ...

    @abstractmethod
    def envvars(self) -> Mapping[str, str]: ...
