__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod


class JobSchedulerExecutorInterface(ABC):
    @abstractmethod
    def executor_error_callback(self, exception: Exception) -> None: ...
