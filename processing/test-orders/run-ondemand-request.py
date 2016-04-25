#! /usr/bin/env python

'''
  DESCRIPTION: Execute test orders using the local environment.

  LICENSE: NASA Open Source Agreement 1.3
'''


import os
import sys
import socket
import logging
import datetime
import json
from argparse import ArgumentParser
from ConfigParser import ConfigParser

import sensor
import utilities


DAAC_HOSTNAME = 'e4ftl01.cr.usgs.gov'


def build_argument_parser():
    """Build the command line argument parser
    """

    # Create a command line argument parser
    description = 'Configures and executes a test order'
    parser = ArgumentParser(description=description)

    # Add parameters
    parser.add_argument('--request',
                        action='store', dest='request', required=True,
                        help='request to process')

    parser.add_argument('--master',
                        action='store_true', dest='master', default=False,
                        help='use the master products file')

    parser.add_argument('--plot',
                        action='store_true', dest='plot', default=False,
                        help='generate plots')

    parser.add_argument('--pre',
                        action='store_true', dest='pre', default=False,
                        help='use a -PRE order suffix')

    parser.add_argument('--post',
                        action='store_true', dest='post', default=False,
                        help='use a -POST order suffix')

    parser.add_argument('--include_dswe',
                        action='store_true', dest='include_dswe',
                        default=False,
                        help='include DSWE processing')

    parser.add_argument('--include_lst',
                        action='store_true', dest='include_lst',
                        default=False,
                        help='include LST processing')

    return parser


def get_satellite_sensor_code(product_id):
    """Returns the satellite-sensor code if known

    Args:
        product_id (str): The Product ID for the requested product.  Can also
                          be a filename with the assumption that the Product
                          ID is prefixed on the filename.
    """

    three_digit_prefixes = [sensor.LT4_SENSOR_CODE,
                            sensor.LT5_SENSOR_CODE,
                            sensor.LE7_SENSOR_CODE,
                            sensor.LT8_SENSOR_CODE,
                            sensor.LC8_SENSOR_CODE,
                            sensor.LO8_SENSOR_CODE,
                            sensor.TERRA_SENSOR_CODE,
                            sensor.AQUA_SENSOR_CODE]

    four_digit_prefixes = [sensor.LT04_SENSOR_CODE,
                           sensor.LT05_SENSOR_CODE,
                           sensor.LE07_SENSOR_CODE,
                           sensor.LT08_SENSOR_CODE,
                           sensor.LC08_SENSOR_CODE,
                           sensor.LO08_SENSOR_CODE,
                           'PLOT']

    # For older Landsat processing, and MODIS data, the Sensor Code is
    # the first 3 characters of the Scene ID
    satellite_sensor_code = product_id[0:3].upper()
    if satellite_sensor_code in three_digit_prefixes:
        return satellite_sensor_code

    # For collection based processing, the Sensor Code is the first 4
    # characters of the Scene Id
    satellite_sensor_code = product_id[0:4].upper()
    if satellite_sensor_code in four_digit_prefixes:
        return satellite_sensor_code

    # We could not determine what the Sesnor Code should be
    raise NotImplementedError('Unsupported Sensor Code [{0}] or [{1}]'
                              .format(product_id[0:3], product_id[0:4]))


