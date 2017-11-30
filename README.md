## ESPA Processing Version 2.25.0 Release Notes

See git tag [v2.25.0]

### General Information
This project contains the code for processing a single input dataset to the final output products.  It is the controlling code for producing a product.  It does not produce science products on it's own, it calls on applications from other ESPA projects to perform that work.  Having said that, it does contain some code to perform a few things, such as, statistics generation, statistics plotting, and warping (using GDAL).

## Release Notes
Please see the Release Tags for notes related to past versions.

- Version change for system wide versioning
- External statistics and plotting CLI
- Angle bands only packaged with TOA-reflectance
- Switch to "surface temperature" terminology
- Ability to include resource snapshots

## Supported Science Products
To generate products for a science application, it must be installed on the system and the applications provided must be available on the PATH.  See the respective science projects for installation instructions and auxiliary data requirements.

For the core capabilities required by each science application including this project.  See  [espa-product-formatter](https://github.com/USGS-EROS/espa-product-formatter).

- CFmask - See [espa-cloud-masking](https://github.com/USGS-EROS/espa-cloud-masking)
- Elevation - See [espa-elevation](https://github.com/USGS-EROS/espa-elevation)
- Surface Temperature - See [espa-surface-temperature](https://github.com/USGS-EROS/espa-surface-temperature)
- Top of Atmosphere and Surface Reflectance - See [espa-surface-reflectance](https://github.com/USGS-EROS/espa-surface-reflectance)
- Spectral Indices - See [espa-spectral-indices](https://github.com/USGS-EROS/espa-spectral-indices)
- Surface Water Extent - See [espa-surface-water-extent](https://github.com/USGS-EROS/espa-surface-water-extent)
- L2 QA Tools - See [espa-l2qa-tools](https://github.com/USGS-EROS/espa-l2qa-tools)

## Installation Notes
TODO - Need to fill in this section.

## Usage
TODO - Need to fill in this section.


#### Support Information

This project is unsupported software provided by the U.S. Geological Survey (USGS) Earth Resources Observation and Science (EROS) Land Satellite Data Systems (LSDS) Project. For questions regarding products produced by this source code, please contact the [Landsat Contact Us][2] page and specify USGS Level-2 in the "Regarding" section.

#### Disclaimer

This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software.


[2]: https://landsat.usgs.gov/contact
    
