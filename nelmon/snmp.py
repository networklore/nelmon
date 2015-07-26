#####################################################################
#
#
#####################################################################

import nelmon.common
from nelmon.common import NelmonArguments, nelmon_exit
from nelmon import constants as C
from nelsnmp.snmp import cmdgen, SnmpHandler

#####################################################################
# CLASSES
#####################################################################

class SnmpArguments(NelmonArguments):

    def __init__(self, description, epilog = ''):

        super(SnmpArguments, self).__init__(description, epilog)

    def _add_local_args(self):
        self.parser.add_argument('-H', help="Target host")
        self.parser.add_argument(
            '-p', help="Port number (default: 161)", default=161)
        self.parser.add_argument(
            '-P', help="SNMP protocol version", choices=['2c', '3'])
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


class NelmonSnmp(SnmpHandler):

    def __init__(self, args):
        self._verify_snmp_arguments(args)
        self._set_snmp_parameters(args)

    def _raise_error(self, ErrorType, error_data):
        nelmon_exit(C.CRITICAL, error_data)

    def _set_snmp_parameters(self, args):
        # Change to SNMP community auth
        self.version = args.P
        if args.P == "2c":
            self.snmp_auth = cmdgen.CommunityData(args.C)

        elif args.P == "3":
            self.username = args.U
            if args.a == "SHA":
                self.integrity = cmdgen.usmHMACSHAAuthProtocol
            elif args.a == "MD5":
                self.integrity = cmdgen.usmHMACMD5AuthProtocol

            if args.x == "AES":
                self.privacy = cmdgen.usmAesCfb128Protocol
            elif args.x == "DES":
                self.privacy = cmdgen.usmDESPrivProtocol

            self.authkey = args.A

            if args.L == "authPriv":
                self.privkey = args.X

        self.host = args.H
        self.port = int(args.p)

    def _verify_snmp_arguments(self, args):
        if args.H is None:
            nelmon_exit(C.UNKNOWN, '-H argument missing')
        if args.P is None:
            nelmon_exit(C.UNKNOWN, '-P argument missing')
        if args.P == "2c" and args.C is None:
            nelmon_exit(C.UNKNOWN, 'Specify community when using SNMP 2c')
        if args.P == "3" and args.U is None:
            nelmon_exit(C.UNKNOWN, 'Specify username when using SNMP 3')
        if args.P == "3" and args.L is None:
            nelmon_exit(C.UNKNOWN, 'Specify security level when using SNMP 3')
        if args.L == "authNoPriv" and args.a is None:
            nelmon_exit(C.UNKNOWN,
                'Specify authentication protocol when using authNoPriv')
        if args.L == "authNoPriv" and args.A is None:
            nelmon_exit(C.UNKNOWN,
                'Specify authentication password when using authNoPriv')
        if args.L == "authPriv" and args.a is None:
            nelmon_exit(C.UNKNOWN,
                'Specify authentication protocol when using authPriv')
        if args.L == "authPriv" and args.A is None:
            nelmon_exit(C.UNKNOWN,
                'Specify authentication password when using authPriv')
        if args.L == "authPriv" and args.x is None:
            nelmon_exit(C.UNKNOWN, 'Specify privacy protocol when using authPriv')
        if args.L == "authPriv" and args.X is None:
            nelmon_exit(C.UNKNOWN, 'Specify privacy password when using authPriv')
