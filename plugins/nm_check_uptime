#!/usr/bin/env python2
#####################################################################

from nelmon import constants as C
from nelmon.common import nelmon_exit
from nelmon.globals import NelmonGlobals
from nelmon.snmp_oids import general_oids as O
from nelmon.snmp import NelmonSnmp, SnmpArguments

NelmonGlobals(PLUGIN_VERSION='1.0')

description = """This plugin queries a network device by SNMP to check how long
it has been up without reloading.

"""

# For more information about this plugin visit:
# http://networklore.com/nelmon/

def main():
    argparser = SnmpArguments(description)
    args = argparser.parser.parse_nelmon_args()
    snmp = NelmonSnmp(args)
    uptime = snmp.get_value(O.sysUpTime + '.0')
    nelmon_exit(C.OK, uptime)

if __name__ == "__main__":
    main()
