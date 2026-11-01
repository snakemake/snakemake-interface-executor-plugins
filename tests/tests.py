from typing import List
from types import SimpleNamespace
from unittest.mock import Mock, patch
import pytest
from snakemake_interface_executor_plugins.executors.real import RealExecutor
from snakemake_interface_executor_plugins.executors.remote import RemoteExecutor
from snakemake_interface_executor_plugins.registry import ExecutorPluginRegistry
from snakemake_interface_common.plugin_registry.tests import TestRegistryBase
from snakemake_interface_common.plugin_registry.plugin import PluginBase, SettingsBase
from snakemake_interface_common.plugin_registry import PluginRegistryBase
from snakemake_interface_executor_plugins.utils import format_cli_arg
from snakemake_interface_executor_plugins.settings import SharedFSUsage


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


def test_shared_fs_usage_parses_none_and_regular_choices():
    assert SharedFSUsage.parse_choices_list(["none"]) == []
    assert SharedFSUsage.parse_choices_set(["none"]) == set()
    assert SharedFSUsage.parse_choices_list(["input-output"]) == [
        SharedFSUsage.INPUT_OUTPUT
    ]
    assert SharedFSUsage.parse_choices_set(["input-output"]) == {
        SharedFSUsage.INPUT_OUTPUT
    }
    with pytest.raises(ValueError, match="Cannot specify 'none'"):
        SharedFSUsage.parse_choices_set(["none", "input-output"])


def test_remote_job_args_forward_cores_to_real_executor():
    class StubRemote(RemoteExecutor):
        def run_job(self, job):
            pass

        def cancel_jobs(self, active_jobs):
            pass

        async def check_active_jobs(self, active_jobs):
            pass

    remote = object.__new__(StubRemote)
    remote.workflow = SimpleNamespace(
        storage_settings=SimpleNamespace(shared_fs_usage=set())
    )
    job = Mock()
    with patch.object(RealExecutor, "get_job_args", return_value="--cores 2") as parent:
        result = remote.get_job_args(job, cores=2)

    parent.assert_called_once_with(job, cores=2)
    assert "--cores 2" in result
