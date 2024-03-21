from typing import List
from snakemake_interface_executor_plugins.registry import ExecutorPluginRegistry
from snakemake_interface_common.plugin_registry.tests import TestRegistryBase
from snakemake_interface_common.plugin_registry.plugin import PluginBase, SettingsBase
from snakemake_interface_common.plugin_registry import PluginRegistryBase
from snakemake_interface_executor_plugins.utils import format_cli_arg


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

    def get_example_args(self) -> List[str]:
        return ["--cluster-generic-submit-cmd", "qsub"]


def test_format_cli_arg_single_quote():
    fmt = format_cli_arg("--default-resources", {"slurm_extra": "'--gres=gpu:1'"})
    assert fmt == "--default-resources \"slurm_extra='--gres=gpu:1'\""


def test_format_cli_arg_double_quote():
    fmt = format_cli_arg("--default-resources", {"slurm_extra": '"--gres=gpu:1"'})
    assert fmt == "--default-resources 'slurm_extra=\"--gres=gpu:1\"'"


def test_format_cli_arg_int():
    fmt = format_cli_arg("--default-resources", {"mem_mb": 200})
    assert fmt == "--default-resources 'mem_mb=200'"


def test_format_cli_arg_expr():
    fmt = format_cli_arg(
        "--default-resources", {"mem_mb": "min(2 * input.size_mb, 2000)"}
    )
    assert fmt == "--default-resources 'mem_mb=min(2 * input.size_mb, 2000)'"


def test_format_cli_arg_list():
    fmt = format_cli_arg("--config", ["foo={'bar': 1}"])
    assert fmt == "--config \"foo={'bar': 1}\""
