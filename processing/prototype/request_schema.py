
from cerberus import Validator


products = [
    {'type': 'list', 'allowed': ['tm_l1', 'tm_l1_metadata', 'tm_l1_customized', 'tm_toa', 'tm_bt', 'tm_sr', 'tm_cfmask', 'tm_dswe', 'tm_lst',
                                 'tm_toa_evi', 'tm_toa_msavi', 'tm_toa_nbr', 'tm_toa_nbr2', 'tm_toa_ndmi', 'tm_toa_ndvi', 'tm_toa_savi',
                                 'tm_sr_evi', 'tm_sr_msavi', 'tm_sr_nbr', 'tm_sr_nbr2', 'tm_sr_ndmi', 'tm_sr_ndvi', 'tm_sr_savi', 'tm_statistics']},

    {'type': 'list', 'allowed': ['etm_l1', 'etm_l1_metadata', 'etm_l1_customized', 'etm_toa', 'etm_bt', 'etm_sr', 'etm_cfmask', 'etm_dswe', 'etm_lst',
                                 'etm_toa_evi', 'etm_toa_msavi', 'etm_toa_nbr', 'etm_toa_nbr2', 'etm_toa_ndmi', 'etm_toa_ndvi', 'etm_toa_savi',
                                 'etm_sr_evi', 'etm_sr_msavi', 'etm_sr_nbr', 'etm_sr_nbr2', 'etm_sr_ndmi', 'etm_sr_ndvi', 'etm_sr_savi', 'etm_statistics']},

    {'type': 'list', 'allowed': ['olitirs_l1', 'olitirs_l1_metadata', 'olitirs_l1_customized', 'olitirs_toa', 'olitirs_bt', 'olitirs_sr', 'olitirs_cfmask', 'olitirs_dswe', 'olitirs_lst',
                                 'olitirs_toa_evi', 'olitirs_toa_msavi', 'olitirs_toa_nbr', 'olitirs_toa_nbr2', 'olitirs_toa_ndmi', 'olitirs_toa_ndvi', 'olitirs_toa_savi',
                                 'olitirs_sr_evi', 'olitirs_sr_msavi', 'olitirs_sr_nbr', 'olitirs_sr_nbr2', 'olitirs_sr_ndmi', 'olitirs_sr_ndvi', 'olitirs_sr_savi', 'olitirs_statistics']},

    {'type': 'list', 'allowed': ['oli_l1', 'oli_l1_metadata', 'oli_l1_customized', 'oli_toa', 'oli_cfmask',
                                 'oli_toa_evi', 'oli_toa_msavi', 'oli_toa_nbr', 'oli_toa_nbr2', 'oli_toa_ndmi', 'oli_toa_ndvi', 'oli_toa_savi', 'oli_statistics']},

    {'type': 'list', 'allowed': ['tirs_l1', 'tirs_l1_metadata', 'tirs_l1_customized', 'tirs_bt', 'tirs_statistics']}
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
    'debug': {'type': 'boolean', 'required': True},
    'keep_directory': {'type': 'boolean', 'required': True},
    'keep_intermediate_data': {'type': 'boolean', 'required': True},
    'keep_log': {'type': 'boolean', 'required': True}
}

input_options = {
    'order_id': {'type': 'string', 'required': True},
    'product_id': {'type': 'string', 'required': True},
    'product_url': {'type': 'string', 'required': True}
}


schema = {
    'input': {'type': 'dict', 'required': True, 'schema': input_options},
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
