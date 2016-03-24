
'''
License:
  "NASA Open Source Agreement 1.3"

Description:
  Provides routines for interfacing with parameters in a dictionary.

History:
  Created Jan/2014 by Ron Dilley, USGS/EROS
'''

import os

# imports from espa_common
from logger_factory import EspaLogging
import settings


import sensor


# This contains the valid sensors and data types which are supported
valid_output_formats = ['envi', 'envi-bip', 'gtiff', 'hdf-eos2']


# ============================================================================
def add_work_directory_parameter(parser):
    '''
    Description:
      Adds the work_directory parameter to the command line parameters
    '''

    parser.add_argument('--work_directory',
                        action='store', dest='work_directory',
                        default=os.curdir,
                        help="work directory on the localhost")


# ============================================================================
def add_debug_parameter(parser):
    '''
    Description:
      Adds the debug parameter to the command line parameters
    '''

    parser.add_argument('--debug',
                        action='store_true', dest='debug', default=False,
                        help="turn debug logging on")


# ============================================================================
def add_reprojection_parameters(parser, projection_values, ns_values,
                                pixel_size_units, image_extents_units,
                                resample_methods, datum_values):
    '''
    Description:
      Adds the reprojection parameters to the command line parameters
    '''

    parser.add_argument('--projection',
                        action='store', dest='projection', default=None,
                        help="proj.4 string for desired output product"
                             " projection")

    parser.add_argument('--reproject',
                        action='store_true', dest='reproject', default=False,
                        help="perform reprojection on the products")

    parser.add_argument('--target_projection',
                        action='store', dest='target_projection',
                        choices=projection_values,
                        help="one of (%s)" % ', '.join(projection_values))

    parser.add_argument('--utm_zone',
                        action='store', dest='utm_zone',
                        help="UTM zone to use")
    parser.add_argument('--utm_north_south',
                        action='store', dest='utm_north_south',
                        choices=ns_values,
                        help="one of (%s)" % ', '.join(ns_values))

    # Default to the first entry which should be WGS84
    parser.add_argument('--datum',
                        action='store', dest='datum', default=datum_values[0],
                        help=("one of (%s), only used with albers projection"
                              % ', '.join(datum_values)))

    parser.add_argument('--longitude_pole',
                        action='store', dest='longitude_pole',
                        help="longitude of the pole projection parameter")

    parser.add_argument('--latitude_true_scale',
                        action='store', dest='latitude_true_scale',
                        help="latitude true of scale projection parameter")

    parser.add_argument('--origin_lat',
                        action='store', dest='origin_lat',
                        help="origin of latitude projection parameter")

    parser.add_argument('--central_meridian',
                        action='store', dest='central_meridian',
                        help="central meridian projection parameter")

    parser.add_argument('--std_parallel_1',
                        action='store', dest='std_parallel_1',
                        help="first standard parallel projection parameter")
    parser.add_argument('--std_parallel_2',
                        action='store', dest='std_parallel_2',
                        help="second standard parallel projection parameter")

    parser.add_argument('--false_northing',
                        action='store', dest='false_northing',
                        help="false northing projection parameter")
    parser.add_argument('--false_easting',
                        action='store', dest='false_easting',
                        help="false easting projection parameter")

    parser.add_argument('--resize',
                        action='store_true', dest='resize', default=False,
                        help="perform resizing of the pixels on the products")
    parser.add_argument('--pixel_size',
                        action='store', dest='pixel_size',
                        help="desired pixel size for output products")
    parser.add_argument('--pixel_size_units',
                        action='store', dest='pixel_size_units',
                        choices=pixel_size_units,
                        help=("units pixel size is specified in: one of (%s)"
                              % ', '.join(pixel_size_units)))

    parser.add_argument('--image_extents',
                        action='store_true', dest='image_extents',
                        default=False,
                        help="specify desired output image extents")
    parser.add_argument('--image_extents_units',
                        action='store', dest='image_extents_units',
                        choices=pixel_size_units,
                        help=("units image extents are specified in:"
                              " one of (%s)"
                              % ', '.join(image_extents_units)))

    parser.add_argument('--minx',
                        action='store', dest='minx',
                        help="minimum X for the image extent")
    parser.add_argument('--miny',
                        action='store', dest='miny',
                        help="minimum Y for the image extent")
    parser.add_argument('--maxx',
                        action='store', dest='maxx',
                        help="maximum X for the image extent")
    parser.add_argument('--maxy',
                        action='store', dest='maxy',
                        help="maximum Y for the image extent")

    parser.add_argument('--resample_method',
                        action='store', dest='resample_method', default='near',
                        choices=resample_methods,
                        help="one of (%s)" % ', '.join(resample_methods))


# ============================================================================
def test_for_parameter(parms, key):
    '''
    Description:
      Tests to see if a specific parameter is present.

    Returns:
       True - If the parameter is present in the dictionary
      False - If the parameter is *NOT* present in the dictionary or does not
              have a value
    '''

    if (key not in parms) or (parms[key] == '') or (parms[key] is None):
        return False

    return True


