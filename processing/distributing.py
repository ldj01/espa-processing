
'''
License:
  "NASA Open Source Agreement 1.3"

Description:
  Provides a mechanism for distributing products.
'''

import os

# imports from espa_common
from logger_factory import EspaLogging
import settings

# local objects and methods
from environment import Environment, DISTRIBUTION_METHOD_LOCAL
import packaging
import transferring


# Define the logger this module will use
logger = EspaLogging.get_logger(settings.PROCESSING_LOGGER)


# ----------------------------------------------------------------------------
class DistributingError(Exception):
    '''Distribution specific exception'''
    pass


# ----------------------------------------------------------------------------
class Distributor(object):
    '''
    Description:
        Provides the base distributor.
    '''

    def __init__(self):
        super(Distributor, self).__init__()

    def distribute(self, source_path, order_id, product_name):
        '''
        Description:
            Child classes overwrite this for specific implementations.
        '''
        raise NotImplementedError('Please implement the (distribute) method')


# ----------------------------------------------------------------------------
class LocalDistributor(Distributor):
    '''
    Description:
        Provides the specifics for a local destination distribution.
    '''

    def __init__(self):
        super(LocalDistributor, self).__init__()

    def distribute(self, source_path, order_id, base_product_name):
        '''
        Description:
            Provides the tasks to be accomplished for this distributor.

        Inputs:
            See this modules distribute method below.

        Returns:
            See this modules distribute method below.
        '''

        # Use the environment configured distribution directory as the base
        # packaging path
        base_path = Environment().get_distribution_directory()

        # Append the order ID to the base path to create the full packaging
        # path
        package_path = os.path.join(base_path, order_id)

        try:
            (full_package_path, checksum) = (
                packaging.package(source_path, package_path,
                                  base_product_name))
        except packaging.PackagingError as exception:
            raise DistributingError(exception)

        return (full_package_path, checksum)


# ----------------------------------------------------------------------------
class RemoteDistributor(Distributor):
    '''
    Description:
        Provides the specifics for a remote destination distribution.
    '''

    def __init__(self):
        super(RemoteDistributor, self).__init__()

    def distribute(self, source_path, order_id, base_package_name):
        '''
        Description:
            Provides the tasks to be accomplished for this distributor.

        Inputs:
            See this modules distribute method below.

        Returns:
            See this modules distribute method below.
        '''

        # TODO TODO TODO
        # TODO TODO TODO
        # Figure out how to determine these
        package_path = 'peter.pan'
        remote_host = 'tiger.lilly'
        remote_path = 'tinkerbell'
        remote_user = 'wendy'
        remote_passwd = 'captain.hook'
        # TODO TODO TODO
        # TODO TODO TODO

        try:
            (full_package_path, checksum) = (
                packaging.package(source_path, package_path,
                                  base_package_name))
            full_transferred_path = (
                transferring.transfer(full_package_path, checksum,
                                      remote_host, remote_path,
                                      remote_user, remote_passwd))

        except packaging.PackagingError as exception:
            raise DistributingError(exception)

        except transferring.TransferringError as exception:
            raise DistributingError(exception)

        return (full_transferred_path, checksum)


# ----------------------------------------------------------------------------
def distribute(source_path, order_id, base_package_name):
    '''
    Description:
        Provides a means to call the correct distributor.  Based on the
        environment select the correct distributor class to use.

    Inputs:
        source_path(str) - The path to a directory containing all the contents
                           to be included in the package.
        order_id(str) - The order id appended to the base distribution path
                        where all the orders individual packages will be
                        placed.
        base_package_name(str) - The unique base filename for the package.

    Returns:
        full_transferred_path(str) - The full path including filename for
                                     where the product was delivered.  Either
                                     the local systems file path or the remote
                                     systems file path.
        checksum(str) - The actual checksum value.
    '''

    env = Environment()

    distribution_method = env.get_distribution_method()

    if distribution_method == DISTRIBUTION_METHOD_LOCAL:
        return LocalDistributor().distribute(source_path, order_id,
                                             base_package_name)

    else:
        return RemoteDistributor().distribute(source_path, order_id,
                                              base_package_name)
