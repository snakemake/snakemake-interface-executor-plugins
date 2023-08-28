from abc import ABC, abstractmethod


class SpawnedJobArgsFactoryExecutorInterface(ABC):
    @abstractmethod
    def general_args(
        self,
        pass_default_remote_provider_args: bool = True,
        pass_default_resources_args: bool = False,
    ) -> str:
        ...
