from argparse_dataclass import _add_dataclass_options, fields
from dataclasses import dataclass
import types
from typing import Optional
import typing
import pkgutil
import importlib
import copy

from snakemake_executor_plugin_interface.exceptions import InvalidPluginException
import snakemake_executor_plugin_interface._common as common


@dataclass
class CommonSettings:
    """Common Snakemake settings shared between executors that can be specified by executor plugins.

    The plugin has to specify an instance of this class as the value of the common_settings attribute.
    """

    non_local_exec: bool
    use_threads: bool = False


@dataclass
class ExecutorSettingsBase:
    """Base class for executor settings.

    Executor plugins can define a subclass of this class, named 'ExecutorSettings'.
    """

    pass


# Valid Argument types (to distinguish from empty dataclasses)
ArgTypes = (str, int, float, bool)


@dataclass
class Plugin:
    name: str

    # This is the executor base class
    executor: object
    common_settings: CommonSettings
    _executor_settings_cls: Optional[type[ExecutorSettingsBase]]

    @property
    def prefix(self):
        return self.name.replace(common.executor_plugin_module_prefix, "")

    def register_cli_args(self, argparser):
        """Add arguments derived from self.executor_settings to given argparser."""

        # Cut out early if we don't have custom parameters to add
        if not self.has_executor_settings():
            return

        # Convenience handle
        params = self._executor_settings_cls

        # Assemble a new dataclass with the same fields, but with prefix
        # fields are stored at dc.__dataclass_fields__
        dc = copy.deepcopy(params)
        for field in fields(params):
            # Executor plugin dataclass members get prefixed with their
            # name when passed into snakemake args.
            prefixed_name = f"{self.prefix}_{field.name}"

            # Since we use the helper function below, we
            # need a new dataclass that has these prefixes
            del dc.__dataclass_fields__[field.name]
            field.name = prefixed_name
            dc.__dataclass_fields__[field.name] = field

        # When we get here, we have a namespaced dataclass.
        # If there is overlap in snakemake args, it should error
        _add_dataclass_options(dc, argparser)

    def has_executor_settings(self):
        """Determine if a plugin defines custom executor settings"""
        return self._executor_settings_cls is not None and not isinstance(
            self._executor_settings_cls, ExecutorSettingsBase
        )

    def get_executor_settings(self, args) -> Optional[ExecutorSettingsBase]:
        """Return an instance of self.executor_settings with values from args.

        This helper function will select executor plugin namespaces arguments
        for a dataclass. It allows us to pass them from the custom executor ->
        custom argument parser -> back into dataclass -> snakemake.
        """
        if not self.has_executor_settings():
            return ExecutorSettingsBase()

        # We will parse the args from snakemake back into the dataclass
        dc = self._executor_settings_cls

        # Iterate through the args, and parse those in the namespace
        kwargs = {}

        # These fields will have the executor prefix
        for field in fields(dc):
            # This is the actual field name without the prefix
            name = field.name.replace(f"{self.name}_", "", 1)
            value = getattr(args, field.name, None)

            # This will only add instantiated values, and
            # skip over dataclasses._MISSING_TYPE and similar
            if isinstance(value, ArgTypes):
                kwargs[name] = value

        # At this point we want to convert back to the original dataclass
        return dc(**kwargs)


class ExecutorPluginRegistry:
    """This class is a singleton that holds all registered executor plugins."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        from snakemake.executors import AbstractExecutor
        if hasattr(self, "executor_base_cls"):
            # init has been called before
            return
        self.executor_base_cls = AbstractExecutor
        self._collect_plugins()

    def register_cli_args(self, argparser):
        """Add arguments derived from self.executor_settings to given argparser."""
        for _, plugin in self.plugins.items():
            plugin.register_cli_args(argparser)

    def _collect_plugins(self):
        """Collect plugins and call _register_plugin for each."""
        self.plugins = dict()

        # Executor plugins are externally installed plugins named "snakemake_executor_<name>"
        # They should follow the same convention if on pip, snakemake-executor-<name>
        # Note that these will not be detected installed in editable mode (pip install -e .)
        for _, name, _ in pkgutil.iter_modules():
            if (
                not name.startswith(common.executor_plugin_module_prefix)
                or name == "snakemake_executor_plugin_interface"
            ):
                continue
            module = importlib.import_module(name)
            self._register_plugin(name, module)

    def _register_plugin(self, name: str, plugin: types.ModuleType):
        """Validate and register a plugin"""
        self._validate_plugin(name, plugin)

        # Derive the shortened name for future access
        plugin_name = name.replace(common.executor_plugin_module_prefix, "")

        self.plugins[plugin_name] = Plugin(
            plugin_name,
            plugin.Executor,
            common_settings=getattr(plugin, "common_settings", None),
            _executor_settings_cls=getattr(plugin, "ExecutorSettings", None),
        )

    def _validate_plugin(self, name: str, module: types.ModuleType):
        """Validate a plugin for attributes and naming"""
        expected_attributes = {
            "common_settings": CommonSettings,
            "ExecutorSettings": Optional[type[ExecutorSettingsBase]],
            "Executor": type[self.executor_base_cls],
        }
        for attr, attr_type in expected_attributes.items():
            # check if attr is missing and fail if it is not optional
            is_optional = type(attr_type) == typing._UnionGenericAlias
            if not hasattr(module, attr):
                if is_optional:
                    continue
                raise InvalidPluginException(name, f"plugin does not define {attr}.")

            if is_optional:
                # get inner type
                attr_type, _ = attr_type.__args__
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
