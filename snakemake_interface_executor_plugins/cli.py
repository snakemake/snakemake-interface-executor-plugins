from abc import ABC, abstractmethod
from typing import List


class SpawnedJobArgsFactoryExecutorInterface(ABC):
    @property
    @abstractmethod
    def general_args(self) -> str:
        ...