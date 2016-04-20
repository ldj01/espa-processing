#! /usr/bin/env python

'''
    FILE: ondemand_cron.py

    PURPOSE: Master script for new Hadoop jobs.  Queries the xmlrpc
             service to find requests that need to be processed and
             builds/executes a Hadoop job to process them.

    PROJECT: Land Satellites Data Systems Science Research and Development
             (LSRD) at the USGS EROS

    LICENSE: NASA Open Source Agreement 1.3
'''


import os
import sys
import logging
import json
import xmlrpclib
import urllib
import commands
from datetime import datetime
from argparse import ArgumentParser
from ConfigParser import ConfigParser
from functools import partial


LOGGER_NAME = 'espa.cron.ondemand'
CRON_CFG_FILENAME = 'cron.conf'
PROC_CFG_FILENAME = 'processing.conf'


def execute_cmd(cmd):
    """Execute a system command line

    Args:
        cmd (str): The command line to execute.

    Returns:
        output (str): The stdout and/or stderr from the executed command.

    Raises:
        Exception(message)
    """

    output = ''
    (status, output) = commands.getstatusoutput(cmd)

    message = ''
    if status < 0:
        message = 'Application terminated by signal [{0}]'.format(cmd)

    if status != 0:
        message = 'Application failed to execute [{0}]'.format(cmd)

    if os.WEXITSTATUS(status) != 0:
        message = ('Application [{0}] returned error code [{1}]'
                   .format(cmd, os.WEXITSTATUS(status)))

    if len(message) > 0:
        if len(output) > 0:
            # Add the output to the exception message
            message = ' Stdout/Stderr is: '.join([message, output])
        raise Exception(message)

    return output


def get_cfg_file_path(filename):
    """Build the full path to the config file

    Args:
        filename (str): The name of the file to append to the full path.

    Raises:
        Exception(message)
    """

    # Use the users home directory as the base source directory for
    # configuration
    if 'HOME' not in os.environ:
        raise Exception('[HOME] not found in environment')
    home_dir = os.environ.get('HOME')

    # Build the full path to the configuration file
    config_path = os.path.join(home_dir, '.usgs', 'espa', filename)

    return config_path


def retrieve_cron_cfg():
    """Retrieve the configuration for the cron

    Returns:
        cfg (ConfigParser): Configuration for ESPA cron.

    Raises:
        Exception(message)
    """

    # Build the full path to the configuration file
    config_path = get_cfg_file_path(CRON_CFG_FILENAME)

    if not os.path.isfile(config_path):
        raise Exception('Missing configuration file [{}]'.format(config_path))

    # Create the object and load the configuration
    cfg = ConfigParser()
    cfg.read(config_path)

    return cfg


def retrieve_proc_cfg():
    """Retrieve the configuration for the processing code

    Returns:
        cfg (ConfigParser): Configuration for ESPA.

    Raises:
        Exception(message)
    """

    # Build the full path to the configuration file
    config_path = get_cfg_file_path(PROC_CFG_FILENAME)

    if not os.path.isfile(config_path):
        raise Exception('Missing configuration file [{}]'.format(config_path))

    # Create the object and load the configuration
    cfg = ConfigParser()
    cfg.read(config_path)

    return cfg


def queue_keys(cfg):
    """Retrieve the sorted keys for the queue mapping

    Args:
        cfg (ConfigParser): Configuration for the ondemand cron.

    Returns:
        keys (list): A sorted list of the keys.
    """

    keys = [key for key, value in cfg.items('hadoop_queue_mapping')]

    return sorted(keys)


def get_queue_name(cfg, priority):
    """Retrieve the queue name for priority

    Args:
        cfg (ConfigParser): Configuration for the ESPA cron.
        priority (str): The priority of the queue to find.

    Returns:
        queue (str): The name of the queue for the priority.

    Raises:
        Exception(message)
    """

    for key, value in cfg.items('hadoop_queue_mapping'):
        if key == priority:
            return value

    raise Exception('priority [{}] not found in configuration'
                    .format(priority))


def gen_cmdenv_from_cfg(cfg, section, option):
    """Build a string suitable for the hadoop -cmdenv command line argument

    Args:
        cfg (ConfigParser): Configuration for the ESPA cron.
        section (str): The section for the option to find.
        option (str): The option to find.

    Returns:
        cmdenv (str): The command environment string required to setup the
                      environment.
    """

    return '{}={}'.format(option.upper(), cfg.get(section, option))


