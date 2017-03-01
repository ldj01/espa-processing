
# Filename extension for Landsat based input products
LANDSAT_INPUT_FILENAME_EXTENSION = '.tar.gz'

# Filename extension for Modis based input products
MODIS_INPUT_FILENAME_EXTENSION = '.hdf'

# Path to the completed orders
ESPA_REMOTE_CACHE_DIRECTORY = '/data2/science_lsrd/LSRD/orders'
ESPA_LOCAL_CACHE_DIRECTORY = ''

# Number of seconds to sleep when errors are encountered before attempting the
# task again
DEFAULT_SLEEP_SECONDS = 2

# Maximum number of times to attempt packaging, delivery, and distribution
MAX_PACKAGING_ATTEMPTS = 3
MAX_DELIVERY_ATTEMPTS = 3
MAX_DISTRIBUTION_ATTEMPTS = 5

# Maximum number of times to attempt setting the scene error
MAX_SET_SCENE_ERROR_ATTEMPTS = 5

# Specify the checksum tool and filename extension
ESPA_CHECKSUM_TOOL = 'md5sum'
ESPA_CHECKSUM_EXTENSION = 'md5'

# Plotting defaults
PLOT_BG_COLOR = '#f3f3f3'  # A light gray
PLOT_MARKER = (1, 3, 0)    # Better circle than 'o'
PLOT_MARKER_SIZE = 5.0     # A good size for the circle or diamond
PLOT_MARKER_EDGE_WIDTH = 0.9  # The width of the black marker border

# We are only supporting one radius when warping to sinusoidal
SINUSOIDAL_SPHERE_RADIUS = 6371007.181

# Some defines for common pixels sizes in decimal degrees
DEG_FOR_30_METERS = 0.0002695
DEG_FOR_15_METERS = (DEG_FOR_30_METERS / 2.0)
DEG_FOR_1_METER = (DEG_FOR_30_METERS / 30.0)

# Supported datums - the strings for them
WGS84 = 'WGS84'
NAD27 = 'NAD27'
NAD83 = 'NAD83'
# WGS84 should always be first in the list
VALID_DATUMS = [WGS84, NAD27, NAD83]

TRANSFER_BLOCK_SIZE = 10485760

# We do not allow any user selectable choices for this projection
GEOGRAPHIC_PROJ4_STRING = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

# Band type data ranges.  They are intended to be used for removing outliers
# from the data before statistics generation
# Must match DATA_MAX_Y and DATA_MIN_Y values in plotting.py
# The types must match the types in cdr_ecv.py and modis.py
# Note: These are also defined in such away that the fill values are also
#       excluded.
BAND_TYPE_STAT_RANGES = {
    'SR': {
        'UPPER_BOUND': 10000,
        'LOWER_BOUND': 0
    },
    'TOA': {
        'UPPER_BOUND': 10000,
        'LOWER_BOUND': 0
    },
    'INDEX': {
        'UPPER_BOUND': 10000,
        'LOWER_BOUND': -1000
    },
    'LST': {
        'UPPER_BOUND': 65535,
        'LOWER_BOUND': 7500
    },
    'LANDSAT_LST': {
        'UPPER_BOUND': 3730,
        'LOWER_BOUND': 1500
    },
    'EMIS': {
        'UPPER_BOUND': 255,
        'LOWER_BOUND': 1
    }
}


'''
LOGGING DEFINITIONS
'''
PROCESSING_LOGGER = 'espa.processing'

LOGGER_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'espa.standard': {
            # Used by the processing system
            'format': ('%(asctime)s.%(msecs)03d %(process)d'
                       ' %(levelname)-8s'
                       ' %(filename)s:%(lineno)d:%(funcName)s'
                       ' -- %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'espa.thread': {
            # An example for threading, not currently used
            'format': ('%(asctime)s.%(msecs)03d %(process)d'
                       ' %(levelname)-8s'
                       ' %(filename)s:%(lineno)d:%(funcName)s'
                       ' %(thread)d'
                       ' -- %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        # All espa.* handler names need to match the espa.* logger names
        'espa.processing': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'espa.standard',
            'filename': '/tmp/espa-processing.log',
            'mode': 'a'
        }
    },
    'loggers': {
        # All espa.* logger names need to match the espa.* handler names
        'espa.processing': {
            # To be used by the processing system
            'level': 'INFO',
            'propagate': False,
            'handlers': ['espa.processing']
        }
    }
}
