
'''
License: "NASA Open Source Agreement 1.3"

Description:
    Provides tasks related to the environment.
'''


import os
from PropertyDictionary.collection import PropertyDict


from strategy import Task


class RetrieveEnvironment(Task):
    '''Provides the implementation for retrieving the environment'''

    def __init__(self, options, ctx):
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

            # Transfer the environment to the ctx parameter
            ctx[key] = item.value

    def validate(self):
        '''Validate the provided options'''
        for key in self.options.keys():
            self.validator.validate(dict(self.options[key]), self.task_schema)

            if self.validator.errors:
                raise ESPAValidationError(self.validator.errors)

    def execute(self, ctx):
        '''We don't need this to do anything at the moment'''
        ctx.reporter.info('executing --- {0}'.format(self.__class__.__name__))
        output = PropertyDict()
        return output
