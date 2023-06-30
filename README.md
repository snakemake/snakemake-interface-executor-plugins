# snakemake-executor-plugin-interface

This package provides a stable interface for interactions between Snakemake and its executor plugins (WIP).

Plugins should implement the following skeleton to comply with this interface:

```python

from snakemake.executors import ClusterExecutor
from snakemake_executor_plugin_interface import ExecutorSettingsBase, CommonSettings

# Optional:
# define additional settings for your executor
# They will occur in the Snakemake CLI as --<executor-name>-<param-name>
# Omit this class if you don't need any.
@dataclass
class ExecutorSettings:
    
    myparam: int=field(default=None, metadata={"help": "Some help text"})


# Optional:
# specify common settings shared by various executors.
# Omit this statement if you don't need any and want
# to rely on the defaults (highly recommended unless
# you are very sure what you do).
common_settings = CommonSettings(
    use_threads=True
)


# Required:
# Implementation of your executor
class Executor(ClusterExecutor)
    ...

```