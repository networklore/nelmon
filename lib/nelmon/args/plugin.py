"""nelmon.args.plugin."""

from nelmon.args.base import NelmonArguments


class PluginArguments(NelmonArguments):
    """Base class for Plugins."""

    def __init__(self, description, epilog=''):

        super(PluginArguments, self).__init__(description, epilog)

        # def _add_local_args(self):
        self.parser.add_argument('-H', help='Target host', required=True)
