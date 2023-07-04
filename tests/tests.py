import argparse
from snakemake_executor_plugin_interface import ExecutorPluginRegistry
from snakemake.executors import AbstractExecutor

def test_registry_collect_plugins():
    registry = ExecutorPluginRegistry(executor_base_cls=AbstractExecutor)
    assert len(registry.plugins) == 1
    plugin = registry.plugins["flux"]
    assert plugin._executor_settings_cls is not None
    assert plugin.common_settings.non_local_exec is True
    assert issubclass(plugin.executor, AbstractExecutor)


def test_registry_register_cli_args():
    registry = ExecutorPluginRegistry(executor_base_cls=AbstractExecutor)
    parser = argparse.ArgumentParser()
    registry.register_cli_args(parser)
    for action in parser._actions:
        if not action.dest == "help":
            assert action.dest.startswith("flux")


def test_registry_get_executor_settings():
    registry = ExecutorPluginRegistry(executor_base_cls=AbstractExecutor)
    parser = argparse.ArgumentParser()
    registry.register_cli_args(parser)
    args = parser.parse_args([])
    plugin = registry.plugins["flux"]
    settings = plugin.get_executor_settings(args)
    assert isinstance(settings, plugin._executor_settings_cls)