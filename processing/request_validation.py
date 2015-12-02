
from cerberus import Validator


products = [
    {'type': 'list', 'allowed': ['tm_sr', 'tm_toa', 'tm_l1', 'tm_ndvi', 'tm_ndsi']},
    {'type': 'list', 'allowed': ['etm_sr', 'etm_toa', 'etm_l1']},
    {'type': 'list', 'allowed': ['olitirs_sr', 'olitirs_toa', 'olitirs_l1']},
    {'type': 'list', 'allowed': ['oli_l1']}
]


projections = [
    {'type': 'dict', 'schema': {'name': { 'type': 'string', 'required': True, 'allowed': ['aea']},
                                'standard_parallel_1': {'type': 'float', 'required': True, 'min':-90.0, 'max': 90.0},
                                'standard_parallel_2': {'type': 'float', 'required': True, 'min':-90.0, 'max': 90.0},
                                'central_meridian': {'type': 'float', 'required': True, 'min':-180.0, 'max':180.0},
                                'latitude_of_origin': {'type': 'float', 'required': True, 'min':-90.0, 'max':90.0},
                                'false_easting': {'type': 'float', 'required': True},
                                'false_northing': {'type': 'float', 'required': True}}},

    {'type': 'dict', 'schema': {'name': {'type': 'string', 'required': True, 'allowed': ['utm']},
                                'zone': {'type': 'integer', 'required': True, 'min': 1, 'max': 60},
                                'zone_ns': {'type': 'string', 'required': True, 'allowed': ['north', 'south']}}},

    {'type': 'dict', 'schema': {'name': {'type': 'string', 'required': True, 'allowed': ['lonlat']}}},

    {'type': 'dict', 'schema': {'name': {'type': 'string', 'required': True, 'allowed': ['sinu']},
                                'central_meridian': {'type': 'float', 'required': True, 'min':-180.0, 'max':180.0},
                                'false_easting': {'type': 'float', 'required': True},
                                'false_northing': {'type': 'float', 'required': True}}},

    {'type': 'dict', 'schema': {'name': {'type': 'string', 'required': True, 'allowed': ['ps']},
                                'longitudinal_pole': {'type': 'float', 'required': True, 'min': -180.0, 'max': 180.0},
                                'latitude_true_scale': {'type': 'float', 'required': True, 'anyof': [{'min': -90.0 , 'max': -60.0},
                                                                                                     {'min': 60.0 , 'max': 90.0}]}}}
]

customizations = {
  'projection': {'type': 'dict', 'oneof': projections}
}


developer_options = {
  'keep_directory': {'type': 'boolean'},
  'keep_intermediate_data': {'type': 'boolean'},
  'keep_log': {'type': 'boolean'}
}


request_schema = {
  'products': {'type': 'list', 'required': True, 'oneof': products},
  'customizations': {'type': 'dict', 'required': False, 'schema': customizations},
  'developer_options': {'type': 'dict', 'required': False, 'schema': developer_options}
}


# Don't need this yet for anything, but maybe later
#class RequestValidator(Validator):
#
#    def __init__(self, *args, **kwargs):
#        super(RequestValidator, self).__init__(*args, **kwargs)
#
#    def _validate_type_products(self, field, value):
#        if not hasattr(value, '__iter__'):
#            self._error(field, 'must be iterable, {0} found'
#                               .format(type(value)))
#
#        for product in value:
#            print product

class RequestValidationError(Exception):
    pass

def validate_request(order_options):
    validator = Validator()
    validator.validate(order_options, request_schema)

    if validator.errors:
        raise RequestValidationError(validator.errors)
