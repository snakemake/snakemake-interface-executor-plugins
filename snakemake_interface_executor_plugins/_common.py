__author__ = "Johannes Köster"
__copyright__ = "Copyright 2022, Johannes Köster, Vanessa Sochat"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from dataclasses import MISSING, Field
from typing import Any, Dict, List, Literal, Tuple, Union, get_args, get_origin
from argparse_dataclass import _handle_bool_type


executor_plugin_prefix = "snakemake-executor-plugin-"
executor_plugin_module_prefix = executor_plugin_prefix.replace("-", "_")


# In Python 3.10, we can use types.NoneType
NoneType = type(None)


# Taken from https://github.com/mivade/argparse_dataclass/pull/59/files.
# TODO remove once https://github.com/mivade/argparse_dataclass/pull/59/files is
# merged and released
def dataclass_field_to_argument_args(
    field: Field[Any],
) -> Tuple[List[str], Dict[str, Any]]:
    """Extract kwargs of ArgumentParser.add_argument from a dataclass field.

    Returns pair of (args, kwargs) to be passed to ArgumentParser.add_argument.
    """
    args = field.metadata.get("args", [f"--{field.name.replace('_', '-')}"])
    positional = not args[0].startswith("-")
    kwargs = {
        "type": field.metadata.get("type", field.type),
        "help": field.metadata.get("help", None),
    }

    if field.metadata.get("args") and not positional:
        # We want to ensure that we store the argument based on the
        # name of the field and not whatever flag name was provided
        kwargs["dest"] = field.name

    if field.metadata.get("choices") is not None:
        kwargs["choices"] = field.metadata["choices"]

    # Support Literal types as an alternative means of specifying choices.
    if get_origin(field.type) is Literal:
        # Prohibit a potential collision with the choices field
        if field.metadata.get("choices") is not None:
            raise ValueError(
                f"Cannot infer type of items in field: {field.name}. "
                "Literal type arguments should not be combined with choices in the "
                "metadata. "
                "Remove the redundant choices field from the metadata."
            )

        # Get the types of the arguments of the Literal
        types = [type(arg) for arg in get_args(field.type)]

        # Make sure just a single type has been used
        if len(set(types)) > 1:
            raise ValueError(
                f"Cannot infer type of items in field: {field.name}. "
                "Literal type arguments should contain choices of a single type. "
                f"Instead, {len(set(types))} types where found: "
                + ", ".join([type_.__name__ for type_ in set(types)])
                + "."
            )

        # Overwrite the type kwarg
        kwargs["type"] = types[0]
        # Use the literal arguments as choices
        kwargs["choices"] = get_args(field.type)

    if field.metadata.get("metavar") is not None:
        kwargs["metavar"] = field.metadata["metavar"]

    if field.metadata.get("nargs") is not None:
        kwargs["nargs"] = field.metadata["nargs"]
        if field.metadata.get("type") is None:
            # When nargs is specified, field.type should be a list,
            # or something equivalent, like typing.List.
            # Using it would most likely result in an error, so if the user
            # did not specify the type of the elements within the list, we
            # try to infer it:
            try:
                kwargs["type"] = get_args(field.type)[0]  # get_args returns a tuple
            except IndexError:
                # get_args returned an empty tuple, type cannot be inferred
                raise ValueError(
                    f"Cannot infer type of items in field: {field.name}. "
                    "Try using a parameterized type hint, or "
                    "specifying the type explicitly using metadata['type']"
                )

    if field.default == field.default_factory == MISSING and not positional:
        kwargs["required"] = True
    else:
        kwargs["default"] = MISSING

    if field.type is bool:
        _handle_bool_type(field, args, kwargs)
    elif get_origin(field.type) is Union:
        if field.metadata.get("type") is None:
            # Optional[X] is equivalent to Union[X, None].
            f_args = get_args(field.type)
            if len(f_args) == 2 and NoneType in f_args:
                arg = next(a for a in f_args if a is not NoneType)
                kwargs["type"] = arg
            else:
                raise TypeError(
                    "For Union types other than 'Optional', a custom 'type' must be "
                    "specified using "
                    "'metadata'."
                )

    return args, kwargs
