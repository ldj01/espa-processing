
'''
License: "NASA Open Source Agreement 1.3"

Description:
    Provides all of the tasks for kicking off science product generation.
    All of these tasks are usually simple wrappers to call the underlying
    science product helper scripts, which in turn call the correct science
    application executable.
'''

from strategy import Task


class GenerateSpectralIndices(Task):
    '''Provides the implementation for generating spectral indice products'''

    def __init__(self, options, ctx):
        self.task_schema = {
            'something': {'type': 'string', 'required': True},
            'fun': {'type': 'string', 'required': True}
        }

        super(GenerateSpectralIndices, self).__init__()

    def execute(self, ctx):
        ctx.reporter.info('executing --- {0}'.format(self.__class__.__name__))
        output = PropertyDict()
        return output