def process_requests(cron_cfg, proc_cfg, args,
                     queue_priority, request_priority):
    """Retrieves and kicks off processes

    Queries the xmlrpc service to see if there are any requests that need
    to be processed with the specified type, priority and/or user.  If there
    are, this method builds and executes a hadoop job and updates the status
    for each request through the xmlrpc service."

    Args:
        cron_cfg (ConfigParser): Configuration for ESPA cron.
        proc_cfg (ConfigParser): Configuration for ESPA processing.
        args (struct): The arguments retireved from the command line.
        queue_priority (str): The queue to use or None.
        request_priority (str): The request to use or None.

    Returns:
        Nothing is returned.

    Raises:
        Exception(message)
    """

    # Get the logger for this task
    logger = logging.getLogger(LOGGER_NAME)

    # check the number of hadoop jobs and don't do anything if they
    # are over a limit
    job_limit = cron_cfg.getint('hadoop', 'max_jobs')
    cmd = "hadoop job -list|awk '{print $1}'|grep -c job 2>/dev/null"
    try:
        job_count = execute_cmd(cmd)
    except Exception as e:
        errmsg = 'Stdout/Stderr is: 0'
        if errmsg in e.message:
            job_count = 0
        else:
            raise e

    if int(job_count) >= int(job_limit):
        logger.warn('Detected {0} Hadoop jobs running'.format(job_count))
        logger.warn('No additional jobs will be run until job count'
                    ' is below {0}'.format(job_limit))
        return

    rpcurl = proc_cfg.get('processing', 'espa_xmlrpc')
    server = None

    # Create a server object if the rpcurl seems valid
    if (rpcurl is not None and
            rpcurl.startswith('http://') and
            len(rpcurl) > 7):

        server = xmlrpclib.ServerProxy(rpcurl, allow_none=True)
    else:
        raise Exception('Missing or invalid XMLRPC URL')

    home_dir = os.environ.get('HOME')
    hadoop_executable = os.path.join(home_dir, 'bin/hadoop/bin/hadoop')

    # Verify xmlrpc server
    if server is None:
        raise Exception('xmlrpc server was None... exiting')

    user = server.get_configuration('landsatds.username')
    if len(user) == 0:
        raise Exception('landsatds.username is not defined... exiting')

    password = urllib.quote(server.get_configuration('landsatds.password'))
    if len(password) == 0:
        raise Exception('landsatds.password is not defined... exiting')

    host = server.get_configuration('landsatds.host')
    if len(host) == 0:
        raise Exception('landsatds.host is not defined... exiting')

    # Use ondemand_enabled to determine if we should be processing or not
    ondemand_enabled = server.get_configuration('system.ondemand_enabled')

    # Determine the appropriate hadoop queue to use
    hadoop_job_queue = get_queue_name(cron_cfg, queue_priority)

    if not ondemand_enabled.lower() == 'true':
        raise Exception('on demand disabled... exiting')

    # Create a partial function to reduce duplication in some of the
    # following code
    proc_cmdenv = partial(gen_cmdenv_from_cfg,
                          cfg=proc_cfg, section='processing')

    try:
        logger.info('Checking for requests to process...')
        requests = server.get_scenes_to_process(int(args.limit), args.user,
                                                request_priority,
                                                list(args.product_types))
        if requests:
            # Figure out the name of the order file
            stamp = datetime.now()
            job_name = ('%s_%s_%s_%s_%s_%s-%s-espa_job'
                        % (str(stamp.month), str(stamp.day),
                           str(stamp.year), str(stamp.hour),
                           str(stamp.minute), str(stamp.second),
                           str(queue_priority)))

            logger.info(' '.join(['Found requests to process,',
                                  'generating job name:', job_name]))

            job_filename = '{0}.txt'.format(job_name)
            job_filepath = os.path.join('/tmp', job_filename)

            # Create the order file full of all the scenes requested
            with open(job_filepath, 'w+') as espa_fd:
                for request in requests:
                    request['xmlrpcurl'] = rpcurl

                    # Log the request before passwords are added
                    line_entry = json.dumps(request)
                    logger.info(line_entry)

                    # Add the usernames and passwords to the options
                    request['options']['source_username'] = user
                    request['options']['destination_username'] = user
                    request['options']['source_pw'] = password
                    request['options']['destination_pw'] = password

                    # Need to refresh since we added password stuff that
                    # could not be logged
                    line_entry = json.dumps(request)

                    # Split the jobs using newline's
                    request_line = ''.join([line_entry, '\n'])

                    # Write out the request line
                    espa_fd.write(request_line)

            # Specify the location of the order file on the hdfs
            hdfs_target = os.path.join('requests', job_filename)

            # Define command line to store the job file in hdfs
            hadoop_store_command = [hadoop_executable, 'dfs',
                                    '-copyFromLocal', job_filepath,
                                    hdfs_target]

            jars_path = os.path.join(home_dir, 'bin/hadoop/contrib/streaming',
                                     'hadoop-streaming*.jar')

            code_dir = os.path.join(home_dir, 'espa-site/processing')
            common_dir = os.path.join(home_dir, 'espa-site/espa_common')

            # Specify the mapper application
            mapper_path = os.path.join(code_dir, 'ondemand_mapper.py')

            # Define command line to execute the hadoop job
            # Be careful it is possible to have conflicts between module names
            hadoop_run_command = \
                [hadoop_executable, 'jar', jars_path,
                 '-D', ('mapred.task.timeout={0}'
                        .format(cron_cfg.getint('hadoop', 'timeout'))),
                 '-D', 'mapred.reduce.tasks=0',
                 '-D', 'mapred.job.queue.name={0}'.format(hadoop_job_queue),
                 '-D', 'mapred.job.name="{0}"'.format(job_name),
                 '-inputformat', ('org.apache.hadoop.mapred.'
                                  'lib.NLineInputFormat'),
                 '-file', mapper_path,
                 '-file', os.path.join(code_dir, 'distribution.py'),
                 '-file', os.path.join(code_dir, 'environment.py'),
                 '-file', os.path.join(code_dir, 'espa_exception.py'),
                 '-file', os.path.join(code_dir, 'metadata.py'),
                 '-file', os.path.join(code_dir, 'initialization.py'),
                 '-file', os.path.join(code_dir, 'parameters.py'),
                 '-file', os.path.join(code_dir, 'processor.py'),
                 '-file', os.path.join(code_dir, 'sensor.py'),
                 '-file', os.path.join(code_dir, 'staging.py'),
                 '-file', os.path.join(code_dir, 'statistics.py'),
                 '-file', os.path.join(code_dir, 'settings.py'),
                 '-file', os.path.join(code_dir, 'transfer.py'),
                 '-file', os.path.join(code_dir, 'utilities.py'),
                 '-file', os.path.join(code_dir, 'warp.py'),
                 '-file', os.path.join(common_dir, 'logger_factory.py'),
                 '-file', get_cfg_file_path(PROC_CFG_FILENAME),
                 '-mapper', mapper_path,
                 '-cmdenv', proc_cmdenv(option='espa_work_dir'),
                 '-cmdenv', proc_cmdenv(option='espa_distribution_method'),
                 '-cmdenv', proc_cmdenv(option='espa_distribution_dir'),
                 '-cmdenv', proc_cmdenv(option='espa_schema'),
                 '-cmdenv', proc_cmdenv(option='espa_land_mass_polygon'),
                 '-cmdenv', proc_cmdenv(option='espa_xmlrpc'),
                 '-cmdenv', proc_cmdenv(option='espa_cache_host_list'),
                 '-cmdenv', proc_cmdenv(option='espa_elevation_dir'),
                 '-cmdenv', proc_cmdenv(option='ias_data_dir'),
                 '-cmdenv', proc_cmdenv(option='pythonpath'),
                 '-cmdenv', proc_cmdenv(option='ledaps_aux_dir'),
                 '-cmdenv', proc_cmdenv(option='l8_aux_dir'),
                 '-cmdenv', proc_cmdenv(option='esun'),
                 '-cmdenv', proc_cmdenv(option='lst_aux_dir'),
                 '-cmdenv', proc_cmdenv(option='lst_data_dir'),
                 '-cmdenv', proc_cmdenv(option='modtran_path'),
                 '-cmdenv', proc_cmdenv(option='modtran_data_dir'),
                 '-cmdenv', proc_cmdenv(option='aster_ged_server_name'),
                 '-input', hdfs_target,
                 '-output', hdfs_target + '-out']

            # Define the executables to clean up hdfs
            hadoop_delete_request_command1 = [hadoop_executable, 'dfs',
                                              '-rmr', hdfs_target]
            hadoop_delete_request_command2 = [hadoop_executable, 'dfs',
                                              '-rmr', hdfs_target + '-out']

            logger.info('Storing request file to hdfs...')
            output = ''
            try:
                cmd = ' '.join(hadoop_store_command)
                logger.info('Store cmd:{0}'.format(cmd))

                output = execute_cmd(cmd)
            except Exception:
                msg = 'Error storing files to HDFS... exiting'
                raise Exception(msg)
            finally:
                if len(output) > 0:
                    logger.info(output)

                logger.info('Deleting local request file copy [{0}]'
                            .format(job_filepath))
                os.unlink(job_filepath)

            try:
                # Update the scene list as queued so they don't get pulled
                # down again now that these jobs have been stored in hdfs
                product_list = list()
                for request in requests:
                    product_list.append((request['orderid'],
                                         request['scene']))

                    logger.info('Adding scene:{0} orderid:{1} to queued list'
                                .format(request['scene'], request['orderid']))

                server.queue_products(product_list, 'CDR_ECV cron driver',
                                      job_name)

                logger.info('Running hadoop job...')
                output = ''
                try:
                    cmd = ' '.join(hadoop_run_command)
                    logger.info('Run cmd:{0}'.format(cmd))

                    output = execute_cmd(cmd)
                except Exception:
                    logger.exception('Error running Hadoop job...')
                finally:
                    if len(output) > 0:
                        logger.info(output)

            finally:
                logger.info('Deleting hadoop job request file from hdfs....')
                output = ''
                try:
                    cmd = ' '.join(hadoop_delete_request_command1)
                    output = execute_cmd(cmd)
                except Exception:
                    logger.exception("Error deleting hadoop job request file")
                finally:
                    if len(output) > 0:
                        logger.info(output)

                logger.info('Deleting hadoop job output...')
                output = ''
                try:
                    cmd = ' '.join(hadoop_delete_request_command2)
                    output = execute_cmd(cmd)
                except Exception:
                    logger.exception('Error deleting hadoop job output')
                finally:
                    if len(output) > 0:
                        logger.info(output)

        else:
            logger.info('No requests to process....')

    except xmlrpclib.ProtocolError:
        logger.exception('A protocol error occurred')

    except Exception:
        logger.exception('Error Processing Ondemand Requests')

    finally:
        server = None


