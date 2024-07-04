__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from abc import ABC, abstractmethod
import sys
from typing import Any, Iterable, Mapping, Optional, Sequence, Union

from snakemake_interface_common.rules import RuleInterface


class JobExecutorInterface(ABC):
    HIGHEST_PRIORITY = sys.maxsize

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def jobid(self) -> int: ...

    @abstractmethod
    def logfile_suggestion(self, prefix: str) -> str: ...

    @abstractmethod
    def is_group(self) -> bool: ...

    @abstractmethod
    def log_info(self, skip_dynamic: bool = False) -> None: ...

    @abstractmethod
    def log_error(self, msg: Optional[str] = None, **kwargs) -> None: ...

    @abstractmethod
    def properties(
        self, omit_resources: Sequence[str] = ("_cores", "_nodes"), **aux_properties
    ) -> Mapping[str, Any]: ...

    @property
    @abstractmethod
    def resources(self) -> Mapping[str, Union[int, str]]: ...

    @property
    @abstractmethod
    def is_local(self) -> bool: ...

    @property
    @abstractmethod
    def is_updated(self) -> bool: ...

    @property
    @abstractmethod
    def output(self) -> Iterable[str]: ...

    @abstractmethod
    def register(self, external_jobid: Optional[str] = None) -> None: ...

    @abstractmethod
    def get_target_spec(self) -> str: ...

    @abstractmethod
    def rules(self) -> Iterable[RuleInterface]: ...

    @property
    @abstractmethod
    def attempt(self) -> int: ...

    @property
    @abstractmethod
    def input(self) -> Iterable[str]: ...

    @property
    @abstractmethod
    def threads(self) -> int: ...

    @property
    @abstractmethod
    def log(self) -> Iterable[str]: ...

    @abstractmethod
    def get_wait_for_files(self) -> Iterable[str]: ...

    @abstractmethod
    def format_wildcards(self, string, **variables) -> str: ...

    @property
    @abstractmethod
    def is_containerized(self) -> bool: ...


class SingleJobExecutorInterface(ABC):
    @property
    @abstractmethod
    def rule(self) -> RuleInterface: ...

    @property
    @abstractmethod
    def benchmark(self) -> Optional[str]: ...

    @property
    @abstractmethod
    def message(self): ...


class GroupJobExecutorInterface(ABC):
    @property
    @abstractmethod
    def jobs(self): ...

    @property
    @abstractmethod
    def groupid(self): ...

    @property
    @abstractmethod
    def toposorted(self): ...
