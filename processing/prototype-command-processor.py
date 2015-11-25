
# This code is just a concept implementation to see if it is worthwhile to
# pursue


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


class BuildScienceProducts(ProcessingTask):
    '''Provides the implementation for building the science products'''

    def __init__(self, options):
        super(BuildScienceProducts, self).__init__()

        # This task is split-up into multiple sub-tasks
        self.processor = Processor()

        if options['include_indices']:
            self.processor.add(GenerateSpectralIndices(options))

    def execute(self):
        print 'executing --- BuildScienceProducts'
        self.processor.run()


class CustomizeProducts(ProcessingTask):
    '''Provides the implementation for customizing the science products'''

    def __init__(self, options):
        super(CustomizeProducts, self).__init__()

    def execute(self):
        print 'executing --- CustomizeProducts'


class CleanupIntermediateProducts(ProcessingTask):
    '''Provides the implementation for customizing the science products'''

    def __init__(self, options):
        super(CleanupIntermediateProducts, self).__init__()

        # This task is split-up into multiple sub-tasks

    def execute(self):
        print 'executing --- CleanupIntermediateProducts'


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


def initialize(options):
    '''Determine processing order and perform initialization of each task'''

    processor = Processor()

    # We always convert to our internal format
    processor.add(ConvertToInternalFormat(options))

    # If any science products are requested then add the task to build science
    # products
    if options['include_indices']:
        processor.add(BuildScienceProducts(options))

    # We always cleanup any intermediate science products
    processor.add(CleanupIntermediateProducts(options))

    # If we need to customize the science products, then add the
    # customization task
    if options['customize_products']:
        processor.add(CustomizeProducts(options))

    # We always distribute our science products
    processor.add(DistributeProducts(options))

    return processor


if __name__ == '__main__':
    processing_options = {
        'include_indices': True,
        'customize_products': False,
        'distribution_mode': 'local'
    }

    print processing_options

    product_processor = initialize(processing_options)
    product_processor.run()