def main():
    """Execute the core processing routine"""

    cron_cfg = retrieve_cron_cfg()
    proc_cfg = retrieve_proc_cfg()

    # Create a command line argument parser
    description = ('Builds and kicks-off hadoop jobs for the espa processing'
                   ' system (to process product requests)')
    parser = ArgumentParser(description=description)

    # Add parameters
    valid_priorities = queue_keys(cron_cfg)
    valid_product_types = ['landsat', 'modis', 'plot']

    parser.add_argument('--priority',
                        action='store', dest='priority', required=True,
                        choices=valid_priorities,
                        help='only process requests with this priority:'
                             ' one of [{0}]'
                             .format(', '.join(valid_priorities)))

    parser.add_argument('--product-types',
                        action='store', dest='product_types', required=True,
                        nargs='+', metavar='PRODUCT_TYPE',
                        help=('only process requests for the specified'
                              ' product type(s)'))

    parser.add_argument('--limit',
                        action='store', dest='limit', required=False,
                        default='500',
                        help='specify the max number of requests to process')

    parser.add_argument('--user',
                        action='store', dest='user', required=False,
                        default=None,
                        help='only process requests for the specified user')

    # Parse the command line arguments
    args = parser.parse_args()

    # Validate product_types
    if ((set(['landsat', 'plot']) == set(args.product_types)) or
            (set(['modis', 'plot']) == set(args.product_types)) or
            (set(['landsat', 'modis', 'plot']) == set(args.product_types))):
        print('Invalid --product-types: [plot] cannot be combined with any'
              ' other product types')
        sys.exit(1)  # EXIT_FAILURE

    # Configure and get the logger for this task
    logger_filename = cron_cfg.get('logging', 'log_filename')
    if 'plot' in args.product_types:
        logger_filename = cron_cfg.get('logging', 'plot_log_filename')

    logger_format = ('%(asctime)s.%(msecs)03d %(process)d'
                     ' %(levelname)-8s {0:>6}'
                     ' %(filename)s:%(lineno)d:%(funcName)s'
                     ' -- %(message)s'.format(args.priority.lower()))

    # Setup the default logger format and level.  Log to STDOUT.
    logging.basicConfig(format=logger_format,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO,
                        filename=logger_filename)

    logger = logging.getLogger(LOGGER_NAME)

    # Determine the appropriate priority value to use for the queue and request
    queue_priority = args.priority.lower()
    request_priority = queue_priority
    if 'plot' in args.product_types:
        if queue_priority == 'all':
            # If all was specified default to high queue
            queue_priority = 'high'
        # The request priority is always None for plotting to get all of them
        request_priority = None
    else:
        if request_priority == 'all':
            # We need to use a value of None to get all of them
            request_priority = None

    # Setup and submit products to hadoop for processing
    try:
        process_requests(cron_cfg, proc_cfg, args,
                         queue_priority, request_priority)
    except Exception:
        logger.exception('Processing failed')
        sys.exit(1)  # EXIT_FAILURE

    sys.exit(0)  # EXIT_SUCCESS


if __name__ == '__main__':
    main()
