__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod

from snakemake_interface_executor_plugins.jobs import ExecutorJobInterface


class DAGExecutorInterface(ABC):
    @abstractmethod
    def is_edit_notebook_job(self, job: ExecutorJobInterface):
        ...

    @abstractmethod
    def incomplete_external_jobid(self, job: ExecutorJobInterface):
        ...

    @abstractmethod
    def jobid(self, job: ExecutorJobInterface):
        ...

    @abstractmethod
    def get_sources(self):
        ...
