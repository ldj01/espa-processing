#! /usr/bin/env python

import click
import json


class CLIError(Exception):
    pass

TEMPLATE_FILE = '/usr/local/share/espa/order_template.json'


@click.command()
@click.version_option(version='2.11.3')
@click.option('--order-id', required=True, help='Order ID')
@click.option('--product-id', required=True, help='Product ID')
@click.option('--input-source', required=True,
              help='Source of the Input Data')
@click.option('--include-cloud-masking', is_flag=True, default=False,
              help='Include Cloud Masking')
@click.option('--include-customized-source-data', is_flag=True, default=False,
              help='Include Customized Source Data')
@click.option('--include-land-surface-temperature', is_flag=True,
              default=False, help='Include Land Surface Temperature')
@click.option('--include-source-metadata', is_flag=True, default=True,
              help='Include Source Metadata')
@click.option('--include-surface-reflectance', is_flag=True, default=False,
              help='Include Surface Reflectance')
@click.option('--include-sr-evi', is_flag=True, default=False,
              help='Include Surface Reflectance based EVI')
@click.option('--include-sr-msavi', is_flag=True, default=False,
              help='Include Surface Reflectance based MSAVI')
@click.option('--include-sr-nbr', is_flag=True, default=False,
              help='Include Surface Reflectance based NBR')
@click.option('--include-sr-nbr2', is_flag=True, default=False,
              help='Include Surface Reflectance based NBR2')
@click.option('--include-sr-ndmi', is_flag=True, default=False,
              help='Include Surface Reflectance based NDMI')
@click.option('--include-sr-ndvi', is_flag=True, default=False,
              help='Include Surface Reflectance based NDVI')
@click.option('--include-sr-savi', is_flag=True, default=False,
              help='Include Surface Reflectance based SAVI')
@click.option('--include-top-of-atmosphere', is_flag=True, default=False,
              help='Include Top-of-Atmosphere Reflectance')
@click.option('--include-brightness-temperature', is_flag=True, default=False,
              help='Include Thermal Brightness Temperature')
@click.option('--include-surface-water-extent', is_flag=True, default=False,
              help='Include Surface Water Extent')
@click.option('--include-statistics', is_flag=True,
              help='Include Statistics')
def cli(order_id, product_id, input_source,
        include_cloud_masking,
        include_customized_source_data,
        include_land_surface_temperature,
        include_source_metadata,
        include_surface_reflectance,
        include_sr_evi,
        include_sr_msavi,
        include_sr_nbr,
        include_sr_nbr2,
        include_sr_ndmi,
        include_sr_ndvi,
        include_sr_savi,
        include_top_of_atmosphere,
        include_brightness_temperature,
        include_surface_water_extent,
        include_statistics):
    """
    """

    contents = None
    with open(TEMPLATE_FILE, 'r') as template_fd:
        contents = template_fd.read()

    if not contents:
        raise CLIError('{} not found'.format(TEMPLATE_FILE))

    template = json.loads(contents)
    if template is None:
        raise CLIError('Failed loading {}'.format(TEMPLATE_FILE))

    print(order_id, product_id, input_source,
          include_cloud_masking,
          include_customized_source_data,
          include_land_surface_temperature,
          include_source_metadata,
          include_surface_reflectance,
          include_sr_evi,
          include_sr_msavi,
          include_sr_nbr,
          include_sr_nbr2,
          include_sr_ndmi,
          include_sr_ndvi,
          include_sr_savi,
          include_top_of_atmosphere,
          include_brightness_temperature,
          include_surface_water_extent,
          include_statistics)


if __name__ == '__main__':
    cli()
