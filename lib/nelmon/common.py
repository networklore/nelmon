"""nelmon.common."""
import sys

from nelmon import constants as C
from nelmon.globals import NelmonGlobals


def nelmon_exit(exit_code, output_message, perf_data=None):
    """End program, return error code and output_message."""
    prefix = ''
    if NelmonGlobals.OUTPUT_FORMAT == 'with_status':
        prefix = '%s - ' % C.STATUS_NAME[exit_code]
    if perf_data:
        if isinstance(perf_data, list):
            perf_header = ' | %s' % perf_data[0]
        else:
            perf_header = ' | %s' % perf_data
    else:
        perf_header = ''
    if isinstance(output_message, list):
        i = 0
        for message in output_message:
            if i == 0:
                print prefix + message + perf_header
            else:
                print message
            i += 1
    else:
        print prefix + str(output_message) + perf_header
    sys.exit(exit_code)


def verify_nelmon_features():
    """Check to see that Nelmon version isn't too low."""
    if C.NELMON_VERSION < NelmonGlobals.MIN_NELMON_VER:
        nelmon_exit(
            C.UNKNOWN,
            'Requires Nelmon v.%s, download at https://networklore.com/nelmon/' % (
                NelmonGlobals.MIN_NELMON_VER)
        )
