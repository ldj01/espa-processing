
# This code is just a concept implementation to see if it is worthwhile to
# pursue


import request_validation


# The three laws:
#   1) A processor contains a list of tasks to be executed in the specified
#      order and must contain one or more tasks.
#   2) A task accomplishes a single part of the whole process.
#   3) A task can implement a processor to accomplish sub-tasks.


# NOTE - TODO - Each of these classes would probably be implemented in
#               their own files.


class Processor(object):
    '''Provides the mechanism to run a sequential list of tasks'''

    def __init__(self):
        super(Processor, self).__init__()

        self.processing_tasks = list()

        print 'Processor.__init__'

    def add(self, processing_task):
        '''Add a task to the task list'''
        self.processing_tasks.append(processing_task)

    def run(self):
        '''Execute each task in the order recieved'''
        for processing_task in self.processing_tasks:
            processing_task.execute()


class ProcessingTask(object):
    '''Provides a consistent api for processing a task'''

    def __init__(self):
        '''Configure any internal properties required to accomplish
           executing the task'''
        super(ProcessingTask, self).__init__()

    def execute(self):
        '''Execute or implement the specific task'''
        raise NotImplementedError('Not Implemented')


class ConvertToInternalFormat(ProcessingTask):
    '''Provides the implementation for converting to our internal ENVI
       format'''

    def __init__(self, options):
        super(ConvertToInternalFormat, self).__init__()

    def execute(self):
        print 'executing --- ConvertToInternalFormat'


class GenerateSpectralIndices(ProcessingTask):
    '''Provides the implementation for generating spectral indice products'''

    def __init__(self, options):
        super(GenerateSpectralIndices, self).__init__()

    def execute(self):
        print 'executing --- GenerateSpectralIndices'


class CleanupIntermediateProducts(ProcessingTask):
    '''Provides the implementation for customizing the science products'''

    def __init__(self, options):
        super(CleanupIntermediateProducts, self).__init__()

        # This task is split-up into multiple sub-tasks

    def execute(self):
        print 'executing --- CleanupIntermediateProducts'


class BuildScienceProducts(ProcessingTask):
    '''Provides the implementation for building the science products'''

    def __init__(self, options):
        super(BuildScienceProducts, self).__init__()

        # This task is split-up into multiple sub-tasks
        self.processor = Processor()

        if options['include_indices']:
            task = GenerateSpectralIndices(options)
            self.processor.add(task)

        # We always cleanup any intermediate science products
        self.processor.add(CleanupIntermediateProducts(options))

    def execute(self):
        print 'executing --- BuildScienceProducts'
        self.processor.run()


class CustomizeProducts(ProcessingTask):
    '''Provides the implementation for customizing the science products'''

    def __init__(self, options):
        super(CustomizeProducts, self).__init__()

    def execute(self):
        print 'executing --- CustomizeProducts'


class PackageProducts(ProcessingTask):
    '''Provides the implementation for packaging the science products'''

    def __init__(self, options):
        super(PackageProducts, self).__init__()

    def execute(self):
        print 'executing --- PackageProducts'


class TransferProducts(ProcessingTask):
    '''Provides the implementation for transferring the package to a remote
       system'''

    def __init__(self, options):
        super(TransferProducts, self).__init__()

    def execute(self):
        print 'executing --- TransferProducts'


class DistributeProducts(ProcessingTask):
    '''Provides the implementation for distributing products'''

    def __init__(self, options):
        super(DistributeProducts, self).__init__()

        # This task is split-up into multiple sub-tasks
        self.processor = Processor()

        # We always package the science products
        self.processor.add(PackageProducts(options))

        if options['distribution_mode'] == 'remote':
            self.processor.add(PackageProducts(options))

    def execute(self):
        print 'executing --- DistributeProducts'
        self.processor.run()


class RequestProcessor(object):
    '''Determine processing order and perform initialization of each task'''

    def __init__(self, options):
        super(RequestProcessor, self).__init__()

        # Validate the request options before anything else
        request_validation.validate_request(options)

        self.__dict__ = options
        self.__setattr__('processor', Processor())

        print 'RequestProcessor.__init__'

    def initialize(self):
        # We always convert to our internal format
        self.processor.add(ConvertToInternalFormat(self.__dict__))

        # If any science products are requested then add the task to build science
        # products
#        if self.__dict__['include_indices']:
#            self.add(BuildScienceProducts(self.__dict__))

        # If we need to customize the science products, then add the
        # customization task
#        if self.__dict__['customize_products']:
#            self.add(CustomizeProducts(self.__dict__))

        # We always distribute our science products
        self.processor.add(DistributeProducts(self.__dict__))


if __name__ == '__main__':
#    request_options = {
#        'include_indices': True,
#        'customize_products': False,
#        'distribution_mode': 'local'
#    }

    request_options = {
        'products': ['tm_sr', 'tm_toa', 'tm_ndvi'],
#        'test': [{'a': 5}, {'a': 4}],
        'customizations': {
            'projection': {'name': 'utm', 'zone': 16, 'zone_ns': 'north'}
        }
    }

#    request_processor = RequestProcessor(request_options)
#    request_processor.initialize()
#    request_processor.run()
