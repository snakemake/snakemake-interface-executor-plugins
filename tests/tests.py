from snakemake_interface_executor_plugins.registry import ExecutorPluginRegistry
from snakemake_interface_common.plugin_registry.tests import TestRegistryBase
from snakemake_interface_common.plugin_registry.plugin import PluginBase, SettingsBase
from snakemake_interface_common.plugin_registry import PluginRegistryBase


class TestRegistry(TestRegistryBase):
    __test__ = True

    def get_registry(self) -> PluginRegistryBase:
        # ensure that the singleton is reset
        ExecutorPluginRegistry._instance = None
        return ExecutorPluginRegistry()

    def get_test_plugin_name(self) -> str:
        return "cluster-generic"

    def validate_plugin(self, plugin: PluginBase):
        assert plugin._executor_settings_cls is not None
        assert plugin.common_settings.non_local_exec is True
        assert plugin.executor is not None

    def validate_settings(self, settings: SettingsBase, plugin: PluginBase):
        assert isinstance(settings, plugin._executor_settings_cls)
