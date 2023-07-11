__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod


class PersistenceExecutorInterface(ABC):
    @abstractmethod
    def cleanup(self):
        ...

    @property
    @abstractmethod
    def path(self):
        ...

    @property
    @abstractmethod
    def aux_path(self):
        ...