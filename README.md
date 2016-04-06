## ESPA Processing Version 2.11.0 Release Notes
Release Date: May 2016

See git tag [espa-2.11.0-release]

### General Information
This project contains the code for processing a single input dataset to the final output products.  It is the controlling code for producing a product.  It does not produce science products on it's own, it calls on applications from other ESPA projects to perform that work.  Having said that, it does contain some code to perform a few things, such as, statistics generation, statistics plotting, and warping (using GDAL).

Authors: David V. Hill, SGT and Ron Dilley, Innovate!

License: NASA Open Source Agreement 1.3

USGS Designation: EROS Science Processing Architecture (ESPA)

## Release Notes
Please see the Release Tags for notes related to past versions.

  - Updated elevation generation to support the new generation executable.
  - Updated surface water extent processing to be allowed for L8 OLITIRS data.
  - Updated land surface temperature processing to be allowed for L4 TM and L8 OLITIRS data.
  - Modified the scheduling code to be self contained within the scheduling directory.
  - Modified the processing code to be self contained within the processing directory.
  - Added support for L4, 5, 7 collection processing.
  - Turned sleeping off for plotting requests, since they do not interface with the LTA.
  - Removed remaining keep_log code, since the logs are always kept from now on.
  - General cleanup of the code base.

## Supported Science Products
To generate products for a science application, it must be installed on the system and the applications provided must be available on the PATH.  See the respective science projects for installation instructions and auxiliary data requirements.

For the core capabilities required by each science application including this project.  See  [espa-product-formatter](https://github.com/USGS-EROS/espa-product-formatter).

- CFmask - See [espa-cloud-masking](https://github.com/USGS-EROS/espa-cloud-masking)
- Land Surface Temperature - See [espa-land-surface-temperature](https://github.com/USGS-EROS/espa-land-surface-temperature)
- Top of Atmosphere and Surface Reflectance - See [espa-surface-reflectance](https://github.com/USGS-EROS/espa-surface-reflectance)
- Spectral Indices - See [espa-spectral-indices](https://github.com/USGS-EROS/espa-spectral-indices)
- Surface Water Extent - See [espa-surface-water-extent](https://github.com/USGS-EROS/espa-surface-water-extent)

## Installation Notes
TODO - Need to fill in this section.

## Usage
TODO - Need to fill in this section.

## More Information
This project is provided by the US Geological Survey (USGS) Earth Resources
Observation and Science (EROS) Land Satellite Data Systems (LSDS) Science
Research and Development (LSRD) Project. For questions regarding products
produced by this source code, please contact the Landsat Contact Us page and
specify USGS CDR/ECV in the "Regarding" section.
https://landsat.usgs.gov/contactus.php
