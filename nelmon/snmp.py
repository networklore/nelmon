#####################################################################
#
#
#####################################################################

import sys
import nelmon.common
from argparse import RawTextHelpFormatter
from pysnmp.entity.rfc3413.oneliner import cmdgen


#####################################################################
# CLASSES
#####################################################################




class SnmpArguments(object):

    def __init__(self, description, epilog = ""):
        helptext = nelmon.common.HelpText(description, epilog)
        self.parser = nelmon.common.NlArgumentParser(
            description=helptext.description,
            epilog=helptext.epilog,
            formatter_class=RawTextHelpFormatter)
        self.parser.add_argument('-H', help="Target host", required=True)
        self.parser.add_argument('-V', help="Show version")
        self.parser.add_argument(
            '-p', help="Port number (default: 161)", default=161)
        self.parser.add_argument(
            '-P', help="SNMP protocol version", choices=['2c', '3'],
            required=True)
        self.parser.add_argument('-C', help="SNMP Community string")
        self.parser.add_argument(
            '-L', help="SNMPv3 Security level",
            choices=['authNoPriv', 'authPriv'])
        self.parser.add_argument(
            '-a', help="SNMPv3 authentiction protocol",
            choices=['MD5', 'SHA'])
        self.parser.add_argument(
            '-x', help="SNMPv3 privacy protocol",
            choices=['DES', 'AES'])
        self.parser.add_argument('-U', help="SNMPv3 username")
        self.parser.add_argument('-A', help="SNMPv3 authentication password")
        self.parser.add_argument('-X', help="SNMPv3 privacy password")


class SnmpHandler(object):

    def __init__(self, args):
        self.verify_snmp_arguments(args)
        self.set_snmp_parameters(args)

    def set_snmp_parameters(self, args):
        # Change to SNMP community auth
        if args.P == "2c":
            self.snmp_auth = cmdgen.CommunityData(args.C)
        elif args.P == "3":
            if args.a == "SHA":
                integrity_proto = cmdgen.usmHMACSHAAuthProtocol
            elif args.a == "MD5":
                integrity_proto = cmdgen.usmHMACMD5AuthProtocol

            if args.x == "AES":
                privacy_proto = cmdgen.usmAesCfb128Protocol
            elif args.x == "DES":
                privacy_proto = cmdgen.usmDESPrivProtocol

            if args.L == "authNoPriv":
                self.snmp_auth = cmdgen.UsmUserData(
                    args.U, authKey=args.A,
                    authProtocol=integrity_proto)
            elif args.L == "authPriv":
                self.snmp_auth = cmdgen.UsmUserData(
                    args.U, authKey=args.A,
                    privKey=args.X,
                    authProtocol=integrity_proto,
                    privProtocol=privacy_proto)

        self.host = args.H
        self.port = int(args.p)

    def snmp_get(self, oid):
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            self.snmp_auth,
            cmdgen.UdpTransportTarget((self.host, self.port)),
            cmdgen.MibVariable(oid,)
        )

        if errorIndication:
            nelmon.common.exit_with_error(errorIndication)

        if errorStatus:
            nelmon.common.exit_with_error(errorStatus)

        return varBinds

    def snmp_get_list(self, oidlist):

        snmpquery = []
        for oid in oidlist:
            snmpquery.append(cmdgen.MibVariable(oid,), )
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            self.snmp_auth,
            cmdgen.UdpTransportTarget((self.host, self.port)),
            *snmpquery
        )

        if errorIndication:
            nelmon.common.exit_with_error(errorIndication)

        if errorStatus:
            nelmon.common.exit_with_error(errorStatus)

        return varBinds


    def snmp_getnext_list(self, oidlist):

        snmpquery = []
        for oid in oidlist:
            snmpquery.append(cmdgen.MibVariable(oid,), )
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varTable = cmdGen.nextCmd(
            self.snmp_auth,
            cmdgen.UdpTransportTarget((self.host, self.port)),
            *snmpquery
        )

        if errorIndication:
            nelmon.common.exit_with_error(errorIndication)

        if errorStatus:
            nelmon.common.exit_with_error(errorStatus)

        return varTable




    def verify_snmp_arguments(self, args):
        if args.P == "2c" and args.C is None:
            exit_with_error('Specify community when using SNMP 2c')
        if args.P == "3" and args.U is None:
            exit_with_error('Specify username when using SNMP 3')
        if args.P == "3" and args.L is None:
            exit_with_error('Specify security level when using SNMP 3')
        if args.L == "authNoPriv" and args.a is None:
            exit_with_error(
                'Specify authentication protocol when using authNoPriv')
        if args.L == "authNoPriv" and args.A is None:
            exit_with_error(
                'Specify authentication password when using authNoPriv')
        if args.L == "authPriv" and args.a is None:
            exit_with_error(
                'Specify authentication protocol when using authPriv')
        if args.L == "authPriv" and args.A is None:
            exit_with_error(
                'Specify authentication password when using authPriv')
        if args.L == "authPriv" and args.x is None:
            exit_with_error('Specify privacy protocol when using authPriv')
        if args.L == "authPriv" and args.X is None:
            exit_with_error('Specify privacy password when using authPriv')

