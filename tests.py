from snakemake_executor_plugin_interface import ExecutorPluginRegistry
from snakemake.executors import AbstractExecutor

def test_registry():
    registry = ExecutorPluginRegistry(executor_base_cls=AbstractExecutor)
    assert len(registry.plugins) == 1
    plugin = registry.plugins["flux"]
    assert plugin._executor_settings_cls is not None
    assert plugin.common_settings.non_local_exec is True
    assert isinstance(plugin.executor, AbstractExecutor)