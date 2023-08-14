from abc import ABC, abstractmethod
from typing import List


class DefaultResourcesExecutorInterface(ABC):
    @property
    @abstractmethod
    def args(self) -> List[str]:
        ...