__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster, Vanessa Sochat"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from argparse_dataclass import _add_dataclass_options, fields
from dataclasses import dataclass
from typing import Optional
import copy
from snakemake_executor_plugin_interface import CommonSettings, ExecutorSettingsBase

import snakemake_executor_plugin_interface._common as common

# Valid Argument types (to distinguish from empty dataclasses)
ArgTypes = (str, int, float, bool, list)


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
