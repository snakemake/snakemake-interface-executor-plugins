__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster, Vanessa Sochat"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

import types
from typing import Mapping
from snakemake_interface_executor_plugins.settings import (
    CommonSettings,
    ExecutorSettingsBase,
)

from snakemake_interface_common.plugin_registry.attribute_types import (
    AttributeKind,
    AttributeMode,
    AttributeType,
)
from snakemake_interface_executor_plugins.registry.plugin import Plugin
from snakemake_interface_common.plugin_registry import PluginRegistryBase
from snakemake_interface_executor_plugins import _common as common


class ExecutorPluginRegistry(PluginRegistryBase):
    """This class is a singleton that holds all registered executor plugins."""

    @property
    def module_prefix(self) -> str:
        return common.executor_plugin_module_prefix

    def load_plugin(self, name: str, module: types.ModuleType) -> Plugin:
        """Load a plugin by name."""
        return Plugin(
            _name=name,
            executor=module.Executor,
            common_settings=module.common_settings,
            _executor_settings_cls=getattr(module, "ExecutorSettings", None),
        )

    def expected_attributes(self) -> Mapping[str, AttributeType]:
        # break otherwise circular import
        from snakemake_interface_executor_plugins.executors.base import AbstractExecutor

        return {
            "common_settings": AttributeType(
                cls=CommonSettings,
                mode=AttributeMode.REQUIRED,
                kind=AttributeKind.OBJECT,
            ),
            "ExecutorSettings": AttributeType(
                cls=ExecutorSettingsBase,
                mode=AttributeMode.OPTIONAL,
                kind=AttributeKind.CLASS,
            ),
            "Executor": AttributeType(
                cls=AbstractExecutor,
                mode=AttributeMode.REQUIRED,
                kind=AttributeKind.CLASS,
            ),
        }

    def collect_plugins(self):
        """Collect plugins and call register_plugin for each."""
        super().collect_plugins()

        try:
            from snakemake.executors import local as local_executor
            from snakemake.executors import dryrun as dryrun_executor
            from snakemake.executors import touch as touch_executor
        except ImportError:
            # snakemake not present, proceed without adding these plugins
            return

        for executor in [local_executor, dryrun_executor, touch_executor]:
            self.register_plugin(executor.__name__, executor)
