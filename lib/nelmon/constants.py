"""nelmon.constants."""
import os
import sys
from nelmon import __version__

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

STATUS_NAME = {
    0: 'OK',
    1: 'WARNING',
    2: 'CRITICAL',
    3: 'UNKNOWN'
}
NELMON_VERSION = __version__
CURRENT_PLUGIN = sys.argv[0].split(os.sep)[-1]