# ============================================================================
def validate_reprojection_parameters(parms, scene, projections, ns_values,
                                     pixel_size_units, image_extents_units,
                                     resample_methods, datum_values):
    '''
    Description:
      Perform a check on the possible reprojection parameters

    Note:
      We blindly convert values to float or int without checking them.  It is
      assumed that the web tier has validated them.
    '''

    logger = EspaLogging.get_logger(settings.PROCESSING_LOGGER)

    # Create this and set to None if not present
    if not test_for_parameter(parms, 'projection'):
        logger.warning("'projection' parameter missing defaulting to None")
        parms['projection'] = None

    # Create this and set to 'near' if not present
    if not test_for_parameter(parms, 'resample_method'):
        logger.warning("'resample_method' parameter missing defaulting to"
                       " near")
        parms['resample_method'] = 'near'

    # Make sure these have at least a False value
    required_parameters = ['reproject', 'image_extents', 'resize']

    for parameter in required_parameters:
        if not test_for_parameter(parms, parameter):
            logger.warning("'%s' parameter missing defaulting to False"
                           % parameter)
            parms[parameter] = False

    if parms['reproject']:
        if not test_for_parameter(parms, 'target_projection'):
            raise RuntimeError("Missing target_projection parameter")
        else:
            # Convert to lower case
            target_projection = parms['target_projection'].lower()
            parms['target_projection'] = target_projection

            # Verify a valid projection
            if target_projection not in projections:
                raise ValueError("Invalid target_projection [%s]:"
                                 " Argument must be one of (%s)"
                                 % (target_projection, ', '.join(projections)))

            # ................................................................
            if target_projection == "sinu":
                if not test_for_parameter(parms, 'central_meridian'):
                    raise RuntimeError("Missing central_meridian parameter")
                else:
                    parms['central_meridian'] = \
                        float(parms['central_meridian'])
                if not test_for_parameter(parms, 'false_easting'):
                    raise RuntimeError("Missing false_easting parameter")
                else:
                    parms['false_easting'] = float(parms['false_easting'])
                if not test_for_parameter(parms, 'false_northing'):
                    raise RuntimeError("Missing false_northing parameter")
                else:
                    parms['false_northing'] = float(parms['false_northing'])

                if not test_for_parameter(parms, 'datum'):
                    parms['datum'] = None

            # ................................................................
            if target_projection == 'aea':
                if not test_for_parameter(parms, 'std_parallel_1'):
                    raise RuntimeError("Missing std_parallel_1 parameter")
                else:
                    parms['std_parallel_1'] = float(parms['std_parallel_1'])
                if not test_for_parameter(parms, 'std_parallel_2'):
                    raise RuntimeError("Missing std_parallel_2 parameter")
                else:
                    parms['std_parallel_2'] = float(parms['std_parallel_2'])
                if not test_for_parameter(parms, 'origin_lat'):
                    raise RuntimeError("Missing origin_lat parameter")
                else:
                    parms['origin_lat'] = float(parms['origin_lat'])
                if not test_for_parameter(parms, 'central_meridian'):
                    raise RuntimeError("Missing central_meridian parameter")
                else:
                    parms['central_meridian'] = \
                        float(parms['central_meridian'])
                if not test_for_parameter(parms, 'false_easting'):
                    raise RuntimeError("Missing false_easting parameter")
                else:
                    parms['false_easting'] = float(parms['false_easting'])
                if not test_for_parameter(parms, 'false_northing'):
                    raise RuntimeError("Missing false_northing parameter")
                else:
                    parms['false_northing'] = float(parms['false_northing'])

                # The datum must be in uppercase for the processing code to
                # work so if it is present here, we force it
                if not test_for_parameter(parms, 'datum'):
                    raise RuntimeError("Missing datum parameter")
                else:
                    parms['datum'] = parms['datum'].upper()
                if parms['datum'] not in datum_values:
                    raise ValueError("Invalid datum [%s]:"
                                     " Argument must be one of (%s)"
                                     % (parms['datum'],
                                        ', '.join(datum_values)))

            # ................................................................
            if target_projection == 'utm':
                if not test_for_parameter(parms, 'utm_zone'):
                    raise RuntimeError("Missing utm_zone parameter")
                else:
                    zone = int(parms['utm_zone'])
                    if zone < 0 or zone > 60:
                        raise ValueError("Invalid utm_zone [%d]:"
                                         " Value must be 0-60" % zone)
                    parms['utm_zone'] = zone
                if not test_for_parameter(parms, 'utm_north_south'):
                    raise RuntimeError("Missing utm_north_south parameter")
                elif parms['utm_north_south'] not in ns_values:
                    raise ValueError("Invalid utm_north_south [%s]:"
                                     " Argument must be one of (%s)"
                                     % (parms['utm_north_south'],
                                        ', '.join(ns_values)))

                if not test_for_parameter(parms, 'datum'):
                    parms['datum'] = None

            # ................................................................
            if target_projection == 'ps':
                if not test_for_parameter(parms, 'latitude_true_scale'):
                    # Must be tested before origin_lat
                    raise RuntimeError("Missing latitude_true_scale parameter")
                else:
                    value = float(parms['latitude_true_scale'])
                    if ((value < 60.0 and value > -60.0) or
                            value > 90.0 or value < -90.0):
                        raise ValueError("Invalid latitude_true_scale [%f]:"
                                         " Value must be between"
                                         " (-60.0 and -90.0) or"
                                         " (60.0 and 90.0)" % value)
                    parms['latitude_true_scale'] = value
                if not test_for_parameter(parms, 'longitude_pole'):
                    raise RuntimeError("Missing longitude_pole parameter")
                else:
                    parms['longitude_pole'] = float(parms['longitude_pole'])
                if not test_for_parameter(parms, 'origin_lat'):
                    # If the user did not specify the origin_lat value, then
                    # set it based on the latitude true scale
                    lat_ts = float(parms['latitude_true_scale'])
                    if lat_ts < 0:
                        parms['origin_lat'] = -90.0
                    else:
                        parms['origin_lat'] = 90.0
                else:
                    value = float(parms['origin_lat'])
                    if value != -90.0 and value != 90.0:
                        raise ValueError("Invalid origin_lat [%f]:"
                                         " Value must be -90.0 or 90.0"
                                         % value)
                    parms['origin_lat'] = value

                if not test_for_parameter(parms, 'false_easting'):
                    raise RuntimeError("Missing false_easting parameter")
                else:
                    parms['false_easting'] = float(parms['false_easting'])
                if not test_for_parameter(parms, 'false_northing'):
                    raise RuntimeError("Missing false_northing parameter")
                else:
                    parms['false_northing'] = float(parms['false_northing'])

                if not test_for_parameter(parms, 'datum'):
                    parms['datum'] = None

            # ................................................................
            if target_projection == 'lonlat':

                if not test_for_parameter(parms, 'datum'):
                    parms['datum'] = None

    # ------------------------------------------------------------------------
    if parms['resample_method'] not in resample_methods:
        raise ValueError("Invalid resample_method [%s]:"
                         " Argument must be one of (%s)"
                         % (parms['resample_method'],
                            ', '.join(resample_methods)))

    # ------------------------------------------------------------------------
    if parms['image_extents']:
        if not test_for_parameter(parms, 'image_extents_units'):
            raise RuntimeError("Missing image_extents_units parameter")
        else:
            if parms['image_extents_units'] not in image_extents_units:
                raise ValueError("Invalid image_extents_units [%s]:"
                                 " Argument must be one of (%s)"
                                 % (parms['image_extents_units'],
                                    ', '.join(image_extents_units)))
        if not test_for_parameter(parms, 'minx'):
            raise RuntimeError("Missing minx parameter")
        else:
            parms['minx'] = float(parms['minx'])
        if not test_for_parameter(parms, 'miny'):
            raise RuntimeError("Missing miny parameter")
        else:
            parms['miny'] = float(parms['miny'])
        if not test_for_parameter(parms, 'maxx'):
            raise RuntimeError("Missing maxx parameter")
        else:
            parms['maxx'] = float(parms['maxx'])
        if not test_for_parameter(parms, 'maxy'):
            raise RuntimeError("Missing maxy parameter")
        else:
            parms['maxy'] = float(parms['maxy'])
    else:
        # Default these
        parms['minx'] = None
        parms['miny'] = None
        parms['maxx'] = None
        parms['maxy'] = None
        parms['image_extents_units'] = None

    # ------------------------------------------------------------------------
    if parms['resize']:
        if not test_for_parameter(parms, 'pixel_size'):
            raise RuntimeError("Missing pixel_size parameter")
        else:
            parms['pixel_size'] = float(parms['pixel_size'])
        if not test_for_parameter(parms, 'pixel_size_units'):
            raise RuntimeError("Missing pixel_size_units parameter")
        else:
            if parms['pixel_size_units'] not in pixel_size_units:
                raise ValueError("Invalid pixel_size_units [%s]:"
                                 " Argument must be one of (%s)"
                                 % (parms['pixel_size_units'],
                                    ', '.join(pixel_size_units)))
    else:
        # Default this
        parms['pixel_size'] = None
        parms['pixel_size_units'] = None

    # ------------------------------------------------------------------------
    if ((parms['reproject'] or parms['image_extents']) and
            not parms['resize']):
        # Sombody asked for reproject or extents, but didn't specify a pixel
        # size

        units = 'meters'
        if parms['reproject'] and parms['target_projection'] == 'lonlat':
            units = 'dd'

        # Default to the sensor specific meters or dd equivalent
        parms['pixel_size'] = sensor.instance(scene).default_pixel_size[units]
        parms['pixel_size_units'] = units

        logger.warning("'resize' parameter not provided but required for"
                       " reprojection or image extents"
                       " (Defaulting pixel_size(%f) and pixel_size_units(%s)"
                       % (parms['pixel_size'], parms['pixel_size_units']))
