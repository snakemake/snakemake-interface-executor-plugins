__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod
from pathlib import Path


class PersistenceExecutorInterface(ABC):
    @property
    @abstractmethod
    def path(self) -> Path: ...

    @property
    @abstractmethod
    def aux_path(self) -> Path: ...
