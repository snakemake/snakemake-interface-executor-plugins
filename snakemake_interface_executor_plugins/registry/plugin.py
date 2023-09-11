__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster, Vanessa Sochat"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from argparse_dataclass import field_to_argument_args, fields
from dataclasses import MISSING, Field, dataclass
from typing import Any, Optional, Type
import copy
from snakemake_interface_executor_plugins import CommonSettings, ExecutorSettingsBase
import snakemake_interface_executor_plugins._common as common
from snakemake_interface_common.exceptions import WorkflowError

from snakemake_interface_executor_plugins.exceptions import InvalidPluginException

# Valid Argument types (to distinguish from empty dataclasses)
ArgTypes = (str, int, float, bool, list)


@dataclass
class Plugin:
    name: str

    # This is the executor base class
    executor: object
    common_settings: CommonSettings
    _executor_settings_cls: Optional[Type[ExecutorSettingsBase]]

    @property
    def prefix(self):
        return self.name.replace(common.executor_plugin_module_prefix, "")

    def register_cli_args(self, argparser):
        """Add arguments derived from self.executor_settings to given
        argparser."""

        # Cut out early if we don't have custom parameters to add
        if not self.has_executor_settings():
            return

        # Convenience handle
        params = self._executor_settings_cls

        # Assemble a new dataclass with the same fields, but with prefix
        # fields are stored at dc.__dataclass_fields__
        dc = copy.deepcopy(params)
        for field in fields(params):
            if "help" not in field.metadata:
                raise InvalidPluginException(
                    "Fields of ExecutorSettings must have a help string."
                )
            if field.default is MISSING and field.default_factory is MISSING:
                raise InvalidPluginException(
                    "Fields of ExecutorSettings must have a default value."
                )

            # Executor plugin dataclass members get prefixed with their
            # name when passed into snakemake args.
            prefixed_name = self._get_prefixed_name(field)

            # Since we use the helper function below, we
            # need a new dataclass that has these prefixes
            del dc.__dataclass_fields__[field.name]
            field.name = prefixed_name
            dc.__dataclass_fields__[field.name] = field

        settings = argparser.add_argument_group(f"{self.name} executor settings")

        for field in fields(dc):
            args, kwargs = field_to_argument_args(field)

            if field.metadata.get("env_var"):
                kwargs["env_var"] = f"SNAKEMAKE_{prefixed_name.upper()}"
            settings.add_argument(*args, **kwargs)

    def has_executor_settings(self):
        """Determine if a plugin defines custom executor settings"""
        return self._executor_settings_cls is not None

    @property
    def executor_settings_class(self):
        return self._executor_settings_cls

    def get_executor_settings(self, args) -> ExecutorSettingsBase:
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

            if field.metadata.get("required") and value is None:
                cli_arg = self._get_cli_arg(field)
                raise WorkflowError(
                    f"Missing required argument {cli_arg} for executor {self.name}."
                )

            # This will only add instantiated values, and
            # skip over dataclasses._MISSING_TYPE and similar
            if isinstance(value, ArgTypes):
                kwargs[name] = value

        # At this point we want to convert back to the original dataclass
        return dc(**kwargs)

    def _get_cli_arg(self, field: Field[Any]):
        return self._get_prefixed_name(field).replace("_", "-")

    def _get_prefixed_name(self, field: Field[Any]):
        return f"{self.prefix}_{field.name}"
