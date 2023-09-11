# Stable interfaces and functionality for Snakemake executor plugins

This package provides a stable interface for interactions between Snakemake and its executor plugins (WIP).

Plugins should implement the following skeleton to comply with this interface:

```python

from snakemake_interface_executor_plugins.executors.remote import RemoteExecutor
from snakemake_interface_executor_plugins import ExecutorSettingsBase, CommonSettings

# Optional:
# Define additional settings for your executor.
# They will occur in the Snakemake CLI as --<executor-name>-<param-name>
# Omit this class if you don't need any.
# Make sure that all defined fields are Optional and specify a default value
# of None or anything else that makes sense in your case.
@dataclass
class ExecutorSettings(ExecutorSettingsBase):
    myparam: Optional[int]=field(
        default=None,
        metadata={
            "help": "Some help text", 
            # Optionally request that setting is also available for specification
            # via an environment variable. The variable will be named automatically as
            # SNAKEMAKE_<executor-name>_<param-name>, all upper case.
            # This mechanism should only be used for passwords and usernames.
            # For other items, we rather recommend to let people use a profile
            # for setting defaults
            # (https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles).
            "env_var": False,
            # Optionally specify that setting is required when the executor is in use.
            "required": True
        }
    )


# Required:
# Specify common settings shared by various executors.
common_settings = CommonSettings(
    # define whether your executor plugin executes locally
    # or remotely. In virtually all cases, it will be remote execution
    # (cluster, cloud, etc.). Only Snakemake's standard execution 
    # plugins (snakemake-executor-plugin-dryrun, snakemake-executor-plugin-local)
    # are expected to specify False here.
    non_local_exec=True
)


# Required:
# Implementation of your executor
class Executor(RemoteExecutor)
    def __init__(
        self,
        workflow: WorkflowExecutorInterface,
        logger: LoggerExecutorInterface,

    ):
        super().__init__(
            workflow,
            logger,
            executor_settings,
            # configure behavior of RemoteExecutor below
            pass_default_remote_provider_args=True,  # whether arguments for setting the remote provider shall  be passed to jobs
            pass_default_resources_args=True,  # whether arguments for setting default resources shall be passed to jobs
            pass_envvar_declarations_to_cmd=True,  # whether environment variables shall be passed to jobs
        )
        # access executor specific settings 
        self.executor_settings
        # access workflow
        self.workflow

        # IMPORTANT: in your plugin, only access methods and properties of Snakemake objects (like Workflow, Persistence, etc.)
        # that are defined in the interfaces found in THIS package. Other parts of those objects
        # are NOT guaranteed to remain the same across new releases.

        # To ensure that the used interfaces are not changing, you should depend on this package as
        # >=a.b.c,<d with d=a+1 (i.e. pin the dependency on this package to be at least the version at time of development
        # and less than the next major version which would introduce breaking changes).

    async def _wait_for_jobs(self):
        # implement here a loop that checks which jobs are already finished
        
```