def process_test_order(args, request_file, products_file, env_vars):
    """Process the test order file
    """

    logger = logging.getLogger(__name__)

    template_file = 'template.json'
    template_dict = None

    order_id = args.request

    if args.pre:
        order_id = ''.join([order_id, '-PRE'])

    if args.post:
        order_id = ''.join([order_id, '-POST'])

    have_error = False
    status = True
    error_msg = ''

    products = list()
    if not args.plot:
        with open(products_file, 'r') as scenes_fd:
            while (1):
                product = scenes_fd.readline().strip()
                if not product:
                    break
                products.append(product)
    else:
        products = ['plot']

    logger.info('Processing Products [{0}]'.format(', '.join(products)))

    with open(template_file, 'r') as template_fd:
        template_contents = template_fd.read()
        if not template_contents:
            raise Exception('Template file [{0}] is empty'
                            .format(template_file))

        template_dict = json.loads(template_contents)
        if template_dict is None:
            logger.error('Loading template.json')

    for product_id in products:
        logger.info('Processing Product [{0}]'.format(product_id))

        tmp_order = 'test-{0}-{1}'.format(order_id, product_id)

        with open(request_file, 'r') as request_fd:
            request_contents = request_fd.read()
            if not request_contents:
                raise Exception('Order file [{0}] is empty'
                                .format(request_file))

            logger.info('Processing Request File [{0}]'.format(request_file))

            request_dict = json.loads(request_contents)
            if request_dict is None:
                logger.error('Loading [{0}]'.format(request_file))

            # Merge the requested options with the template options, to create
            # a new dict with the requested options overriding the template.
            new_dict = template_dict.copy()
            new_dict.update(request_dict)
            new_dict['options'] = template_dict['options'].copy()
            new_dict['options'].update(request_dict['options'])

            # Turn it into a string for follow-on processing
            order_contents = json.dumps(new_dict, indent=4, sort_keys=True)

            sensor_code = get_satellite_sensor_code(product_id)

            with open(tmp_order, 'w') as tmp_fd:

                logger.info('Creating [{0}]'.format(tmp_order))

                tmp_line = order_contents

                # Update the order for the developer
                download_url = 'null'

                # for plots
                if not sensor.is_modis(product_id) and not args.plot:
                    product_path = ('{0}/{1}/{2}{3}'
                                    .format(env_vars['dev_data_dir']['value'],
                                            sensor_code, product_id,
                                            '.tar.gz'))

                    logger.info('Using Product Path [{0}]'
                                .format(product_path))
                    if not os.path.isfile(product_path):
                        error_msg = ('Missing product data [{0}]'
                                     .format(product_path))
                        have_error = True
                        break

                    download_url = 'file://{0}'.format(product_path)

                elif not args.plot:
                    if sensor.is_terra(product_id):
                        base_source_path = '/MOLT'
                    else:
                        base_source_path = '/MOLA'

                    parts = product_id.split('.')
                    short_name = parts[0]
                    version = parts[3]
                    date_YYYYDDD = parts[1][1:]
                    date_acquired = datetime.datetime.strptime(date_YYYYDDD,
                                                               '%Y%j').date()

                    xxx = ('{0}.{1}.{2}'
                           .format(str(date_acquired.year).zfill(4),
                                   str(date_acquired.month).zfill(2),
                                   str(date_acquired.day).zfill(2)))

                    product_path = ('{0}/{1}.{2}/{3}'
                                    .format(base_source_path, short_name,
                                            version, xxx))

                    if sensor.is_modis(product_id):
                        download_url = ('http://{0}/{1}/{2}.hdf'
                                        .format(DAAC_HOSTNAME, product_path,
                                                product_id))

                sensor_name = 'plot'
                if not args.plot:
                    sensor_name = sensor.info(product_id).sensor_name
                    logger.info('Processing Sensor [{0}]'.format(sensor_name))
                else:
                    logger.info('Processing Plot Request')

                tmp_line = tmp_line.replace('\n', '')
                tmp_line = tmp_line.replace('ORDER_ID', order_id)
                tmp_line = tmp_line.replace('SCENE_ID', product_id)

                if sensor_name in ['tm', 'etm', 'olitirs']:
                    tmp_line = tmp_line.replace('PRODUCT_TYPE', 'landsat')
                elif sensor_name in ['terra', 'aqua']:
                    tmp_line = tmp_line.replace('PRODUCT_TYPE', 'modis')
                else:
                    tmp_line = tmp_line.replace('PRODUCT_TYPE', 'plot')

                tmp_line = tmp_line.replace('DOWNLOAD_URL', download_url)

                tmp_fd.write(tmp_line)

                # Validate again, since we modified it
                parms = json.loads(tmp_line)
                print(json.dumps(parms, indent=4, sort_keys=True))

        if have_error:
            logger.error(error_msg)
            return False

        cmd = ('cd ..; cat test-orders/{0} | ./ondemand_mapper.py --developer'
               .format(tmp_order))

        output = ''
        try:
            logger.info('Processing [{0}]'.format(cmd))
            output = utilities.execute_cmd(cmd)
            if len(output) > 0:
                print output
        except Exception, e:
            logger.exception('Processing failed')
            status = False

        os.unlink(tmp_order)

    return status


def export_environment_variables(cfg):
    """Export the configuration to environment variables
    """

    for key, value in cfg.items('processing'):
        os.environ[key.upper()] = value


def main():
    """Main code for executing a test order
    """

    logging.basicConfig(format=('%(asctime)s.%(msecs)03d %(process)d'
                                ' %(levelname)-8s'
                                ' %(filename)s:%(lineno)d:%(funcName)s'
                                ' -- %(message)s'),
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    logger = logging.getLogger(__name__)

    # Build the command line argument parser
    parser = build_argument_parser()

    # Load up the environment variables from the processing configuration
    cfg = ConfigParser()
    cfg.read('processing.conf')

    export_environment_variables(cfg)

    env_vars = dict()
    env_vars = {'dev_data_dir': {'name': 'DEV_DATA_DIRECTORY',
                                 'value': None}}

    missing_environment_variable = False
    for var in env_vars:
        env_vars[var]['value'] = os.environ.get(env_vars[var]['name'])

        if env_vars[var]['value'] is None:
            logger.warning('Missing environment variable [{0}]'
                           .format(env_vars[var]['name']))
            missing_environment_variable = True

    # Terminate if missing environment variables
    if missing_environment_variable:
        logger.critical('Please fix missing environment variables')
        sys.exit(1)  # EXIT_FAILURE

    # Parse the command line arguments
    args = parser.parse_args()

    request_file = os.path.join(args.request, 'order.json')
    if not os.path.isfile(request_file):
        logger.critical('Request file [{0}] does not exist'
                        .format(request_file))
        sys.exit(1)  # EXIT_FAILURE

    products_file = None
    if not args.plot:
        products_file = os.path.join(args.request, 'order.products')

        if args.master:
            # Use the master file instead
            products_file = os.path.join(args.request, 'master.products')

        if not os.path.isfile(products_file):
            logger.critical('No products file exists for [{0}]'
                            .format(args.request))
            sys.exit(1)  # EXIT_FAILURE

    # Avoid the creation of the *.pyc files
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

    if not process_test_order(args, request_file, products_file, env_vars):
        logger.critical('Request [{0}] failed to process'
                        .format(args.request))
        sys.exit(1)  # EXIT_FAILURE

    sys.exit(0)  # EXIT_SUCCESS


if __name__ == '__main__':
    main()
