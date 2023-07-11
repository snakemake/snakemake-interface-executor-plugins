__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod

from typing import Optional
from snakemake_interface_executor_plugins.persistence import (
    PersistenceExecutorInterface,
)

from snakemake_interface_executor_plugins.scheduler import JobSchedulerExecutorInterface


class WorkflowExecutorInterface(ABC):
    @property
    @abstractmethod
    def latency_wait(self) -> int:
        ...

    @property
    @abstractmethod
    def rerun_triggers(self) -> Optional[list[str]]:
        ...

    @property
    @abstractmethod
    def shadow_prefix(self) -> Optional[str]:
        ...

    @property
    @abstractmethod
    def conda_frontend(self) -> Optional[str]:
        ...

    @property
    @abstractmethod
    def conda_prefix(self) -> Optional[str]:
        ...

    @property
    @abstractmethod
    def conda_base_path(self) -> Optional[str]:
        ...

    @property
    @abstractmethod
    def singularity_args(self) -> Optional[str]:
        ...

    @property
    @abstractmethod
    def execute_subworkflows(self) -> bool:
        ...

    @property
    @abstractmethod
    def max_threads(self) -> Optional[int]:
        ...

    @property
    @abstractmethod
    def keep_metadata(self) -> bool:
        ...

    @property
    @abstractmethod
    def wrapper_prefix(self) -> Optional[str]:
        ...

    @property
    @abstractmethod
    def overwrite_threads(self) -> dict[str, int]:
        ...

    @property
    @abstractmethod
    def overwrite_scatter(self) -> dict[str, int]:
        ...

    @property
    @abstractmethod
    def local_groupid(self):
        ...

    @property
    @abstractmethod
    def conda_not_block_search_path_envvars(self):
        ...

    @property
    @abstractmethod
    def overwrite_configfiles(self):
        ...

    @property
    @abstractmethod
    def config_args(self):
        ...

    @property
    @abstractmethod
    def printshellcmds(self):
        ...

    @property
    @abstractmethod
    def scheduler_type(self):
        ...

    @property
    @abstractmethod
    def overwrite_resources(self):
        ...

    @property
    @abstractmethod
    def default_resources(self):
        ...

    @property
    @abstractmethod
    def overwrite_resource_scopes(self):
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
    def output_file_cache(self):
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
    def use_conda(self):
        ...

    @property
    @abstractmethod
    def use_singularity(self):
        ...

    @property
    @abstractmethod
    def use_env_modules(self):
        ...

    @property
    @abstractmethod
    def debug(self):
        ...

    @property
    @abstractmethod
    def cleanup_scripts(self):
        ...

    @property
    @abstractmethod
    def edit_notebook(self):
        ...

    @property
    @abstractmethod
    def sourcecache(self):
        ...

    @property
    @abstractmethod
    def verbose(self):
        ...

    @property
    @abstractmethod
    def jobscript(self):
        ...

    @property
    @abstractmethod
    def envvars(self):
        ...

    @property
    @abstractmethod
    def scheduler(self) -> JobSchedulerExecutorInterface:
        ...

    @property
    @abstractmethod
    def immediate_submit(self):
        ...

    @property
    @abstractmethod
    def default_remote_prefix(self):
        ...

    @property
    @abstractmethod
    def rules(self):
        ...

    @abstractmethod
    def get_rule(self, name):
        ...
