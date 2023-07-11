import textwrap


class InvalidPluginException(Exception):
    def __init__(self, plugin_name: str, message: str):
        super().__init__(
            f"Snakemake executor plugin {plugin_name} is invalid: {message}"
        )


class WorkflowError(Exception):
    @staticmethod
    def format_arg(arg):
        if isinstance(arg, str):
            return arg
        elif isinstance(arg, WorkflowError):
            spec = ""
            if arg.rule is not None:
                spec += f"rule {arg.rule}"
            if arg.snakefile is not None:
                if spec:
                    spec += ", "
                spec += f"line {arg.lineno}, {arg.snakefile}"

            if spec:
                spec = f" ({spec})"

            return "{}{}:\n{}".format(
                arg.__class__.__name__, spec, textwrap.indent(str(arg), "    ")
            )
        else:
            return f"{arg.__class__.__name__}: {arg}"

    def __init__(self, *args, lineno=None, snakefile=None, rule=None):
        super().__init__("\n".join(self.format_arg(arg) for arg in args))
        if rule is not None:
            self.lineno = rule.lineno
            self.snakefile = rule.snakefile
        else:
            self.lineno = lineno
            self.snakefile = snakefile
        self.rule = rule