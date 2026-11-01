__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod
from typing import Callable
from snakemake_interface_executor_plugins.jobs import JobExecutorInterface


class JobSchedulerExecutorInterface(ABC):
    submit_callback: Callable[[JobExecutorInterface], None]
    finish_callback: Callable[[JobExecutorInterface], None]
    error_callback: Callable[[JobExecutorInterface], None]

    @abstractmethod
    def executor_error_callback(self, exception: Exception) -> None: ...
