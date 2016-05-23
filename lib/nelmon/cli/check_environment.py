"""Plugin: Check Environment."""

from nelmon import constants as C
from nelmon.common import nelmon_exit
from nelmon.globals import NelmonGlobals
from nelmon.snmp.oids import cisco_oids as O
from nelmon.snmp.args import SnmpArguments
from nelmon.snmp.handler import NelmonSnmp
from nelsnmp.hostinfo.device import HostInfo

NelmonGlobals(PLUGIN_VERSION='1.0')

description = """This plugin queries a Cisco device by SNMP and does an
environmental (check, power, fans, temperature).

"""

# For more information about this plugin visit:
# https://networklore.com/nelmon/

envmon_state = {
    1: 'normal',
    2: 'warning',
    3: 'critical',
    4: 'shutdown',
    5: 'notPresent',
    6: 'notFunctioning'
}

envmon_state_map = {
    1: C.OK,
    2: C.WARNING,
    3: C.CRITICAL,
    4: C.CRITICAL,
    5: C.UNKNOWN,
    6: C.CRITICAL
}


class Sensor(object):

    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.description = None
        self.state = None
        self.value = None

    def set_description(self, value):
        self.description = value

    def set_state(self, value):
        self.state = value

    def set_value(self, value):
        self.state = value


class SensorCollection(object):

    def __init__(self):
        self.status = C.OK
        self.sensors = 0
        self.normal_sensors = 0
        self.failed_sensors = 0
        self.normal_fans = 0
        self.failed_fans = 0
        self.normal_volt = 0
        self.failed_volt = 0
        self.normal_pw = 0
        self.failed_pw = 0
        self.normal_temp = 0
        self.failed_temp = 0
        self.errors = []
        self.normals = []
        self.output = []

    def _add_error(self, message):
        self.errors.append(message)

    def _add_normal(self, message):
        self.normals.append(message)

    def _state(self, state):
        if envmon_state_map[state] > self.status:
            self.status = status

    def add_sensor(self, sensor_type, description, state):
        self.sensors += 1
        self._state(state)
        message = '%s - %s' % (description, envmon_state[state])
        if state > 1:
            failed = True
            self.failed_sensors += 1
            self._add_error(message)
        else:
            failed = False
            self.normal_sensors += 1
            self._add_normal(message)
        if sensor_type == 'fan':
            if failed:
                self.failed_fans += 1
            else:
                self.normal_fans += 1
        elif sensor_type == 'temp':
            if failed:
                self.failed_temp += 1
            else:
                self.normal_temp += 1
        elif sensor_type == 'pw':
            if failed:
                self.failed_pw += 1
            else:
                self.normal_pw += 1
        elif sensor_type == 'volt':
            if failed:
                self.failed_volt += 1
            else:
                self.normal_volt += 1

        self._state(state)

    def set_message(self):
        if len(self.errors) == 1:
            self.output.append(self.errors[0])
        elif len(self.errors) > 1:
            message = '%s failed sensors' % self.failed_sensors
            if self.failed_fans > 0:
                message += ', %s fans' % self.failed_fans
            if self.failed_pw > 0:
                message += ', %s pw' % self.failed_pw
            if self.failed_volt > 0:
                message += ', %s volt' % self.failed_volt
            if self.failed_temp > 0:
                message += ', %s temp' % self.failed_temp
            self.output.append(message)
            for error in self.errors:
                self.output.append(error)
        elif len(self.errors) == 0 and self.normal_sensors > 0:
            message = '%s normal sensors' % self.normal_sensors
            if self.normal_fans > 0:
                message += ', %s fans' % self.normal_fans
            if self.normal_pw > 0:
                message += ', %s pw' % self.normal_pw
            if self.normal_volt > 0:
                message += ', %s volt' % self.normal_volt
            if self.normal_temp > 0:
                message += ', %s temp' % self.normal_temp
            self.output.append(message)

        for message in self.normals:
            self.output.append(message)

        if len(self.output) == 0:
            self.output = 'No environmental sensors found'


def main():
    """Plugin: check_environment."""
    argparser = SnmpArguments(description)

    args = argparser.parser.parse_nelmon_args()
    snmp = NelmonSnmp(args)

    hostinfo = HostInfo(snmp)
    hostinfo.get_vendor()

    if hostinfo.vendor != 'cisco':
        nelmon_exit(
            C.UNKNOWN, '%s v%s only works with Cisco devices' % (
                C.CURRENT_PLUGIN, NelmonGlobals.PLUGIN_VERSION))

    env_tables = snmp.getnext(O.ciscoEnvMonObjects)
    volt_sensors = {}
    temp_sensors = {}
    fan_sensors = {}
    pw_sensors = {}
    s = SensorCollection()
    for env_table in env_tables:
        for oid, value in env_table:
            if O.ciscoEnvMonVoltageStatusTable in oid:
                sensor_id = oid.rsplit('.', 1)[-1]
                if sensor_id not in volt_sensors.keys():
                    volt_sensors[sensor_id] = Sensor(sensor_id)
                if O.ciscoEnvMonVoltageStatusDescr in oid:
                    volt_sensors[sensor_id].set_description(value)
                if O.ciscoEnvMonVoltageStatusValue in oid:
                    volt_sensors[sensor_id].set_value(value)
                if O.ciscoEnvMonVoltageState in oid:
                    volt_sensors[sensor_id].set_state(value)
            if O.ciscoEnvMonTemperatureStatusTable in oid:
                sensor_id = oid.rsplit('.', 1)[-1]
                if sensor_id not in temp_sensors.keys():
                    temp_sensors[sensor_id] = Sensor(sensor_id)
                if O.ciscoEnvMonTemperatureStatusDescr in oid:
                    temp_sensors[sensor_id].set_description(value)
                if O.ciscoEnvMonTemperatureStatusValue in oid:
                    temp_sensors[sensor_id].set_value(value)
                if O.ciscoEnvMonTemperatureState in oid:
                    temp_sensors[sensor_id].set_state(value)
            if O.ciscoEnvMonFanStatusTable in oid:
                sensor_id = oid.rsplit('.', 1)[-1]
                if sensor_id not in fan_sensors.keys():
                    fan_sensors[sensor_id] = Sensor(sensor_id)
                if O.ciscoEnvMonFanStatusDescr in oid:
                    fan_sensors[sensor_id].set_description(value)
                if O.ciscoEnvMonFanState in oid:
                    fan_sensors[sensor_id].set_state(value)
            if O.ciscoEnvMonSupplyStatusTable in oid:
                sensor_id = oid.rsplit('.', 1)[-1]
                if sensor_id not in pw_sensors.keys():
                    pw_sensors[sensor_id] = Sensor(sensor_id)
                if O.ciscoEnvMonSupplyStatusDescr in oid:
                    pw_sensors[sensor_id].set_description(value)
                if O.ciscoEnvMonSupplyState in oid:
                    pw_sensors[sensor_id].set_state(value)

    for sensor in volt_sensors:
        s.add_sensor('volt', volt_sensors[sensor].description, volt_sensors[sensor].state)
    for sensor in temp_sensors:
        s.add_sensor('temp', temp_sensors[sensor].description, temp_sensors[sensor].state)
    for sensor in fan_sensors:
        s.add_sensor('fan', fan_sensors[sensor].description, fan_sensors[sensor].state)
    for sensor in pw_sensors:
        s.add_sensor('pw', pw_sensors[sensor].description, pw_sensors[sensor].state)

    s.set_message()
    nelmon_exit(s.status, s.output)

if __name__ == "__main__":
    main()
