__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster, Vanessa Sochat"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from dataclasses import dataclass
from typing import Optional, Type
from snakemake_interface_executor_plugins.settings import (
    CommonSettings,
    ExecutorSettingsBase,
)
import snakemake_interface_executor_plugins._common as common

from snakemake_interface_common.plugin_registry.plugin import PluginBase


@dataclass
class Plugin(PluginBase):
    executor: object
    common_settings: CommonSettings
    _executor_settings_cls: Optional[Type[ExecutorSettingsBase]]
    _name: str

    @property
    def name(self):
        return self._name

    @property
    def cli_prefix(self):
        return self.name.replace(common.executor_plugin_module_prefix, "")

    @property
    def settings_cls(self):
        return self._executor_settings_cls
