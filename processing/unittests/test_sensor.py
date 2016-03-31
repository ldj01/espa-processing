#!/usr/bin/env python


import os
import unittest
from cStringIO import StringIO

import sensor


class TestSensor(unittest.TestCase):
    """Test a few things, and expand on it someday"""

    def setUp(self):
        self.terra_product_id = 'MOD09GQ.A2000072.h02v09.005.2008237032813'
        self.aqua_product_id = 'MYD09GQ.A2000072.h02v09.005.2008237032813'
        self.lt4_product_id = 'LT42181092013069PFS00'
        self.lt5_product_id = 'LT52181092013069PFS00'
        self.le7_product_id = 'LE72181092013069PFS00'
        self.lc8_product_id = 'LC82181092013069PFS00'
        self.lt8_product_id = 'LT82181092013069PFS00'
        self.lo8_product_id = 'LO82181092013069PFS00'
        self.lt04_product_id = 'LT04_L1T_038038_19950624_20160302_01_T1'
        self.lt05_product_id = 'LT05_L1T_038038_19950624_20160302_01_T1'
        self.le07_product_id = 'LE07_L1T_038038_19950624_20160302_01_T1'
        self.lc08_product_id = 'LC08_L1T_038038_19950624_20160302_01_T1'
        self.lt08_product_id = 'LT08_L1T_038038_19950624_20160302_01_T1'
        self.lo08_product_id = 'LO08_L1T_038038_19950624_20160302_01_T1'

    def tearDown(self):
        pass

    def test_is_terra(self):
        method = sensor.is_terra

        self.assertTrue(method(self.terra_product_id))
        self.assertFalse(method(self.aqua_product_id))

    def test_is_aqua(self):
        method = sensor.is_aqua

        self.assertTrue(method(self.aqua_product_id))
        self.assertFalse(method(self.terra_product_id))

    def test_is_modis(self):
        method = sensor.is_modis

        self.assertTrue(method(self.aqua_product_id))
        self.assertTrue(method(self.terra_product_id))

        self.assertFalse(method(self.lt04_product_id))
        self.assertFalse(method(self.lt05_product_id))
        self.assertFalse(method(self.le07_product_id))
        self.assertFalse(method(self.lc08_product_id))
        self.assertFalse(method(self.lt08_product_id))
        self.assertFalse(method(self.lo08_product_id))

        self.assertFalse(method(self.lt4_product_id))
        self.assertFalse(method(self.lt5_product_id))
        self.assertFalse(method(self.le7_product_id))
        self.assertFalse(method(self.lc8_product_id))
        self.assertFalse(method(self.lt8_product_id))
        self.assertFalse(method(self.lo8_product_id))

    def test_is_lt4(self):
        method = sensor.is_lt4

        self.assertTrue(method(self.lt4_product_id))
        self.assertFalse(method(self.lt5_product_id))

    def test_is_lt5(self):
        method = sensor.is_lt5

        self.assertTrue(method(self.lt5_product_id))
        self.assertFalse(method(self.le7_product_id))

    def test_is_le7(self):
        method = sensor.is_le7

        self.assertTrue(method(self.le7_product_id))
        self.assertFalse(method(self.lc8_product_id))

    def test_is_lc8(self):
        method = sensor.is_lc8

        self.assertTrue(method(self.lc8_product_id))
        self.assertFalse(method(self.lt8_product_id))

    def test_is_lt8(self):
        method = sensor.is_lt8

        self.assertTrue(method(self.lt8_product_id))
        self.assertFalse(method(self.lo8_product_id))

    def test_is_lo8(self):
        method = sensor.is_lo8

        self.assertTrue(method(self.lo8_product_id))
        self.assertFalse(method(self.lt4_product_id))

    def test_is_lt04(self):
        method = sensor.is_lt04

        self.assertTrue(method(self.lt04_product_id))
        self.assertFalse(method(self.lt05_product_id))

    def test_is_lt05(self):
        method = sensor.is_lt05

        self.assertTrue(method(self.lt05_product_id))
        self.assertFalse(method(self.le07_product_id))

    def test_is_le07(self):
        method = sensor.is_le07

        self.assertTrue(method(self.le07_product_id))
        self.assertFalse(method(self.lc08_product_id))

    def test_is_lc08(self):
        method = sensor.is_lc08

        self.assertTrue(method(self.lc08_product_id))
        self.assertFalse(method(self.lt08_product_id))

    def test_is_lt08(self):
        method = sensor.is_lt08

        self.assertTrue(method(self.lt08_product_id))
        self.assertFalse(method(self.lo08_product_id))

    def test_is_lo08(self):
        method = sensor.is_lo08

        self.assertTrue(method(self.lo08_product_id))
        self.assertFalse(method(self.lt04_product_id))

    def test_is_landsat8(self):
        method = sensor.is_landsat8

        self.assertTrue(method(self.lc8_product_id))
        self.assertTrue(method(self.lt8_product_id))
        self.assertTrue(method(self.lo8_product_id))

        self.assertTrue(method(self.lc08_product_id))
        self.assertTrue(method(self.lt08_product_id))
        self.assertTrue(method(self.lo08_product_id))

        self.assertFalse(method(self.lt4_product_id))
        self.assertFalse(method(self.lt5_product_id))
        self.assertFalse(method(self.le7_product_id))

        self.assertFalse(method(self.lt04_product_id))
        self.assertFalse(method(self.lt05_product_id))
        self.assertFalse(method(self.le07_product_id))

    def test_is_landsat_historical(self):
        method = sensor.is_landsat_historical

        self.assertTrue(method(self.lt4_product_id))
        self.assertTrue(method(self.lt5_product_id))
        self.assertTrue(method(self.le7_product_id))
        self.assertTrue(method(self.lc8_product_id))
        self.assertTrue(method(self.lt8_product_id))
        self.assertTrue(method(self.lo8_product_id))

        self.assertFalse(method(self.lt04_product_id))
        self.assertFalse(method(self.lt05_product_id))
        self.assertFalse(method(self.le07_product_id))
        self.assertFalse(method(self.lc08_product_id))
        self.assertFalse(method(self.lt08_product_id))
        self.assertFalse(method(self.lo08_product_id))

    def test_is_landsat_collection(self):
        method = sensor.is_landsat_collection

        self.assertTrue(method(self.lt04_product_id))
        self.assertTrue(method(self.lt05_product_id))
        self.assertTrue(method(self.le07_product_id))
        self.assertTrue(method(self.lc08_product_id))
        self.assertTrue(method(self.lt08_product_id))
        self.assertTrue(method(self.lo08_product_id))

        self.assertFalse(method(self.lt4_product_id))
        self.assertFalse(method(self.lt5_product_id))
        self.assertFalse(method(self.le7_product_id))
        self.assertFalse(method(self.lc8_product_id))
        self.assertFalse(method(self.lt8_product_id))
        self.assertFalse(method(self.lo8_product_id))


if __name__ == '__main__':
    unittest.main(verbosity=2)
