import sys

from nelmon import constants as C
from nelmon.globals import NelmonGlobals

import argparse
from argparse import RawTextHelpFormatter

#####################################################################
# CLASSES
#####################################################################

class HelpText(object):

    def __init__(self, description, epilog):
        desc_prefix = "#" * 75
        desc_prefix += "\n"
        desc_suffix = "#" * 75
        plugin = C.CURRENT_PLUGIN + ' v' ' ' + NelmonGlobals.PLUGIN_VERSION + '\n'
        self.description = desc_prefix + description + plugin + desc_suffix
        epilog_suffix = "#" * 75
        epilog_suffix += "\n"
        epilog_suffix += "This plugin is part of Nelmon, for more information visit:\n"
        epilog_suffix += "http://networklore.com/nelmon\n"
        epilog_suffix += "\n"
        self.epilog = epilog_suffix + epilog

class NelmonArguments(object):

    def __init__(self, description, epilog = ''):
        helptext = HelpText(description, epilog)
        self.parser = NlArgumentParser(
            description=helptext.description,
            epilog=helptext.epilog,
            formatter_class=RawTextHelpFormatter)

        self.parser.add_argument('-V', help='Show version', action='store_true')


        self._add_local_args()

    def _add_local_args(self):
        pass

class NlArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        self.exit(2, 'UNKNOWN: %s: error: %s\n' % (self.prog, message))

    def parse_nelmon_args(self):
        args = self.parse_args()
        if args.V:
            output = '%s - v%s (Nelmon - v%s)' % (C.CURRENT_PLUGIN, NelmonGlobals.PLUGIN_VERSION, C.NELMON_VERSION)
            nelmon_exit(C.OK, output)
        return args


#####################################################################
# FUNCTIONS
#####################################################################

def nelmon_exit(exit_code, output_message):
    if isinstance(output_message, basestring):
        print output_message
    else:
        for message in output_message:
            print message
    sys.exit(exit_code)

def verify_nelmon_features():

    if C.NELMON_VERSION < NelmonGlobals.MIN_NELMON_VER:
        nelmon_exit(C.UNKNOWN, 'Requires Nelmon v.%s, download at http://networklore.com/nelmon/' % (MIN_NELMON_VER))
