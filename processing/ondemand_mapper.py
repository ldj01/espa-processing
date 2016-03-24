#! /usr/bin/env python

'''
License:
  "NASA Open Source Agreement 1.3"

Description:
  Read all lines from STDIN and process them.

History:
  Created Jan/2014 by Ron Dilley, USGS/EROS

    Date              Programmer               Reason
    ----------------  ------------------------ -------------------------------
    Jan/2014          Ron Dilley               Initial implementation
    Sept/2014         Ron Dilley               Updated to use espa_common and
                                               our python logging setup
                                               Updated to use Hadoop
    Oct/2014          Ron Dilley               Renamed to ondemand and updated
                                               to perform all of our ondemand
                                               map operations
'''

import sys
import socket
import json
import xmlrpclib
from time import sleep
from argparse import ArgumentParser

# imports from espa_common
from logger_factory import EspaLogging
import settings
import sensor

# local objects and methods
import parameters
import processor


# ============================================================================
def set_product_error(server, order_id, product_id, processing_location):
    '''
    Description:
        Call the xmlrpc server routine to set a product request to error.
        Provides a sleep retry implementation to hopefully by-pass any errors
        encountered, so that we do not get requests that have failed, but
        show a status of processing.
    '''

    if server is not None:
        logger = EspaLogging.get_logger(settings.PROCESSING_LOGGER)

        attempt = 0
        sleep_seconds = settings.DEFAULT_SLEEP_SECONDS
        while True:
            try:
                # START - DEBUG
                if product_id is None:
                    logger.info("DEBUG: Product ID is [None]")
                else:
                    logger.info("DEBUG: Product ID is [%s]" % product_id)
                if order_id is None:
                    logger.info("DEBUG: Order ID is [None]")
                else:
                    logger.info("DEBUG: Order ID is [%s]" % order_id)
                if processing_location is None:
                    logger.info("DEBUG: Processing Location is [None]")
                else:
                    logger.info("DEBUG: Processing Location is [%s]"
                                % processing_location)
                # END - DEBUG

                logged_contents = \
                    EspaLogging.read_logger_file(settings.PROCESSING_LOGGER)

                status = server.set_scene_error(product_id, order_id,
                                                processing_location,
                                                logged_contents)

                if not status:
                    logger.critical("Failed processing xmlrpc call to"
                                    " set_scene_error")
                    return False

                break

            except Exception:
                logger.critical("Failed processing xmlrpc call to"
                                " set_scene_error")
                logger.exception("Exception encountered and follows")

                if attempt < settings.MAX_SET_SCENE_ERROR_ATTEMPTS:
                    sleep(sleep_seconds)  # sleep before trying again
                    attempt += 1
                    sleep_seconds = int(sleep_seconds * 1.5)
                    continue
                else:
                    return False
        # END - while True

    return True


