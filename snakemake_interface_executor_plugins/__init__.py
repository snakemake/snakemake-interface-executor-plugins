__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster, Vanessa Sochat"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from dataclasses import dataclass


@dataclass
class CommonSettings:
    """Common Snakemake settings shared between executors that can be specified
    by executor plugins.

    The plugin has to specify an instance of this class as the value of the
    common_settings attribute.

    Attributes
    ----------
    non_local_exec : bool
        Whether to execute jobs locally or on a cluster.
    force_no_shared_fs : bool
        Whether to the executor implies to not have a shared file system.
    dryrun_exec : bool
        Whether to jobs will be executed in dry-run mode.
    touch_exec : bool
        Whether job outputs will be touched only.
    use_threads : bool
        Whether to use threads instead of processes.
    """

    non_local_exec: bool
    implies_no_shared_fs: bool
    dryrun_exec: bool = False
    touch_exec: bool = False
    use_threads: bool = False

    @property
    def local_exec(self):
        return not self.non_local_exec


@dataclass
class ExecutorSettingsBase:
    """Base class for executor settings.

    Executor plugins can define a subclass of this class,
    named 'ExecutorSettings'.
    """

    pass
