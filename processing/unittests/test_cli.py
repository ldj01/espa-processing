#!/usr/bin/env python


import os
import unittest
from argparse import ArgumentParser


import cli


class TestCLI(unittest.TestCase):
    """Test the cli.py methods"""

    def setUp(self):
        self.parser = cli.build_command_line_parser()
        self.static_options = ['--order-id', 'ORDERID',
                               '--input-product-id', 'PRODUCT_ID',
                               '--input-url', 'file://',
                               '--espa-api', 'skip_api',
                               '--work-dir', '.',
                               '--dist-method', 'local',
                               '--dist-dir', '.']

    def tearDown(self):
        pass

    def test_load_template(self):
        cli.load_template('order_template.json')
        with self.assertRaises(cli.BadTemplateError) as context:
            cli.load_template('unittests/empty.json')
        with self.assertRaises(ValueError) as context:
            cli.load_template('unittests/garbage.json')

    def test_extents_not_specified(self):
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])

        args = self.parser.parse_args(options)
        self.assertFalse(cli.check_for_extents(args))

    def test_extents_specified(self):
        # Check missing options
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])

        # Missing minx
        options.extend(['--extent-maxx', '2.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_for_extents(args)
        except cli.MissingExtentError:
            pass

        # Missing maxx
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--extent-minx', '1.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_for_extents(args)
        except cli.MissingExtentError:
            pass

        # Missing miny
        options.extend(['--extent-maxx', '2.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_for_extents(args)
        except cli.MissingExtentError:
            pass

        # Missing maxy
        options.extend(['--extent-miny', '1.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_for_extents(args)
        except cli.MissingExtentError:
            pass

        # Check all options
        options.extend(['--extent-maxy', '2.0'])

        args = self.parser.parse_args(options)
        self.assertTrue(cli.check_for_extents(args))

    def test_sinu_specified(self):
        # Check not sinu
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'utm'])

        args = self.parser.parse_args(options)
        self.assertFalse(cli.check_projection_sinu(args))

        # Check missing options
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'sinu'])

        # Missing central meridian
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_sinu(args)
        except cli.MissingSinuError:
            pass

        # Missing false easting
        options.extend(['--central-meridian', '-96.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_sinu(args)
        except cli.MissingSinuError:
            pass

        # Missing false northing
        options.extend(['--false-easting', '2.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_sinu(args)
        except cli.MissingSinuError:
            pass

        # Check all options
        options.extend(['--false-northing', '2.0'])

        args = self.parser.parse_args(options)
        self.assertTrue(cli.check_projection_sinu(args))

    def test_aea_specified(self):
        # Check not aea
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'sinu'])

        args = self.parser.parse_args(options)
        self.assertFalse(cli.check_projection_aea(args))

        # Check missing options
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'aea'])

        # Missing central meridian
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_aea(args)
        except cli.MissingAeaError:
            pass

        # Missing std parallel 1
        options.extend(['--central-meridian', '-96.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_aea(args)
        except cli.MissingAeaError:
            pass

        # Missing std parallel 2
        options.extend(['--std-parallel-1', '29.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_aea(args)
        except cli.MissingAeaError:
            pass

        # Missing origin latitude
        options.extend(['--std-parallel-2', '70.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_aea(args)
        except cli.MissingAeaError:
            pass

        # Missing false easting
        options.extend(['--origin-latitude', '40.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_aea(args)
        except cli.MissingAeaError:
            pass

        # Missing false northing
        options.extend(['--false-easting', '2.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_aea(args)
        except cli.MissingAeaError:
            pass

        # Missing datum
        options.extend(['--false-northing', '2.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_aea(args)
        except cli.MissingAeaError:
            pass

        # Check all options
        options.extend(['--datum', 'wgs84'])

        args = self.parser.parse_args(options)
        self.assertTrue(cli.check_projection_aea(args))


    def test_utm_specified(self):
        # Check not aea
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'sinu'])

        args = self.parser.parse_args(options)
        self.assertFalse(cli.check_projection_utm(args))

        # Check missing options
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'utm'])

        # Missing utm zone
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_utm(args)
        except cli.MissingUtmError:
            pass

        # Missing utm north south
        options.extend(['--utm-zone', '10.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_utm(args)
        except cli.MissingUtmError:
            pass

        # Check all options
        options.extend(['--utm-north-south', 'north'])

        args = self.parser.parse_args(options)
        self.assertTrue(cli.check_projection_utm(args))

    def test_ps_specified(self):
        # Check not ps
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'sinu'])

        args = self.parser.parse_args(options)
        self.assertFalse(cli.check_projection_ps(args))

        # Check missing options
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'ps'])

        # Missing latitude true scale
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_ps(args)
        except cli.MissingPsError:
            pass

        # Missing longitude pole
        options.extend(['--latitude-true-scale', '-90.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_ps(args)
        except cli.MissingPsError:
            pass

        # Missing origin latitude
        options.extend(['--longitude-pole', '0.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_ps(args)
        except cli.MissingPsError:
            pass

        # Missing false easting
        options.extend(['--origin-latitude', '-71.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_ps(args)
        except cli.MissingPsError:
            pass

        # Missing false northing
        options.extend(['--false-easting', '2.0'])
        try:
            args = self.parser.parse_args(options)
            cli.check_projection_ps(args)
        except cli.MissingPsError:
            pass

        # Check all options
        options.extend(['--false-northing', '2.0'])

        args = self.parser.parse_args(options)
        self.assertTrue(cli.check_projection_ps(args))