# ============================================================================
def process(args):
    '''
    Description:
      Read all lines from STDIN and process them.  Each line is converted to
      a JSON dictionary of the parameters for processing.  Validation is
      performed on the JSON dictionary to test if valid for this mapper.
      After validation the generation of the products is performed.
    '''

    # Initially set to the base logger
    logger = EspaLogging.get_logger('base')

    processing_location = socket.gethostname()

    # Process each line from stdin
    for line in sys.stdin:
        if not line or len(line) < 1 or not line.strip().find('{') > -1:
            # this is how the nlineinputformat is supplying values:
            # 341104        {"orderid":
            # logger.info("BAD LINE:%s##" % line)
            continue
        else:
            # take the entry starting at the first opening parenth to the end
            line = line[line.find("{"):]
            line = line.strip()

        # Reset these for each line
        (server, order_id, product_id) = (None, None, None)

        # Default to the command line value
        mapper_keep_log = args.keep_log

        try:
            line = line.replace('#', '')
            parms = json.loads(line)

            if not parameters.test_for_parameter(parms, 'options'):
                raise ValueError("Error missing JSON 'options' record")

            # TODO scene will be replaced with product_id someday
            (order_id, product_id, product_type, options) = \
                (parms['orderid'], parms['scene'], parms['product_type'],
                 parms['options'])

            # Fix the orderid in-case it contains any single quotes
            # The processors can not handle single quotes in the email
            # portion due to usage in command lines.
            parms['orderid'] = order_id.replace("'", '')

            # If it is missing due to above TODO, then add it
            if not parameters.test_for_parameter(parms, 'product_id'):
                parms['product_id'] = product_id

            # Figure out if debug level logging was requested
            debug = False
            if parameters.test_for_parameter(options, 'debug'):
                debug = options['debug']

            # Configure and get the logger for this order request
            EspaLogging.configure(settings.PROCESSING_LOGGER, order=order_id,
                                  product=product_id, debug=debug)
            logger = EspaLogging.get_logger(settings.PROCESSING_LOGGER)

            # If the command line option is True don't use the scene option
            if not mapper_keep_log:
                if not parameters.test_for_parameter(options, 'keep_log'):
                    options['keep_log'] = False

                mapper_keep_log = options['keep_log']

            logger.info("Processing %s:%s" % (order_id, product_id))

            # Update the status in the database
            if parameters.test_for_parameter(parms, 'xmlrpcurl'):
                if parms['xmlrpcurl'] != 'skip_xmlrpc':
                    server = xmlrpclib.ServerProxy(parms['xmlrpcurl'],
                                                   allow_none=True)
                    if server is not None:
                        status = server.update_status(product_id, order_id,
                                                      processing_location,
                                                      'processing')
                        if not status:
                            logger.warning("Failed processing xmlrpc call"
                                           " to update_status to processing")

            if product_id != 'plot':
                # Make sure we can process the sensor
                tmp_inst = sensor.instance(product_id)
                del tmp_inst

                # Make sure we have a valid output format
                if not parameters.test_for_parameter(options, 'output_format'):
                    logger.warning("'output_format' parameter missing"
                                   " defaulting to envi")
                    options['output_format'] = 'envi'

                if (options['output_format']
                        not in parameters.VALID_OUTPUT_FORMATS):

                    raise ValueError("Invalid Output format %s"
                                     % options['output_format'])

            # ----------------------------------------------------------------
            # NOTE: The first thing the product processor does during
            #       initialization is validate the input parameters.
            # ----------------------------------------------------------------

            destination_product_file = 'ERROR'
            destination_cksum_file = 'ERROR'
            pp = None
            try:
                # All processors are implemented in the processor module
                pp = processor.get_instance(parms)
                (destination_product_file, destination_cksum_file) = \
                    pp.process()

            finally:
                # Free disk space to be nice to the whole system.
                if not mapper_keep_log and pp is not None:
                    pp.remove_product_directory()

            # Everything was successfull so mark the scene complete
            if server is not None:
                status = server.mark_scene_complete(product_id, order_id,
                                                    processing_location,
                                                    destination_product_file,
                                                    destination_cksum_file, "")
                if not status:
                    logger.warning("Failed processing xmlrpc call to"
                                   " mark_scene_complete")

            # Cleanup the log file
            if not mapper_keep_log:
                EspaLogging.delete_logger_file(settings.PROCESSING_LOGGER)

            # Reset back to the base logger
            logger = EspaLogging.get_logger('base')

        except Exception as excep:

            # First log the exception
            logger.exception("Exception encountered stacktrace follows")

            if server is not None:

                try:
                    status = set_product_error(server,
                                               order_id,
                                               product_id,
                                               processing_location)
                    if status and not mapper_keep_log:
                        try:
                            # Cleanup the log file
                            EspaLogging. \
                                delete_logger_file(settings.PROCESSING_LOGGER)
                        except Exception:
                            logger.exception("Exception encountered"
                                             " stacktrace follows")
                except Exception:
                    logger.exception("Exception encountered stacktrace"
                                     " follows")
    # END - for line in STDIN


# ============================================================================
if __name__ == '__main__':
    '''
    Description:
        Some parameter and logging setup, then call the process routine.
    '''

    # Grab our only command line parameter
    parser = ArgumentParser(
        description="Processes a list of scenes from stdin")
    parser.add_argument('--keep-log', action='store_true', dest='keep_log',
                        default=False, help="keep the generated log file")
    args = parser.parse_args()

    EspaLogging.configure_base_logger(filename='/tmp/espa-ondemand-mapper.log')
    # Initially set to the base logger
    logger = EspaLogging.get_logger('base')

    try:
        process(args)
    except Exception:
        logger.exception("Processing failed stacktrace follows")

    sys.exit(0)
