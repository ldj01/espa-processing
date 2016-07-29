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
        #with self.assertRaises(Exception) as context:
        #    cli.load_template('cli.py')
        #    #self.assertTrue('frog' in context)

    def test_extents_not_specified(self):
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])

        args = self.parser.parse_args(options)
        self.assertFalse(cli.check_for_extents(args))

    def test_extents_specified(self):
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--extent-minx', '1.0'])
        options.extend(['--extent-maxx', '2.0'])
        options.extend(['--extent-miny', '1.0'])
        options.extend(['--extent-maxy', '2.0'])

        args = self.parser.parse_args(options)
        self.assertTrue(cli.check_for_extents(args))

    def test_check_for_not_all_extents(self):
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])

        # Missing minx
        opts_x = [x for x in options]
        opts_x.extend(['--extent-maxx', '2.0'])
        try:
            args = self.parser.parse_args(opts_x)
            cli.check_for_extents(args)
        except cli.MissingExtentError:
            pass

        # Missing maxx
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

        self.assertTrue(True)

    def test_sinu_specified(self):
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'sinu'])
        options.extend(['--central-meridian', '1.0'])
        options.extend(['--false-easting', '2.0'])
        options.extend(['--false-northing', '2.0'])

        args = self.parser.parse_args(options)
        self.assertTrue(cli.check_projection_sinu(args))

    def test_check_for_not_all_sinu(self):
        options = [x for x in self.static_options]
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'sinu'])

        # Missing minx
        opts_x = [x for x in options]
        opts_x.extend(['--false-easting', '2.0'])
        try:
            args = self.parser.parse_args(opts_x)
            cli.check_projection_sinu(args)
        except cli.MissingSinuError:
            pass

        # Missing maxx
        options.extend(['--central-meridian', '1.0'])

        try:
            args = self.parser.parse_args(options)
            cli.check_projection_sinu(args)
        except cli.MissingSinuError:
            pass

        # Missing miny
        options.extend(['--false-easting', '2.0'])

        try:
            args = self.parser.parse_args(options)
            cli.check_projection_sinu(args)
        except cli.MissingSinuError:
            pass

        self.assertTrue(True)
