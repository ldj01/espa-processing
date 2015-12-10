
'''
License: "NASA Open Source Agreement 1.3"

Description:
    Implements a prototype command processor for the espa-processing system.
'''


import os
import logging
from cerberus import Validator
from PropertyDictionary.collection import PropertyDict

import request_schema
from espa_exceptions import ESPAValidationError, ESPAEnvironmentError
from reporting import Reporter
from strategy import Task, TaskChain
from new_distributing import DISTRIBUTION_METHODS


# The three laws:
#   1) A TaskCain contains a list of Task's to be executed in the specified
#      order and must contain one or more Task's.
#   2) A Task accomplishes a single part of the whole process.
#   3) A Task can be a TaskChain.


# NOTE - TODO - Each of these classes will probably be implemented in
#               their own files.


class RetrieveEnvironment(Task):
    '''Provides the implementation for retrieving the environment'''

    def __init__(self, options, context):
        self.task_schema = {
            'name': {'type': 'string', 'required': True},
            'required': {'type': 'boolean', 'required': True},
            'valid_values': {'type': 'list', 'nullable': True,
                             'required': True},
            'value': {'type': 'string', 'nullable': True, 'required': False}
        }

        super(RetrieveEnvironment, self).__init__(options)

        for key in self.options.keys():
            item = self.options[key]
            # Check that required variables are present in the environment
            if item.required and (item.name not in os.environ):
                msg = ('Environment variable ${0} is not defined'
                       .format(item.name))
                raise ESPAEnvironmentError(msg)

            item.value = os.environ.get(item.name, '')

            # If it has a strict set of values, verify that it is set to one
            # of them
            if item.valid_values is not None:
                if item.value not in item.valid_values:
                    msg = ('Invalid ${0} value was \'{1}\','
                           ' but should be one of {2}'
                           .format(item.name, item.value, item.valid_values))
                    raise ESPAEnvironmentError(msg)

            # Transfer the environment to the context parameter
            context[key] = item.value

    def validate(self):
        '''Validate the provided options'''
        for key in self.options.keys():
            self.validator.validate(dict(self.options[key]), self.task_schema)

            if self.validator.errors:
                raise ESPAValidationError(self.validator.errors)

    def execute(self):
        '''We don't need this to do anything at the moment'''
        print 'executing --- {0}'.format(self.__class__.__name__)
        output = PropertyDict()
        return output


class InitializeProcessingDirectories(Task):
    '''Provides the implementation for converting to our internal ENVI
       format'''

    def __init__(self, options, context):
        self.task_schema = {
            'base_work_dir': {'type': 'string', 'required': True},
            'order_id': {'type': 'string', 'required': True},
            'product_id': {'type': 'string', 'required': True}
        }

        super(InitializeProcessingDirectories, self).__init__(options)

        context.order_dir = os.path.join(self.options.base_work_dir,
                                         self.options.order_id)
        context.product_dir = os.path.join(context.order_dir,
                                           self.options.product_id)

        context.stage_dir = os.path.join(context.product_dir, 'stage')
        context.work_dir = os.path.join(context.product_dir, 'work')

        # TODO TODO TODO - Fix for local vs remote
        context.output_dir = os.path.join(context.product_dir, 'output')

    def execute(self):
        print 'executing --- {0}'.format(self.__class__.__name__)
        output = PropertyDict()
        # TODO TODO TODO - Do the work
        output.test_output = 'test_output'
        # TODO TODO TODO - Do the work
        return output


class ConvertToInternalFormat(Task):
    '''Provides the implementation for converting to our internal ENVI
       format'''

    def __init__(self, options, context):
        self.task_schema = {
            'something': {'type': 'string', 'required': True},
            'fun': {'type': 'string', 'required': True}
        }

        super(ConvertToInternalFormat, self).__init__(*args, **kwargs)

    def execute(self):
        print 'executing --- {0}'.format(self.__class__.__name__)


class GenerateSpectralIndices(Task):
    '''Provides the implementation for generating spectral indice products'''

    def __init__(self, options, context):
        self.task_schema = {
            'something': {'type': 'string', 'required': True},
            'fun': {'type': 'string', 'required': True}
        }

        super(GenerateSpectralIndices, self).__init__()

    def execute(self):
        print 'executing --- {0}'.format(self.__class__.__name__)


