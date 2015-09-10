
'''
License:
  "NASA Open Source Agreement 1.3"

Description:
  Provides the implementation for creating the core directories required
  for the processing of a product request.

History:
  Created Oct/2014 by Ron Dilley, USGS/EROS

    Date              Reason
    ----------------  --------------------------------------------------------
    May/2015          Initial implementation completed
    Sep/2015          Reduced complexity based on peer review comments

'''


import os


import utilities
from environment import Environment, DISTRIBUTION_METHOD_LOCAL


# ----------------------------------------------------------------------------
def __create_local_directory(base_path, directory_name):
    '''
    Description:
        Creates a local directory under the base path.

    Note: "local" in this case means a standard directory.

    Returns:
        string: The fullpath to the directory created.

    Parameters:
        string: base_path - The location where to create the directory.
        string: directory_name - The name of the directory to be created.
    '''

    full_path = os.path.join(base_path, directory_name)

    utilities.create_directory(full_path)

    return full_path


# ----------------------------------------------------------------------------
def __create_linked_directory(base_path, linked_path, link_name):
    '''
    Description:
        Creates a link to the linked path

    Note: "linked" in this case means a symbolic link to the linked path.

    Returns:
        string: The fullpath to the link.

    Parameters:
        string: base_path - The location where to create the directory.
        string: linked_path - The location where the link will point.
        string: link_name - The name of the link to be created.
    '''

    full_path = os.path.join(base_path, link_name)

    utilities.create_link(linked_path, full_path)

    return full_path


# ============================================================================
# API Implementation
# ============================================================================

# ----------------------------------------------------------------------------
def create_stage_directory(base_path):
    '''
    Description:
        Creates a local stage directory.

    Note: "local" in this case means a standard directory.

    Returns:
        string: The fullpath to the "stage" directory.

    Parameters:
        string: base_path - The location where to create the directory.
    '''

    return __create_local_directory(base_path, 'stage')


# ----------------------------------------------------------------------------
def create_work_directory(base_path):
    '''
    Description:
        Creates a local work directory.

    Note: "local" in this case means a standard directory.

    Returns:
        string: The fullpath to the "work" directory.

    Parameters:
        string: base_path - The location where to create the directory.
    '''

    return __create_local_directory(base_path, 'work')


# ----------------------------------------------------------------------------
def create_output_directory(base_path):
    '''
    Description:
        Creates either a symbolic link to the online cache or a local
        directory.

    Note: With the local distribution method, a symbolic link is created so
          that we can just tar.gz the product and place the checksum directly
          on the product (online) cache.
          With the remote distribution method, we just create a directory to
          hold the tar.gz and checksum before using ftp/scp to transfer the
          product over the network.

    Returns:
        string: The fullpath to the "output" link or directory.

    Parameters:
        base_path - The location where to create the "output" link or
                    directory under.
    '''

    env = Environment()

    distribution_method = env.get_distribution_method()
    name = 'output'

    if distribution_method == DISTRIBUTION_METHOD_LOCAL:
        linked_path = env.get_distribution_directory()
        return __create_linked_directory(base_path, linked_path, name)
    else:
        return __create_local_directory(base_path, name)
