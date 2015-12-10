
'''
License:
  "NASA Open Source Agreement 1.3"

Description:
  Provides a mechanism for distributing products.
'''

import os

from strategy import Task


# Define the distribution methods allowed
DISTRIBUTION_METHOD_LOCAL = 'local'
DISTRIBUTION_METHOD_REMOTE = 'remote'
DISTRIBUTION_METHODS = [DISTRIBUTION_METHOD_LOCAL,
                        DISTRIBUTION_METHOD_REMOTE]


class PackageProducts(Task):
    '''Provides the implementation for packaging the product'''

    def __init__(self, options, context):
        # TODO TODO TODO - Implement the schema
        self.task_schema = None

        super(PackageProduct, self).__init__(options)

        # TODO TODO TODO - Implement whatever

    def execute(self):
        # TODO TODO TODO - Implement whatever
        print 'executing --- {0}'.format(self.__class__.__name__)


class TransferPackage(Task):
    '''Provides the implementation for packaging the product'''

    def __init__(self, options, context):
        # TODO TODO TODO - Implement the schema
        self.task_schema = None

        super(TransferPackage, self).__init__(options)

        # TODO TODO TODO - Implement whatever

    def execute(self):
        # TODO TODO TODO - Implement whatever
        print 'executing --- {0}'.format(self.__class__.__name__)
