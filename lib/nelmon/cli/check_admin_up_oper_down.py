"""Plugin: Check Admin Up Oper Down."""
from nelmon import constants as C
from nelmon.common import nelmon_exit
from nelmon.globals import NelmonGlobals
from nelmon.snmp.oids import cisco_oids as O
from nelmon.snmp.args import SnmpArguments
from nelmon.snmp.handler import NelmonSnmp

NelmonGlobals(PLUGIN_VERSION='1.2')

description = """This plugin queries a network device by SNMP to check if there are
any interfaces which are in the admin up (no shutdown) but are operationally
down. It returns a warning or critical state depending on if you use -w or -c

"""
# For more information about this plugin visit:
# https://networklore.com/check-admin-up-oper-down


def main():
    """Plugin: check_admin_up_oper_down."""
    argparser = SnmpArguments(description)
    argparser.parser.add_argument('-w', action='store_true',
                                  help='Return Warning if interfaces are down')
    argparser.parser.add_argument('-c', action='store_true',
                                  help='Return Critical if interfaces are down')

    args = argparser.parser.parse_nelmon_args()

    if args.c:
        exit_status = C.CRITICAL
    elif args.w:
        exit_status = C.WARNING
    else:
        nelmon_exit(C.UNKNOWN, 'Use -w or -c')

    snmp = NelmonSnmp(args)

    oidlist = []
    oidlist.append(O.ifAdminStatus)
    oidlist.append(O.ifOperStatus)

    var_table = snmp.getnext(*oidlist)

    admin_up = []
    oper_down = []

    for var_binds in var_table:

        for oid, value in var_binds:
            if O.ifAdminStatus in oid and value == 1:
                ifIndex = int(oid.rsplit('.', 1)[-1])
                admin_up.append(ifIndex)
            if O.ifOperStatus in oid and value == 2:
                ifIndex = int(oid.rsplit('.', 1)[-1])
                oper_down.append(ifIndex)

    down_interfaces = list(set(admin_up) & set(oper_down))
    if len(down_interfaces) == 0:
        nelmon_exit(C.OK, 'No interfaces down')

    oidlist = []
    interface_descr = {}
    interface_alias = {}
    for ifIndex in down_interfaces:
        oidlist.append(O.ifDescr + "." + str(ifIndex))
        oidlist.append(O.ifAlias + "." + str(ifIndex))
    var_binds = snmp.get(*oidlist)
    for oid, value in var_binds:
        if O.ifDescr in oid:
            ifIndex = int(oid.rsplit('.', 1)[-1])
            interface_descr[ifIndex] = value
        if O.ifAlias in oid:
            ifIndex = int(oid.rsplit('.', 1)[-1])
            interface_alias[ifIndex] = value
    return_string = []

    if len(down_interfaces) > 1:
        return_string.append("%d interfaces down" % (len(down_interfaces)))

    for ifIndex in down_interfaces:
        if len(str(interface_alias[ifIndex])) > 0:
            return_string.append(str(interface_descr[ifIndex]) + " - " + str(interface_alias[ifIndex]))
        else:
            return_string.append(str(interface_descr[ifIndex]))

    nelmon_exit(exit_status, return_string)

if __name__ == "__main__":
    main()
