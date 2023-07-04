class InvalidPluginException(Exception):
    def __init__(self, plugin_name: str, message: str):
        super().__init__(
            f"Snakemake executor plugin {plugin_name} is invalid: {message}"
        )
