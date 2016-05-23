"""nelmon.snmp.oids."""
from nelsnmp.oids import GeneralOids
from nelsnmp.vendors.cisco.oids import CiscoOids
from nelsnmp.vendors.synology.oids import SynologyOids

cisco_oids = CiscoOids()
general_oids = GeneralOids()
synology_oids = SynologyOids()
