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


from config_utils import get_cfg_file_path, retrieve_cfg


LOGGER_NAME = 'espa.cron.orderdisp'
CRON_CFG_FILENAME = 'cron.conf'
PROC_CFG_FILENAME = 'processing.conf'


def determine_order_disposition(proc_cfg):
    """Accomplishes order dispossition tasks

      Interact with the web service to accomplish order dispossition tasks
      along with sending the initial emails out to the users after their
      order has been accepted.
    """

    # Get the logger for this task
    logger = logging.getLogger(LOGGER_NAME)

    rpcurl = proc_cfg.get('processing', 'espa_xmlrpc')
    server = None

    # Create a server object if the rpcurl seems valid
    if (rpcurl is not None and
            rpcurl.startswith('http://') and
            len(rpcurl) > 7):

        server = xmlrpclib.ServerProxy(rpcurl)
    else:
        raise Exception('Missing or invalid XMLRPC URL')

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

    cron_cfg = retrieve_cfg(CRON_CFG_FILENAME)
    proc_cfg = retrieve_cfg(PROC_CFG_FILENAME)

    # Configure and get the logger for this task
    logger_filename = cron_cfg.get('logging', 'disposition_log_filename')

    # Configure and get the logger for this task
    logging.basicConfig(format=('%(asctime)s.%(msecs)03d %(process)d'
                                ' %(levelname)-8s'
                                ' %(filename)s:%(lineno)d:'
                                '%(funcName)s -- %(message)s'),
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO,
                        filename=logger_filename)

    logger = logging.getLogger(LOGGER_NAME)

    try:
        determine_order_disposition(proc_cfg)
    except Exception:
        logger.exception('Processing failed')
        sys.exit(1)  # EXIT_FAILURE

    sys.exit(0)  # EXIT_SUCCESS


if __name__ == '__main__':
    main()
