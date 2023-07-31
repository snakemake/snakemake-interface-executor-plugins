# Stable interfaces and functionality for Snakemake executor plugins

This package provides a stable interface for interactions between Snakemake and its executor plugins (WIP).

Plugins should implement the following skeleton to comply with this interface:

```python

from snakemake_interface_executor_plugins.executors.remote import RemoteExecutor
from snakemake_interface_executor_plugins import ExecutorSettingsBase, CommonSettings

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
class Executor(RemoteExecutor)
    def __init__(
        self,
        workflow: WorkflowExecutorInterface,
        dag: DAGExecutorInterface,
        stats: StatsExecutorInterface,
        logger: LoggerExecutorInterface,
        executor_settings: Optional[ExecutorSettings], # if no ExecutorSettings are defined above, this will receive None
    ):
    super().__init__(
        workflow,
        dag,
        stats,
        logger,
        executor_settings,
        # configure behavior of RemoteExecutor below
        max_status_checks_per_second=1, # how many status checks should be performed per second
        disable_default_remote_provider_args=False, # whether arguments for setting the remote provider shall not be passed to jobs
        disable_default_resources_args=False, # whether arguments for setting default resources shall not be passed to jobs
        disable_envvar_declarations=False, # whether environment variables shall not be passed to jobs
    )
    # access executor specific settings 
    self.executor_settings
```
