
'''
License:
  "NASA Open Source Agreement 1.3"

Description:
  Provides a mechanism for packaging products.
'''

import os
import tarfile
import hashlib

# imports from espa_common
from logger_factory import EspaLogging
import settings

# Define the logger this module will use
logger = EspaLogging.get_logger(settings.PROCESSING_LOGGER)


# ----------------------------------------------------------------------------
class PackagingError(Exception):
    '''Distribution specific exception'''
    pass


# ----------------------------------------------------------------------------
class Packager(object):
    '''
    Description:
        Provides the base packager.
    '''

    def __init__(self):
        super(Packager, self).__init__()

    def package(self, source_path, package_path, base_product_name,
                compression_method=None):
        '''
        Description:
            Child classes overwrite this for specific implementations.
        '''
        raise NotImplementedError('Please implement the (package) method')


# ----------------------------------------------------------------------------
class TarPackager(Packager):
    '''
    Description:
        Provides the specifics for packaging using tar.  Including using
        compression.
    '''

    def __init__(self):
        super(TarPackager, self).__init__()

    def package(self, source_path, package_path, base_package_name,
                compression_method=None):
        '''
        Description:
            Finalize package location, name and input, then tar the package
            appropriatly.

        Inputs:
            See this modules package method below.

        Returns:
            See this modules package method below.
        '''

        full_base_package_name = os.path.join(package_path, base_product_name)

        write_mode = 'w'
        read_mode = 'r'
        full_package_path = '.'.join([base_package_name, 'tar'])
        if compression_method is not None:
            write_mode = ':'.join([write_mode, compression_method])
            read_mode = ':'.join([read_mode, compression_method])
            full_package_path = '.'.join([full_package_path,
                                          compression_method])

        # Change to the source directory
        current_directory = os.getcwd()
        os.chdir(source_directory)

        try:
            # Figure out the package contents
            package_source = glob.glob('*')

            # Write the tar package
            with tarfile.open(full_package_path, write_mode) as tar:
                for name in package_source:
                    tar.add(name)

            # Verify the tar package by reading the filenames from it
            with tarfile.open(full_package_path, read_mode) as tar:
                package_contents = tar.getnames():

            diff = list(set(package_source) - set(package_contents))
            if len(diff) > 0)
                msg = 'Package source and contents do not match'
                raise PackagingError(msg)

        except Exception as exception:
            raise PackagingError(exception)

        finally:
            # Change back to the previous directory
            os.chdir(current_directory)

        return (full_package_path)


# ----------------------------------------------------------------------------
class CheckSum(object):
    '''
    Description:
        Provides the base packager.
    '''

    def __init__(self):
        super(Packager, self).__init__()

    def checksum(self, full_package_path, package_path, base_package_name):
        '''
        Description:
            Generates a checksum file and returns the value.
        '''

        full_base_checksum_name = os.path.join(package_path, base_product_name)
        full_checksum_path = '.'.join([full_package_path, 'md5'])

        md5hash = hashlib.md5(open(full_package_path, 'rb').read()).hexdigest()

        file_content = '  '.join([md5hash,
                                  os.path.basename(full_package_path)])

        with open(full_checksum_path, 'w') as checksum_fd:
            checksum_fd.write(file_content)

        return md5hash


# ----------------------------------------------------------------------------
def package(source_path, package_path, base_package_name):
    '''
    Description:
        Provides a means to call the correct packager.  Only one is currently
        implemented.

    Inputs:
        source_path(str) - The path to a directory containing all the contents
                           to be included in the package.
        package_path(str) - The path to a directory where the package should
                            be built, in.
        base_package_name(str) - The unique base filename for the package.

    Returns:
        full_package_path(str) - The full path including filename for where
                                 the product was packaged to on the local file
                                 system.
        checksum(str) - The actual checksum value.
    '''

    try:
        full_package_path = TarPackager.package(source_path, package_path,
                                                base_package_name, 'gz')
    except Exception as exception:
        raise PackagingError(exception)

    try:
        checksum_value = CheckSum.checksum(full_package_path, package_path,
                                           base_package_name)
    except Exception as exception:
        raise PackagingError(exception)

    return (full_package_path, checksum_value)