class CleanupIntermediateProducts(Task):
    '''Provides the implementation for customizing the science products'''

    def __init__(self, options, context):
        self.task_schema = {
            'something': {'type': 'string', 'required': True},
            'fun': {'type': 'string', 'required': True}
        }

        super(CleanupIntermediateProducts, self).__init__()

        # This task is split-up into multiple sub-tasks

    def execute(self):
        print 'executing --- {0}'.format(self.__class__.__name__)


class CustomizeProducts(Task):
    '''Provides the implementation for customizing the science products'''

    def __init__(self, options, context):
        self.task_schema = {
            'something': {'type': 'string', 'required': True},
            'fun': {'type': 'string', 'required': True}
        }

        super(CustomizeProducts, self).__init__()

    def execute(self):
        print 'executing --- {0}'.format(self.__class__.__name__)


class TransferProducts(Task):
    '''Provides the implementation for transferring the package to a remote
       system'''

    def __init__(self, options, context):
        self.task_schema = {
            'something': {'type': 'string', 'required': True},
            'fun': {'type': 'string', 'required': True}
        }

        super(TransferProducts, self).__init__()

    def execute(self):
        print 'executing --- {0}'.format(self.__class__.__name__)


class RequestProcessor(TaskChain):
    '''Determine processing order and perform initialization of each task'''

    def __init__(self, options, context):
        self.task_schema = request_schema.schema

        super(RequestProcessor, self).__init__(options)

        # Initialize the reporting -------------------------------------------
        # Figure out filename
        context.report_filename = ('/tmp/espa-job-{0}-{1}.log'
                                   .format(options.order_id,
                                           options.product_id))

        # Figure out reporting level
        context.reporting_level = logging.INFO
        if options.developer_options is not None:
            if options.developer_options.debug:
                context.reporting_level = logging.DEBUG

        # Configure the reporter
        Reporter.configure(reporter_name='espa.request',
                           filename=context.report_filename,
                           level=context.reporting_level)

        # Set the reporter
        context.reporter = Reporter.reporter('espa.request')

        # Validate the environment -------------------------------------------
        task_options = {
            'dist_method': {'name': 'ESPA_DISTRIBUTION_METHOD',
                            'required': True,
                            'valid_values': DISTRIBUTION_METHODS,
                            'value': None},
            'dist_dir': {'name': 'ESPA_DISTRIBUTION_DIR',
                         'required': False,
                         'valid_values': None,
                         'value': None},
            'base_work_dir': {'name': 'ESPA_WORK_DIR',
                              'required': False,
                              'valid_values': None,
                              'value': None}
        }
        self.add(RetrieveEnvironment(task_options, context))

        # Initiali processing directories ------------------------------------
        bwd = context.base_work_dir

        # Finalize the base working directory in the context
        if bwd is None or bwd is '':
            bwd = os.getcwd()

        bwd = os.path.abspath(bwd)
        context.base_work_dir = bwd

        # We always initialize the processing directories
        task_options = {
            'base_work_dir': context.base_work_dir,
            'order_id': self.options.input.order_id,
            'product_id': self.options.input.product_id
        }
        self.add(InitializeProcessingDirectories(task_options, context))

        print context
        # TODO TODO TODO - Add the remaining tasks
        # "Strategy" is performed here to only add the tasks required for this
        # request
        # TODO TODO TODO - Add the remaining tasks
        # TODO TODO TODO - Add the remaining tasks
        # TODO TODO TODO - Add the remaining tasks
        # TODO TODO TODO - Add the remaining tasks
        # TODO TODO TODO - Add the remaining tasks
        # TODO TODO TODO - Add the remaining tasks


if __name__ == '__main__':
    request_options = {
        'input': {
            'order_id': 'TOA_PRE',
            'product_id': 'LE70420332015090EDC00',
            'product_url': '/path/to/LE70420332015090EDC00'
        },
        'products': ['tm_sr', 'tm_toa', 'tm_ndvi'],
        'customizations': {
            'projection': {'name': 'utm', 'zone': 16, 'zone_ns': 'north'}
        },
        'developer_options': {
            'debug': True,
            'keep_directory': True,
            'keep_intermediate_data': True,
            'keep_log': True
        }

    }

    context = PropertyDict()
    request_processor = RequestProcessor(PropertyDict(request_options), context)
    output = PropertyDict()
    output.update(request_processor.execute())
    print output
