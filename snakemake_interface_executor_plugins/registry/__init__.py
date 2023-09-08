__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster, Vanessa Sochat"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

import types
import pkgutil
import importlib
from snakemake_interface_executor_plugins import CommonSettings, ExecutorSettingsBase

from snakemake_interface_executor_plugins.exceptions import InvalidPluginException
import snakemake_interface_executor_plugins._common as common
from snakemake_interface_executor_plugins.executors.base import AbstractExecutor
from snakemake_interface_executor_plugins.registry.attribute_types import (
    AttributeKind,
    AttributeMode,
    AttributeType,
)
from snakemake_interface_executor_plugins.registry.plugin import Plugin


class ExecutorPluginRegistry:
    """This class is a singleton that holds all registered executor plugins."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "plugins"):
            # init has been called before
            return
        self._collect_plugins()

    def get_plugin(self, plugin_name):
        """Get a plugin by name."""
        return self.plugins[plugin_name.replace("-", "_")]

    def register_cli_args(self, argparser):
        """Add arguments derived from self.executor_settings to given
        argparser."""
        for _, plugin in self.plugins.items():
            plugin.register_cli_args(argparser)

    def _collect_plugins(self):
        """Collect plugins and call _register_plugin for each."""
        self.plugins = dict()

        # Executor plugins are externally installed plugins named
        # "snakemake_executor_<name>".
        # They should follow the same convention if on pip,
        # snakemake-executor-<name>.
        # Note that these will not be detected installed in editable
        # mode (pip install -e .).
        for moduleinfo in pkgutil.iter_modules():
            if not moduleinfo.ispkg or not moduleinfo.name.startswith(
                common.executor_plugin_module_prefix
            ):
                continue
            module = importlib.import_module(moduleinfo.name)
            self.register_plugin(moduleinfo.name, module)

    def register_plugin(self, name: str, plugin: types.ModuleType):
        """Validate and register a plugin.

        Does nothing if the plugin is already registered.
        """
        if name in self.plugins:
            return

        self._validate_plugin(name, plugin)

        # Derive the shortened name for future access
        plugin_name = name.removeprefix(common.executor_plugin_module_prefix)

        self.plugins[plugin_name] = Plugin(
            plugin_name,
            plugin.Executor,
            common_settings=plugin.common_settings,
            _executor_settings_cls=getattr(plugin, "ExecutorSettings", None),
        )

    def _validate_plugin(self, name: str, module: types.ModuleType):
        """Validate a plugin for attributes and naming"""
        expected_attributes = {
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
        for attr, attr_type in expected_attributes.items():
            # check if attr is missing and fail if it is not optional
            if not hasattr(module, attr):
                if attr_type.is_optional:
                    continue
                raise InvalidPluginException(name, f"plugin does not define {attr}.")

            attr_value = getattr(module, attr)
            if attr_type.is_class:
                # check for class type
                if not issubclass(attr_value, attr_type.cls):
                    raise InvalidPluginException(
                        name,
                        f"{attr} must be a subclass of "
                        f"{attr_type.cls.__module__}.{attr_type.cls.__name__}.",
                    )
            else:
                # check for instance type
                if not isinstance(attr_value, attr_type.cls):
                    raise InvalidPluginException(
                        name, f"{attr} must be of type {attr_type.cls.__name__}."
                    )
