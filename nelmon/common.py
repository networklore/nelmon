import sys

from nelmon import constants as C

import argparse


#####################################################################
# CLASSES
#####################################################################

class HelpText(object):

    def __init__(self, description, epilog):
        desc_prefix = "#" * 75
        desc_prefix += "\n"
        desc_suffix = "#" * 75
        self.description = desc_prefix + description + desc_suffix
        epilog_suffix = "#" * 75
        epilog_suffix += "\n"
        epilog_suffix += "This plugin is part of Nelmon, for more information visit:\n"
        epilog_suffix += "http://networklore.com/nelmon\n"
        epilog_suffix += "\n"
        self.epilog = epilog_suffix + epilog

class NlArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        self.exit(2, 'UNKNOWN: %s: error: %s\n' % (self.prog, message))



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

def verify_nelmon_features(minimum_version, current_version):

    if current_version < minimum_version:
        nelmon_exit(C.UNKNOWN, 'Requires Nelmon v.%s, download at http://networklore.com/nelmon/' % (minimum_version))
