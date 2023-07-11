__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod

from snakemake_executor_plugin_interface.jobs import ExecutorJobInterface


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


class StatsExecutorInterface(ABC):
    @abstractmethod
    def report_job_start(self, job: ExecutorJobInterface):
        ...

    @abstractmethod
    def report_job_end(self, job: ExecutorJobInterface):
        ...

    @property
    @abstractmethod
    def rule_stats(self):
        ...

    @property
    @abstractmethod
    def file_stats(self):
        ...

    @property
    @abstractmethod
    def overall_runtime(self):
        ...

    @abstractmethod
    def to_json(self, path):
        ...
