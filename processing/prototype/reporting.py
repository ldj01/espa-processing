
'''
License: "NASA Open Source Agreement 1.3"

Description:
    Provides the reporting/logging configuration and creation for the
    espa-processing system.
'''


import logging
import logging.config


from PropertyDictionary.collection import PropertyDict


from espa_exceptions import ESPAReporterError


# Defines the standard message formatting used in espa-processing logs
LOG_MSG_FORMAT = (
    '%(asctime)s.%(msecs)03d %(process)d'
    ' %(levelname)-8s'
    ' %(filename)s:%(lineno)d:%(funcName)s'
    ' -- %(message)s')
# Defines the standard date formatting used in espa-processing logs
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Defines the supported reporters used in espa-processing
REPORTER_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'espa.mapper': {
            'format': LOG_MSG_FORMAT,
            'datefmt': LOG_DATE_FORMAT
        },
        'espa.request': {
            'format': LOG_MSG_FORMAT,
            'datefmt': LOG_DATE_FORMAT
        }
    },
    'handlers': {
        'espa.mapper': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'espa.mapper',
            'filename': '/tmp/espa-mapper.log',
            'mode': 'a'
        },
        'espa.request': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'espa.request',
            'filename': '/tmp/espa-processing.log',
            'mode': 'a'
        }
    },
    'loggers': {
        'espa.mapper': {
            'level': 'INFO',
            'propagate': False,
            'handlers': ['espa.mapper']
        },
        'espa.request': {
            'level': 'INFO',
            'propagate': False,
            'handlers': ['espa.request']
        }
    }
}


class Reporter(object):
    '''Provides access to a configured logger which is intended to be shared
       between request tasks within the same process'''

    config = None

    @classmethod
    def configure(cls,
                  reporter_name='espa.request',
                  filename=None,
                  level=logging.DEBUG):
        '''Configures/initializes the reporter'''

        if cls.config is None:
            cls.config = PropertyDict()
            cls.config.version = REPORTER_CONFIG['version']
            cls.config.disable_existing_loggers = (
                REPORTER_CONFIG['disable_existing_loggers'])
            cls.config.loggers = PropertyDict()
            cls.config.handlers = PropertyDict()
            cls.config.formatters = PropertyDict()

        name = reporter_name.lower()
        loggers = REPORTER_CONFIG['loggers']
        handlers = REPORTER_CONFIG['handlers']
        formatters = REPORTER_CONFIG['formatters']

        # Check if avaliable
        if (name not in loggers or
                name not in handlers or
                name not in formatters):

            msg = '[{0}] is not an available reporter'.format(name)
            raise ESPAReporterError(msg)

        # Check if not already configured
        if name not in cls.config.loggers:
            # Add the reporter
            cls.config.loggers[name] = PropertyDict(loggers[name])

            # Configure the reporting level
            cls.config.loggers[name].level = level

            # Add the configured handler
            cls.config.handlers[name] = PropertyDict(handlers[name])

            # Add the configured formatter
            formatter_name = cls.config.handlers[name].formatter
            cls.config.formatters[formatter_name] = (
                PropertyDict(formatters[formatter_name]))

            if filename is not None:
                cls.config.handlers[name].filename = filename

            # Now configure the python logging module
            logging.config.dictConfig(dict(cls.config))

    @classmethod
    def check_configured(cls, reporter_name):
        '''Checks is a reporter has been configured'''

        name = reporter_name.lower()
        if name not in cls.config.loggers:
            msg = '[{0}] is not a configured reporter'.format(name)
            raise ESPAReporterError(msg)

    @classmethod
    def reporter(cls, reporter_name):
        '''Returns an already configured reporter from the python logging
           module'''

        name = reporter_name.lower()
        cls.check_configured(name)

        return logging.getLogger(name)

    @classmethod
    def read_reported_data(cls, reporter_name):
        '''Reads the contents of a log file into memory
           If the reporter logs to a file and after verifying existence of
           the log file
           An empty string is returned if the reporter is not a FileHandler'''

        name = reporter_name.lower()
        cls.check_configured(name)

        data = ''
        if (cls.config.handlers[name]['class'] == 'logging.FileHandler' and
                os.path.exists(cls.config.handlers[name].filename)):

            if os.path.exists(filename):
                with open(filename, 'r') as fd:
                    data = fd.read()

        return data
