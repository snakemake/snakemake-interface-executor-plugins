__author__ = "Johannes Köster"
__copyright__ = "Copyright 2023, Johannes Köster, Vanessa Sochat"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"


from snakemake_interface_common.exceptions import ApiError


class InvalidPluginException(ApiError):
    def __init__(self, plugin_name: str, message: str):
        super().__init__(
            f"Snakemake executor plugin {plugin_name} is invalid: {message}"
        )
