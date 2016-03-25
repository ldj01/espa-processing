# The maximum number of jobs Hadoop should be able to run at once.
# This is needed so that the job tracker doesn't exceed resource limits.
# This also affects our level of service to end users.
# We are submitting batches of 25 every minute, so 25 * 50 = 1250 scenes.
# This means it will take a little over an hour to addres an item ordered
# because the hadoop queue will be 25 * 50 scenes deep.
HADOOP_MAX_JOBS = 50


# Set the hadoop timeouts to a ridiculous number so jobs don't get killed
# before they are done
HADOOP_TIMEOUT = 172800000  # which is 2 days

# Specifies the hadoop queue to use based on priority
# 'all' must be present as it is used in the cron code to pass 'None' instead
HADOOP_QUEUE_MAPPING = {
    'all': 'ondemand',
    'low': 'ondemand-low',
    'normal': 'ondemand',
    'high': 'ondemand-high'
}


'''
LOGGING DEFINITIONS
'''
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
        'espa.standard.low': {
            # Provided so 'low' is added to the log message
            'format': ('%(asctime)s.%(msecs)03d %(process)d'
                       ' %(levelname)-8s    low '
                       ' %(filename)s:%(lineno)d:%(funcName)s'
                       ' -- %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'espa.standard.normal': {
            # Provided so 'normal' is added to the log message
            'format': ('%(asctime)s.%(msecs)03d %(process)d'
                       ' %(levelname)-8s normal '
                       ' %(filename)s:%(lineno)d:%(funcName)s'
                       ' -- %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'espa.standard.high': {
            # Provided so 'high' is added to the log message
            'format': ('%(asctime)s.%(msecs)03d %(process)d'
                       ' %(levelname)-8s   high '
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
        'espa.cron.all': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'espa.standard',
            'filename': '/tmp/espa-cron.log',
            'mode': 'a'
        },
        'espa.cron.low': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'espa.standard.low',
            'filename': '/tmp/espa-cron.log',
            'mode': 'a'
        },
        'espa.cron.normal': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'espa.standard.normal',
            'filename': '/tmp/espa-cron.log',
            'mode': 'a'
        },
        'espa.cron.high': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'espa.standard.high',
            'filename': '/tmp/espa-cron.log',
            'mode': 'a'
        },
        'espa.cron.plot': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'espa.standard',
            'filename': '/tmp/espa-plot-cron.log',
            'mode': 'a'
        },
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
        # All espa.cron.<priority> must match the priority levels defined in
        # settings.HADOOP_QUEUE_MAPPING above
        'espa.cron.all': {
            # To be used by the 'all' cron
            'level': 'INFO',
            'propagate': False,
            'handlers': ['espa.cron.all']
        },
        'espa.cron.low': {
            # To be used by the 'low' cron
            'level': 'INFO',
            'propagate': False,
            'handlers': ['espa.cron.low']
        },
        'espa.cron.normal': {
            # To be used by the 'normal' cron
            'level': 'INFO',
            'propagate': False,
            'handlers': ['espa.cron.normal']
        },
        'espa.cron.high': {
            # To be used by the 'high' cron
            'level': 'INFO',
            'propagate': False,
            'handlers': ['espa.cron.high']
        },
        'espa.cron.plot': {
            # To be used by the 'lpcs' cron
            'level': 'INFO',
            'propagate': False,
            'handlers': ['espa.cron.plot']
        },
        'espa.processing': {
            # To be used by the processing system
            'level': 'INFO',
            'propagate': False,
            'handlers': ['espa.processing']
        }
    }
}
