from dataclasses import dataclass
import types
from typing import Optional
import typing

from snakemake_executor_plugin_interface.exceptions import InvalidPluginException


@dataclass
class CommonSettings:
    """Common Snakemake settings shared between executors that can be specified by executor plugins.

    The plugin can specify an instance of this class as the value of the common_settings attribute.
    """
    use_threads: bool = False


@dataclass
class ExecutorSettingsBase:
    """Base class for executor settings.
    
    Executor plugins can define a subclass of this class, named 'ExecutorSettings'.
    """
    pass


@dataclass
class Plugin:
    name: str
    executor: object
    common_settings: Optional[CommonSettings]
    _executor_settings_cls: Optional[type[ExecutorSettingsBase]]

    def register_cli_args(self, argparser):
        """Add arguments derived from self.executor_settings to given argparser."""
        ...

    def get_executor_settings(self, args) -> Optional[ExecutorSettingsBase]:
        """Return an instance of self.executor_settings with values from args."""
        ...



class ExecutorPluginRegistry:
    """This class is a singleton that holds all registered executor plugins."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, executor_base_cls: type[object]):
        if hasattr(self, "executor_base_cls"):
            # init has been called before
            return
        self.executor_base_cls = executor_base_cls
        self._collect_plugins()

    def _collect_plugins(self):
        self.plugins = dict()

        # collect plugins and call _register_plugin for each
        ...

    def _register_plugin(self, name: str, plugin: types.ModuleType):
        self._validate_plugin(name, plugin)
        self.plugins[name] = Plugin(
            name,
            plugin.Executor,
            common_settings=getattr(plugin, "common_settings", None),
            _executor_settings_cls=getattr(plugin, "ExecutorSettings", None),
        )

    def _validate_plugin(self, name: str, module: types.ModuleType):

        expected_attributes = {
           "common_settings": Optional[CommonSettings],
           "ExecutorSettings": Optional[type[ExecutorSettingsBase]],
           "Executor": type[self.executor_base_cls],
        }

        for attr, attr_type in expected_attributes.items():
            # check if attr is missing and fail if it is not optional
            is_optional = type(attr_type) == typing._UnionGenericAlias
            if not hasattr(module, attr):
                if is_optional:
                    continue
                else:
                    raise InvalidPluginException(
                        name, f"plugin does not define {attr}."
                    )
            if is_optional:
                # get inner type
                attr_type, = attr_type.__args__
            attr_value = getattr(module, attr)
            if type(attr_type) == types.GenericAlias:
                # check for class type
                cls, = attr_type.__args__
                if not issubclass(attr_value, cls):
                    raise InvalidPluginException(name, f"{attr} must be a subclass of {cls.__module__}.{cls.__name__}.")
            else:
                # check for instance type
                if not isinstance(attr_value, attr_type):
                    raise InvalidPluginException(
                        name, f"{attr} must be of type {attr_type}."
                    )