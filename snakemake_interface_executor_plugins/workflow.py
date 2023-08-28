__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod

from snakemake_interface_executor_plugins.cli import (
    SpawnedJobArgsFactoryExecutorInterface,
)
from snakemake_interface_executor_plugins.persistence import (
    PersistenceExecutorInterface,
)

from snakemake_interface_executor_plugins.scheduler import JobSchedulerExecutorInterface
from snakemake_interface_executor_plugins.settings import (
    DeploymentSettingsExecutorInterface,
    ExecutionSettingsExecutorInterface,
    RemoteExecutionSettingsExecutorInterface,
    StorageSettingsExecutorInterface,
)


class WorkflowExecutorInterface(ABC):
    @property
    @abstractmethod
    def spawned_job_args_factory(self) -> SpawnedJobArgsFactoryExecutorInterface:
        ...

    @property
    @abstractmethod
    def execution_settings(self) -> ExecutionSettingsExecutorInterface:
        ...

    @property
    @abstractmethod
    def remote_execution_settings(self) -> RemoteExecutionSettingsExecutorInterface:
        ...

    @property
    @abstractmethod
    def storage_settings(self) -> StorageSettingsExecutorInterface:
        ...

    @property
    @abstractmethod
    def deployment_settings(self) -> DeploymentSettingsExecutorInterface:
        ...

    @property
    @abstractmethod
    def resource_scopes(self):
        ...

    @abstractmethod
    def get_cache_mode(self, rule):
        ...

    @property
    @abstractmethod
    def main_snakefile(self):
        ...

    @property
    @abstractmethod
    def persistence(self) -> PersistenceExecutorInterface:
        ...

    @property
    @abstractmethod
    def linemaps(self):
        ...

    @property
    @abstractmethod
    def workdir_init(self):
        ...

    @property
    @abstractmethod
    def sourcecache(self):
        ...

    @property
    @abstractmethod
    def scheduler(self) -> JobSchedulerExecutorInterface:
        ...
