from dataclasses import dataclass


@dataclass
class CommonSettings:
    """Common Snakemake settings shared between executors that can be specified
    by executor plugins.

    The plugin has to specify an instance of this class as the value of the
    common_settings attribute.
    """

    non_local_exec: bool
    use_threads: bool = False


@dataclass
class ExecutorSettingsBase:
    """Base class for executor settings.

    Executor plugins can define a subclass of this class,
    named 'ExecutorSettings'.
    """

    pass
