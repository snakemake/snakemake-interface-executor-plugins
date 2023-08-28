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
    """

    non_local_exec: bool
    dryrun_exec: bool = False
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
