"""nelmon.args.base."""

import argparse
from argparse import RawTextHelpFormatter
import sys
from nelmon import constants as C
from nelmon.globals import NelmonGlobals
from nelmon.common import nelmon_exit


class HelpText(object):
    def __init__(self, description, epilog):
        desc_prefix = "#" * 75
        desc_prefix += "\n"
        desc_suffix = "#" * 75
        plugin = C.CURRENT_PLUGIN + ' v' + NelmonGlobals.PLUGIN_VERSION + '\n'
        self.description = desc_prefix + description + plugin + desc_suffix
        epilog_suffix = "#" * 75
        epilog_suffix += "\n"
        epilog_suffix += "This plugin is part of Nelmon, for more information visit:\n"
        epilog_suffix += "https://networklore.com/nelmon\n"
        epilog_suffix += "\n"
        self.epilog = epilog_suffix + epilog


class NelmonArguments(object):

    def __init__(self, description, epilog=''):
        helptext = HelpText(description, epilog)
        self.parser = NlArgumentParser(
            description=helptext.description,
            epilog=helptext.epilog,
            formatter_class=RawTextHelpFormatter)

        self.parser.add_argument('-V', help='Show version', action='store_true')

        self.parser.add_argument(
            '-O',
            help='Output format',
            choices=['standard', 'with_status'],
            default='standard'
        )

        self._add_local_args()

    def _add_local_args(self):
        pass


class NlArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        nelmon_exit(C.UNKNOWN, '%s: error: %s\n' % (self.prog, message))

    def parse_nelmon_args(self):
        sys_args = sys.argv[1:]
        choose_output = False
        for sys_arg in sys_args:
            if choose_output:
                if sys_arg == 'with_status':
                    NelmonGlobals(OUTPUT_FORMAT='with_status')
                choose_output = False
            if sys_arg == '-O':
                choose_output = True
        if '-V' in sys_args:
            output = '%s - v%s (Nelmon - v%s)' % (
                C.CURRENT_PLUGIN, NelmonGlobals.PLUGIN_VERSION, C.NELMON_VERSION)
            nelmon_exit(C.OK, output)
        args = self.parse_args()

        return args
