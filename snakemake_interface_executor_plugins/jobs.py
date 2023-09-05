__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod
import sys


class ExecutorJobInterface(ABC):
    HIGHEST_PRIORITY = sys.maxsize

    @property
    @abstractmethod
    def name(self):
        ...

    @property
    @abstractmethod
    def jobid(self):
        ...

    @abstractmethod
    def logfile_suggestion(self, prefix: str) -> str:
        ...

    @abstractmethod
    def is_group(self):
        ...

    @abstractmethod
    def log_info(self, skip_dynamic=False):
        ...

    @abstractmethod
    def log_error(self, msg=None, **kwargs):
        ...

    @abstractmethod
    def remove_existing_output(self):
        ...

    @abstractmethod
    def download_remote_input(self):
        ...

    @abstractmethod
    def properties(self, omit_resources=("_cores", "_nodes"), **aux_properties):
        ...

    @property
    @abstractmethod
    def resources(self):
        ...

    @abstractmethod
    def check_protected_output(self):
        ...

    @property
    @abstractmethod
    def is_local(self):
        ...

    @property
    @abstractmethod
    def is_branched(self):
        ...

    @property
    @abstractmethod
    def is_updated(self):
        ...

    @property
    @abstractmethod
    def output(self):
        ...

    @abstractmethod
    def register(self, external_jobid: str = None):
        ...

    @abstractmethod
    def postprocess(self):
        ...

    @abstractmethod
    def get_target_spec(self):
        ...

    @abstractmethod
    def rules(self):
        ...

    @property
    @abstractmethod
    def attempt(self):
        ...

    @property
    @abstractmethod
    def input(self):
        ...

    @property
    @abstractmethod
    def threads(self) -> int:
        ...

    @property
    @abstractmethod
    def log(self):
        ...

    @abstractmethod
    def cleanup(self):
        ...

    @abstractmethod
    def get_wait_for_files(self):
        ...

    @abstractmethod
    def format_wildcards(self, string, **variables):
        ...

    @property
    @abstractmethod
    def needs_singularity(self):
        ...


class SingleJobExecutorInterface(ABC):
    @property
    @abstractmethod
    def rule(self):
        ...

    @abstractmethod
    def prepare(self):
        ...

    @property
    @abstractmethod
    def conda_env(self):
        ...

    @property
    @abstractmethod
    def container_img_path(self):
        ...

    @property
    @abstractmethod
    def env_modules(self):
        ...

    @property
    @abstractmethod
    def benchmark_repeats(self):
        ...

    @property
    @abstractmethod
    def benchmark(self):
        ...

    @property
    @abstractmethod
    def params(self):
        ...

    @property
    @abstractmethod
    def wildcards(self):
        ...

    @property
    @abstractmethod
    def shadow_dir(self):
        ...

    @property
    @abstractmethod
    def is_shadow(self):
        ...

    @property
    @abstractmethod
    def is_run(self):
        ...

    @property
    @abstractmethod
    def is_template_engine(self):
        ...

    @property
    @abstractmethod
    def message(self):
        ...


class GroupJobExecutorInterface(ABC):
    @property
    @abstractmethod
    def jobs(self):
        ...

    @property
    @abstractmethod
    def groupid(self):
        ...

    @property
    @abstractmethod
    def toposorted(self):
        ...
