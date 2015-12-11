
'''
License: "NASA Open Source Agreement 1.3"

Description:
    Implements a command processor for the espa-processing system.
'''


import os
import logging
from cerberus import Validator
from PropertyDictionary.collection import PropertyDict

import request_schema
from espa_exceptions import ESPAValidationError, ESPAEnvironmentError
from reporting import Reporter
from strategy import Task, TaskChain
from environment import RetrieveEnvironment
from distributing import DISTRIBUTION_METHODS, PackageProducts, TransferPackage
from science_products import GenerateSpectralIndices


# The three laws:
#   1) A TaskChain contains a list of Task's to be executed in the specified
#      order and must contain one or more Task's.
#   2) A Task accomplishes a single part of the whole process.
#   3) A Task can be a TaskChain.


# NOTE - TODO - Each of these classes will probably be implemented in
#               their own files.


class InitializeProcessingDirectories(Task):
    '''Provides the implementation for converting to our internal ENVI
       format'''

    def __init__(self, options, ctx):
        self.task_schema = {
            'base_work_dir': {'type': 'string', 'required': True},
            'order_id': {'type': 'string', 'required': True},
            'product_id': {'type': 'string', 'required': True}
        }

        super(InitializeProcessingDirectories, self).__init__(options)

        ctx.order_dir = os.path.join(self.options.base_work_dir,
                                     self.options.order_id)
        ctx.product_dir = os.path.join(ctx.order_dir,
                                       self.options.product_id)

        ctx.stage_dir = os.path.join(ctx.product_dir, 'stage')
        ctx.work_dir = os.path.join(ctx.product_dir, 'work')

        # TODO TODO TODO - Fix for local vs remote
        ctx.output_dir = os.path.join(ctx.product_dir, 'output')

    def execute(self, ctx):
        ctx.reporter.info('executing --- {0}'.format(self.__class__.__name__))
        output = PropertyDict()
        # TODO TODO TODO - Do the work
        output.test_output = 'test_output'
        # TODO TODO TODO - Do the work
        return output


class ConvertToInternalFormat(Task):
    '''Provides the implementation for converting to our internal ENVI
       format'''

    def __init__(self, options, ctx):
        self.task_schema = {
            'keep_intermediate_data': {'type': 'string', 'required': True}
        }

        super(ConvertToInternalFormat, self).__init__(*args, **kwargs)

    def execute(self, ctx):
        ctx.reporter.info('executing --- {0}'.format(self.__class__.__name__))
        output = PropertyDict()
        return output

class CleanupIntermediateProducts(Task):
    '''Provides the implementation for customizing the science products'''

    def __init__(self, options, ctx):
        self.task_schema = {
            'something': {'type': 'string', 'required': True},
            'fun': {'type': 'string', 'required': True}
        }

        super(CleanupIntermediateProducts, self).__init__()

        # This task is split-up into multiple sub-tasks

    def execute(self, ctx):
        ctx.reporter.info('executing --- {0}'.format(self.__class__.__name__))
        output = PropertyDict()
        return output


class CustomizeProducts(Task):
    '''Provides the implementation for customizing the science products'''

    def __init__(self, options, ctx):
        self.task_schema = {
            'something': {'type': 'string', 'required': True},
            'fun': {'type': 'string', 'required': True}
        }

        super(CustomizeProducts, self).__init__()

    def execute(self, ctx):
        ctx.reporter.info('executing --- {0}'.format(self.__class__.__name__))
        output = PropertyDict()
        return output


class TransferProducts(Task):
    '''Provides the implementation for transferring the package to a remote
       system'''

    def __init__(self, options, ctx):
        self.task_schema = {
            'something': {'type': 'string', 'required': True},
            'fun': {'type': 'string', 'required': True}
        }

        super(TransferProducts, self).__init__()

    def execute(self, ctx):
        ctx.reporter.info('executing --- {0}'.format(self.__class__.__name__))
        output = PropertyDict()
        return output


class RequestProcessor(TaskChain):
    '''Determine processing order and perform initialization of each task'''

    def __init__(self, options, ctx):
        self.task_schema = request_schema.schema

        super(RequestProcessor, self).__init__(options)

        # Strip sensor off of the products -----------------------------------
        # Because we don't care anymore and it removes sensor from the logic
        # TODO TODO TODO - Do I still need the sensor for somethings??????
        self.options.products = ['_'.join(x.split('_')[1:])
                                 for x in self.options.products]

        # Initialize the reporting -------------------------------------------
        # Figure out filename
        ctx.report_filename = ('/tmp/espa-job-{0}-{1}.log'
                               .format(options.input.order_id,
                                       options.input.product_id))

        # Default (processing)required options not provided
        if options.developer_options is not None:
            ctx.developer_options = PropertyDict(options.developer_options)
        else:
            ctx.developer_options = PropertyDict()
            ctx.developer_options.debug = False
            ctx.developer_options.keep_directory = False
            ctx.developer_options.keep_intermediate_data = False
            ctx.developer_options.keep_log = False

        # Fixup the reporting level
        ctx.reporting_level = logging.INFO
        if ctx.developer_options.debug:
            ctx.reporting_level = logging.DEBUG

        # Configure the reporter
        Reporter.configure(reporter_name='espa.request',
                           filename=ctx.report_filename,
                           level=ctx.reporting_level)

        # Set the reporter
        ctx.reporter = Reporter.reporter('espa.request')

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
        self.add(RetrieveEnvironment(task_options, ctx))

        # Initialize processing directories ----------------------------------
        bwd = ctx.base_work_dir

        # Finalize the base working directory in the ctx
        if bwd is None or bwd is '':
            bwd = os.getcwd()

        bwd = os.path.abspath(bwd)
        ctx.base_work_dir = bwd

        # We always initialize the processing directories
        task_options = {
            'base_work_dir': ctx.base_work_dir,
            'order_id': self.options.input.order_id,
            'product_id': self.options.input.product_id
        }
        self.add(InitializeProcessingDirectories(task_options, ctx))
        ctx.reporter.debug(str(ctx))

        for product in self.options.products:
            if product in ['l1_customized', 'toa', 'bt', 'sr', 'cfmask',
                           'dswe', 'lst', 'toa_evi', 'toa_msavi', 'toa_nbr',
                           'toa_nbr2', 'toa_ndmi', 'toa_ndvi', 'toa_savi',
                           'sr_evi', 'sr_msavi', 'sr_nbr', 'sr_nbr2',
                           'sr_ndmi', 'sr_ndvi', 'sr_savi', 'statistics']:

                task_options = {
                    'keep_intermediate_data': (
                        ctx.developer_options.keep_intermediate_data or True)
                }
                self.add(ConvertToInternalFormat(task_options, ctx))
                ctx.reporter.debug(str(ctx))
                break

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
        'products': ['tm_sr', 'tm_toa', 'tm_sr_ndvi'],
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

    ctx = PropertyDict()
    request_processor = RequestProcessor(PropertyDict(request_options), ctx)
    output = PropertyDict()
    output.update(request_processor.execute(ctx))
    print output
