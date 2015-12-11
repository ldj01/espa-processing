
'''
License: "NASA Open Source Agreement 1.3"

Description:
    Provides the exceptions used in the espa-processor.
'''


class ESPAException(Exception):
    '''Base ESPA exception'''
    pass


class ESPAValidationError(ESPAException):
    '''Exception raised during any validation'''
    pass


class ESPAEnvironmentError(ESPAException):
    '''Exception raised by environment processing'''
    pass


class ESPAReporterError(ESPAException):
    '''Exception raised by reporting'''
    pass
