## ESPA Processing Version 2.10.0 Release Notes
Release Date: Dec XX, 2015

See git tag [espa-2.10.0-release]

### General Information
This project contains the code for processing a single input dataset to the final output products.  It is the controlling code for producing a product.  It does not produce science products on it's own, it calls on applications from other ESPA projects to perform that work.  Having said that, it does contain some code to perform a few things, such as, statistics generation, statistics plotting, and warping (using GDAL).

Authors: David V. Hill, SGT and Ron Dilley, Innovate!

License: NASA Open Source Agreement 1.3
USGS Designation: EROS Science Processing Architecture (ESPA)

## Release Notes
Please see the Release Tags for notes related to past versions.

  - Added support for Land Surface Temperature products.
  - Added support for ENVI BIP output products.
  - Modified to call science application specific helper scripts.  These helper scripts determine which sensor specific versions of science applications to call for a product.  In an effort to dumb down and cleanup the code in this project.

## Supported Science Products
TODO - Need to fill in this section.

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
