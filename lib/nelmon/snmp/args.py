"""nelmon.snmp.args."""

from nelmon.args.plugin import PluginArguments


class SnmpArguments(PluginArguments):

    def __init__(self, description, epilog=''):

        super(SnmpArguments, self).__init__(description, epilog)

    def _add_local_args(self):
        self.parser.add_argument(
            '-p', help="Port number (default: 161)", default=161)
        self.parser.add_argument(
            '-P', help="SNMP protocol version", choices=['2c', '3'], required=True)
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
