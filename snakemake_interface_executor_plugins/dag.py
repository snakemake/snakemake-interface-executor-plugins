__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod
from typing import Iterable, Optional

from snakemake_interface_executor_plugins.jobs import JobExecutorInterface


class DAGExecutorInterface(ABC):
    @abstractmethod
    def incomplete_external_jobid(self, job: JobExecutorInterface) -> Optional[str]: ...

    @abstractmethod
    def get_sources(self) -> Iterable[str]: ...

    @abstractmethod
    def get_unneeded_temp_files(self, job: JobExecutorInterface) -> Iterable[str]: ...
