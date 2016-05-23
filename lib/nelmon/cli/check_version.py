"""Plugin: Check Version."""

import os
import yaml
from nelmon import constants as C
from nelmon.common import nelmon_exit
from nelmon.globals import NelmonGlobals
from nelmon.snmp.args import SnmpArguments
from nelmon.snmp.handler import NelmonSnmp
from nelsnmp.hostinfo.device import HostInfo

NelmonGlobals(PLUGIN_VERSION='1.1')

description = """This plugin queries a network device by SNMP to check which
version is running on the device. It uses the HostInfo feature from Nelsnmp.
To see a list of currently supported devices visit:
https://networklore.com/nelsnmp-hostinfo/

The plugin can run in reporting mode to just retreive the device versions,
or it can compare the current versions against your policy by specifying a
directory (-d) of yaml files, one for each device class.
For more information visit:
https://networklore.com/nm-check-version/
"""

# For more information about this plugin visit:
# https://networklore.com/nelmon/


def main():
    """Plugin: check_version."""
    argparser = SnmpArguments(description)
    argparser.parser.add_argument(
        '-d',
        help="Directory containing yaml version files")
    args = argparser.parser.parse_nelmon_args()
    snmp = NelmonSnmp(args)
    hostinfo = HostInfo(snmp)
    hostinfo.get_version()

    if hostinfo.version == 'UNKNOWN':
        exit_str = ['Unable to determine device version']
        exit_str.append('Vendor: %s' % hostinfo.vendor)
        exit_str.append('OS: %s' % hostinfo.os)
        exit_str.append('Version: %s' % hostinfo.version)
        exit_str.append('*******************************')
        exit_str.append("Your version of Nelsnmp does't support this device")
        exit_str.append('please check:')
        exit_str.append('http://networklore.com/nelsnmp-hostinfo/')
        nelmon_exit(C.UNKNOWN, exit_str)

    if args.d:
        yaml_file = '%s/%s_%s.yml' % (args.d, hostinfo.vendor, hostinfo.os)
    else:
        nelmon_exit(C.OK, hostinfo.version)

    if not os.path.isfile(yaml_file):
        nelmon_exit(C.UNKNOWN, 'Unable to find file: %s' % yaml_file)

    data = None
    with open(yaml_file, 'r') as f:
        data = yaml.load(f.read())

    if data is None:
        nelmon_exit(C.UNKNOWN, 'Unable to parse %s' % yaml_file)

    declared_versions = []
    for policy in data:
        if data[policy] is not None:
            for version in data[policy]:
                declared_versions.append(version)
                if hostinfo.version == version:
                    match_policy = policy

    hits = declared_versions.count(hostinfo.version)
    if hits == 0:
        nelmon_exit(
            C.UNKNOWN, '%s not declared in %s' % (hostinfo.version, yaml_file))
    elif hits > 1:
        nelmon_exit(
            C.UNKNOWN,
            '%s is declared  %s times in %s' % (hostinfo.version,
                                                hits, yaml_file))
    else:
        if match_policy == 'approved':
            if data[match_policy][hostinfo.version]:
                nelmon_exit(
                    C.OK,
                    '%s - %s' % (hostinfo.version,
                                 data[match_policy][hostinfo.version])
                )
            else:
                nelmon_exit(C.OK, hostinfo.version)
        elif match_policy == 'critical':
            if data[match_policy][hostinfo.version]:
                nelmon_exit(
                    C.CRITICAL,
                    '%s - %s (critical)' % (
                        hostinfo.version,
                        data[match_policy][hostinfo.version])
                )
            else:
                nelmon_exit(C.CRITICAL, '%s - (critical)' % hostinfo.version)
        elif match_policy == 'vulnerable':
            if data[match_policy][hostinfo.version]:
                nelmon_exit(
                    C.WARNING,
                    '%s - %s (vulnerable)' % (
                        hostinfo.version,
                        data[match_policy][hostinfo.version])
                )
            else:
                nelmon_exit(C.WARNING, '%s - (warning)' % hostinfo.version)
        elif match_policy == 'obsolete':
            if data[match_policy][hostinfo.version]:
                nelmon_exit(
                    C.WARNING,
                    '%s - %s (obsolete)' % (
                        hostinfo.version,
                        data[match_policy][hostinfo.version])
                )
            else:
                nelmon_exit(C.WARNING, '%s - (obsolete)' % hostinfo.version)
        else:
            nelmon_exit(C.UNKNOWN,
                        '%s is under unknown policy: %s' % (
                            hostinfo.version, match_policy))

    nelmon_exit(C.OK, hostinfo.version)


if __name__ == "__main__":
    main()
