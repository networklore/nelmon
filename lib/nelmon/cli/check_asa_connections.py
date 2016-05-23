"""Plugin: Check ASA Connections."""

from nelmon import constants as C
from nelmon.common import nelmon_exit
from nelmon.globals import NelmonGlobals
from nelmon.snmp.oids import cisco_oids as O
from nelmon.snmp.args import SnmpArguments
from nelmon.snmp.handler import NelmonSnmp

NelmonGlobals(PLUGIN_VERSION='1.2')

description = """This plugin queries a Cisco ASA device by SNMP to check how many
current connections are established through the firewall.

"""

# For more information about this plugin visit:
# https://networklore.com/check-asa-connections/


def main():
    """Plugin: check_asa_connections."""
    argparser = SnmpArguments(description)
    argparser.parser.add_argument(
        '-w',
        help='Number of connections to report warning state',
        type=int)
    argparser.parser.add_argument(
        '-c',
        help='Number of connections to report critical state',
        type=int)

    args = argparser.parser.parse_nelmon_args()
    snmp = NelmonSnmp(args)

    current_connections = O.cfwConnectionStatValue + ".40.6"
    connections = snmp.get_value(current_connections)

    if not args.c or not args.w:
        nelmon_exit(C.UNKNOWN, 'Use -w or -c')

    if args.c <= connections:
        exit_code = C.CRITICAL
        exit_string = "%d connections" % connections
    elif args.w <= connections:
        exit_code = C.WARNING
        exit_string = "%d connections" % connections
    else:
        exit_code = C.OK
        exit_string = "%d connections" % connections

    if args.c and args.w:
        perf_data = 'connections=%s;%s;%s' % (connections, args.w, args.c)
    else:
        perf_data = 'connections=%s' % connections

    nelmon_exit(
        exit_code,
        exit_string,
        perf_data=perf_data)

if __name__ == "__main__":
    main()
