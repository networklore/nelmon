

class NelmonGlobals(object):

    MIN_NELMON_VER = None
    PLUGIN_VERSION = None

    def __init__(self, **kwargs):

        for key in kwargs:
            if key == 'PLUGIN_VERSION':
                NelmonGlobals.PLUGIN_VERSION = kwargs[key]
            if key == 'MIN_NELMON_VER':
                NelmonGlobals.MIN_NELMON_VER = kwargs[key]
