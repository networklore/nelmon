import sys

try:
    import argparse
except:
    print "argparse module is missing"
    sys.exit()

#####################################################################
# CLASSES
#####################################################################

class ExitStatus(object):

    def __init__(self):
        self.OK = 0
        self.WARNING = 1
        self.CRITICAL = 2
        self.UNKNOWN = 3

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

def exit_with_error(message):
    current_plugin = sys.argv[0]
    print ('UNKNOWN: %s: - %s' % (current_plugin, message))
    sys.exit(2)

def exit_with_unknown(message):
    current_plugin = sys.argv[0]
    print ('UNKNOWN: %s: - %s' % (current_plugin, message))
    sys.exit(3)

def exit_string(message, exit_code):
    print message
    sys.exit(exit_code)

def exit_list(messages, exit_code):
    for message in messages:
        print message
    sys.exit(exit_code)

def verify_nelmon_features(minimum_version, current_version):
    
    if current_version < minimum_version:
        exit_with_error('Requires Nelmon v.%s, download at http://networklore.com/nelmon/' % (minimum_version))

