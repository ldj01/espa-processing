#! /usr/bin/env python

'''
    FILE: order_disposition_cron.py

    PURPOSE: Processes order finalization and email generation for accepted
             orders.

    PROJECT: Land Satellites Data Systems Science Research and Development
             (LSRD) at the USGS EROS

    LICENSE: NASA Open Source Agreement 1.3
'''

import os
import sys
import logging
import xmlrpclib


LOGGER_NAME = 'espa.cron.orderdisp'
LOGGER_FILENAME = '/tmp/espa-order-disposition-cron.log'


def determine_order_disposition():
    """Accomplishes order dispossition tasks

      Interact with the web service to accomplish order dispossition tasks
      along with sending the initial emails out to the users after their
      order has been accepted.
    """

    # Get the logger for this task
    logger = logging.getLogger(LOGGER_NAME)

    rpcurl = os.environ.get('ESPA_XMLRPC')
    server = None

    # Create a server object if the rpcurl seems valid
    if (rpcurl is not None and
            rpcurl.startswith('http://') and
            len(rpcurl) > 7):

        server = xmlrpclib.ServerProxy(rpcurl)
    else:
        raise Exception('Missing or invalid environment variable ESPA_XMLRPC')

    # Verify xmlrpc server
    if server is None:
        raise Exception('xmlrpc server was None... exiting')

    # Use order_disposition_enabled to determine if we should be processing
    # or not
    od_enabled = server.get_configuration('system.order_disposition_enabled')

    if not od_enabled.lower() == 'true':
        raise Exception('order disposition disabled... exiting')

    try:
        if not server.handle_orders():
            raise Exception('server.handle_orders() was not successful')

    except xmlrpclib.ProtocolError:
        logger.exception('A protocol error occurred')

    except Exception:
        logger.exception('An error occurred finalizing orders')

    finally:
        server = None


def main():
    """Execute the order disposition determination routine"""

    # Configure and get the logger for this task
    logging.basicConfig(format=('%(asctime)s.%(msecs)03d %(process)d'
                                ' %(levelname)-8s'
                                ' %(filename)s:%(lineno)d:'
                                '%(funcName)s -- %(message)s'),
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO,
                        filename=LOGGER_FILENAME)

    logger = logging.getLogger(LOGGER_NAME)

    # Check required variables that this script should fail on if they are not
    # defined
    required_vars = ['ESPA_XMLRPC']
    for env_var in required_vars:
        if (env_var not in os.environ or os.environ.get(env_var) is None or
                len(os.environ.get(env_var)) < 1):

            logger.critical('${0} is not defined... exiting'.format(env_var))
            sys.exit(1)  # EXIT_FAILURE

    try:
        determine_order_disposition()
    except Exception:
        logger.exception('Processing failed')
        sys.exit(1)  # EXIT_FAILURE

    sys.exit(0)  # EXIT_SUCCESS


if __name__ == '__main__':
    main()
