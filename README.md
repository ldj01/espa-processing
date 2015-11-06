## ESPA Processing Version 2.10.0 Release Notes
Release Date: Dec XX, 2015

See git tag [espa-2.10.0-release]

### General Information
This project contains the code for processing a single input dataset to the final output products.  It is the controlling code for producing a product.  It does not produce science products on it's own, it calls on applications from other ESPA projects to perform that work.  Having said that, it does contain some code to perform a few things, such as, statistics generation, statistics plotting, and warping (using GDAL).

Authors: David V. Hill, SGT and Ron Dilley, Innovate!

License: NASA Open Source Agreement 1.3
USGS Designation: EROS Science Processing Architecture (ESPA)

## Release Notes
  - Added support for Land Surface Temperature products.
  - Added support for ENVI BIP output products.
  - Modified to call science application specific helper scripts.  These helper scripts determine which sensor specific versions of science applications to call for a product.  In an effort to dumb down and cleanup the code in this project.

## Supported Science Products
TODO - Need to fill in this section.

## Installation Notes
TODO - Need to fill in this section.

## Usage
TODO - Need to fill in this section.

## OLD Release Notes (To be removed ??? TBD)
Version 2.9.2 (October 2015)
        Added checks to the ondemand_cron to limit the number of 
        active Hadoop jobs.

Version 2.9.0 (XXXX 2015)
        Code for the web interface has been moved to the following repository.
            https://github.com/USGS-EROS/espa-web

        Code for the down load client has been moved to the following
        repository.
            https://github.com/USGS-EROS/espa-bulk-downloader

        Code for the tools and prototype directories have been moved to better
        locations under the following repositories.
            https://github.com/USGS-EROS/espa-junk-drawer
            https://github.com/USGS-EROS/espa-maintenance


Version 2.8.5 (July 2015)
        Added additional error condition to network errors 
            - retry on socket timeouts

Version 2.8.4 (July 2015)
        Added additional error conditions to the auto error resolver
            - sixs failures now retry
            - additional warp failures result in status unavailable

Version 2.8.3 (July 2015)
        Modified RSS feed queries to use raw SQL due to performance overhead
        with large orders.
        Created separate uwsgi ini configurations for each environment to
        ease deployment logic.
        Removed deploy_install.sh and replaced with deploy_install.py,
        which now works with github instead of subversion on Google Projects.
        Updated lsrd_stats.py to work off of separate credentials to support
        reporting from the historical db.
        Enhanced processing system to support using a local path for output
        product delivery and code cleanup associated with supporting the
        local path.
        Modified warping parameters for UTM South to match UTM North with both
        now using the WGS84 datum.

Version 2.8.1 (May 2015)
        Added additional error conditions to the master error handler
        Cosmetic changes for field labels
        Removed inventory restrictions on L8SR TIRS failure scenes

Version 2.8.0 (May 2015)

Version 2.7.2 (March 4, 2015)
        Added DSWE to ECV section for staff only
        Corrected bugs with validation messages
        UI updates for images on index page

Version 2.7.1 (January 6, 2015)
        Added status update retry logic to processing tier.
        Corrected set_product_retry in app tier to include log file.

Version 2.7.0 (December 22, 2014)
        Added auto-retry logic.
        Added landsat 8 surface reflectance.
        Added timeout for SUDS ObjectCache.
        Utilizing EE HTTP services for ordering and level 1 download.

Version 2.5.0 (August 27, 2014)
        Added console application for staff personnel.

        Added priority to Orders in conjunction with Hadoop Queueing to prevent
        large orders from dominating all compute resources.

        Moved espa schema file to espa-common to prevent network effects from
        causing processing failures.

        Added select MODIS products as customizable input products.
        Corrected error with invalid checksum generation.
        Multiple bug fixes relating to image reprojection and resampling.
        Added trunk/espa_common to hold shared libs between web and processing.

Version 2.4.0 (July 29, 2014)
        Transitioned to binary raster processing for science algorithms.
        Introduced schema constrained xml metadata for all products.
        Format conversion has been introduced.
        Reprojected products now have properly populated metadata entries.

Version 2.3.0 (May 30, 2014)

        *Note -- All changes for this release are for the web tier only.
                 No modifications were made to the back end processing code.

        -----------------
        major features
        -----------------
        Added ability to authenticate users against EarthExplorer
            - reorganized lta.py, added service clients for RegistrationService

        L1T order submission changed from LTA Massloader to
        LTA OrderWrapperService

        Added temporary logic to search for user email addresses in both the
        Django auth User table and the Order email field to support migration
        of EE auth.
            - Order.email field will be removed with the next release.

        -----------------
        platform
        -----------------
        Upgraded to Django 1.6

        -----------------
        project structure
        -----------------
        Upgraded project structure to be Django 1.6 compliant

        Reorganized the orderservice directory
            - now called 'web'
            - moved contents of 'htdocs' into 'web/static'
            - populated 'web/static' with Django admin static content,
              eliminating need for softlinks
                - regenerate these with ./manage.py collectstatic

        -----------------
        settings.py
        -----------------
        Modified settings.py to include the static files app and set
        STATIC_ROOT, STATIC_URL
        Added LOGIN_URL, LOGIN_REDIRECT_URL
        Added URL_FOR() lambda function as service locator function
            - was previously implemented in lta.py, multiple modules now need
              this and its a critical dependency 
        Added ESPA_DEBUG flag to settings.py
            - looks for ESPA_DEBUG = TRUE in environment variables, enables
              DEBUG and TEMPLATE_DEBUG

        Moved all configuration items to settings.py
            - configurable items can be set in espa-uwsgi.ini or as environment
              variables
            - private key & database credentials must be provided on the local
              filesystem in ~/.cfgno

        -----------------
        espa-uwsgi.ini
        -----------------
        Removed the /media mapping in espa-uwsgi.ini as it is no longer
        necessary (merged into /static mapping)

        -----------------
        Misc
        -----------------

        django.wsgi removed in favor of django generated wsgi.py

        Deleted scene_cache.py from the espa/ codebase
            - Moved the scene cache replacement from
              trunk/prototype/new_scene_cache to trunk/scenecache.

        Moved all Order & Scene related operations to the models.Order and
        models.Scene classes as either class or static methods

        Removed all partially hardcoded urls from template and view code,
        replaced with named urls, {% url %}, {% static %} and reverse() tags

        Moved all cross-application functionality into espa_web

        Added espa_web/context_processors.py to include needed variables in
        templates
            - must include in settings.py TEMPLATE_CONTEXT_PROCESSORS

        Added espa_web/auth_backends.py for EE authentication 
            - Django auth system plugin
            - must include in settings.py AUTHENTICATION_BACKENDS


Version 2.2.5 (March 11, 2014)
        Made change to support variable cloud pixel threshold for calls
        to cfmask.

Version 2.2.4 (December 20, 2013)
        Bug fix to parse_hdf_subdatasets() in cdr_ecv.py to correct
        reprojection failures.

Version 2.2.3
        Altered cdr_ecv to use straight FTP rather than SCP (performance)

Version 2.2.2
        Added SCA & SWE to internal ordering
        Corrected unchecked reprojection errors
        Corrected Bulk Ordering Navigation
        Fail job submission if no products selected
        Added MSAVI to spectral indices
        Merged all vegetation indices to a single raster
        Removed standalone CFMask option
        Removed solr index generation option
        Corrected cross browser rendering issues

Version 2.2.1
        Fixed bug reprojecting spectral indices
        Fixed bug reprojecting cfmask
        Modified reprojected filename extensions to '.tif'
        Defaulted pixel size to 30 meters or dd equivalent when necessary.
        Corrected Albers subsetting failures.
        Modified code to properly clean up HDFs when reprojecting/reformatting
        to GeoTiff
        Optimized calls to warp outputs in the cdr_ecv.
        Added first set of prototype system level tests for cdr_ecv.py

Version 2.2.0
        Added code to perform reprojection.
        Added code to perform framing.
        Added code to perform subsetting.

Version 2.1.6
        Reorganized the codebase to accomodate LPVS code.
        Implemented a standardized logging format.
        Added webpages for marketing.

Version 2.1.5
        Added a lockfile to the scene_cache update to prevent multiple
        processes from running, which causes a parallel contention issue

Version 2.1.4
        Bug fix for duplicate orders from EE.  Modified core.py
        load_orders_from_ee() to look for an order + scene in the db before
        attempting to add a new one

Version 2.1.3
        Fix to clear logs upon non-error status update.
        Initial version of api.py added.
        Integration for SI 1.1.2, cfmask 1.1.1, ledaps 1.3.0,
        cfmask_append 1.0.1, swe 1.0.0
        Updated code to interact with online cache over private 10Gig network
        Added load balancing code mapper.py for contacting the online cache

Version 2.1.2
        Updates for new cfmask and appending cfmask to sr outputs.
        Multiple bug fixes related to UI css files when viewed of https
Version 2.1.1
        Update internal email verbage to remove "Surface Reflectance"
        Bug fixes for LTA integration when processing mixed orders
        Fixed product file names
        Corrected bug where espa user interface wouldn't accept a Glovis
        scenelist
        Added all available spectral indices to espa_internal
        Integrated cfmask 1.0.4
        Integrated updated Spectral Indices

Version 2.1.0
        Updated web code to verify submitted scenes against the inventory
        before accepting them.
        Updated web code to pull orders from EE on demand for surface
        reflectance only.

Version 2.0.4
        Update espa to work with new ledaps and cfmask
        Corrected issue with bad tarballs being distributed.
        Generated cksum files and distribute those with the product.

Version 2.0.3
        Updated espa to work with ledaps 1.2 & cfmask 1.0.1
        Added ability for all users to select product options.
        Added ability to order cfmask for espa_internal and espa_admin
        Removed seperate source file distribution (can be selected as an
        option)

Version 2.0.2
        Fixed solr generation to account for landsat metadata field name
        changes
        Changed espa TRAM ordering priority
        Tested setting ESPA work directory to "." or cwd()

Version 2.0.1
        Added espa_internal for evaluation.

Version 2.0.0
        Modified architecture to remove the Chain of Command structure from
        processing.
        Modified espa to work with ledaps 1.1.2.
        Added ability for end users to select which products they want in
        their delivery (admin acct only at this time.)
        Added mapper.py and removed any external calls from espa.py except for
        scp calls to obtain data.  Mapper.py handles
        all status notifications to the espa tracking node now.

Version 1.3.8
        Updated espa to work with ledaps 1.1.1.

Version 1.3.7
        Updated espa to work with ledaps 1.1.0.  Added scene_cache.py to speed
        up scene submission.

        Multiple bugfixes and cosmetic website/email changes.

Version 1.3.5
        Updated 'lndpm' binary to work with new Landsat metdata

        Corrected metadata file lookup to account for Landsat's metadata format
        changes.

Version 1.3.4
        Corrections to reprojection code in espacollection.py when creating
        browse images.

Version 1.3.3
        Modifications to the NDVI code to release memory more quickly, reduce
        memory footprint.

Version 1.3.2
        Correction to the solr index to be semicolon seperated

Version 1.3.1
        Bug fixes for NDVI and CleanupDirs

Version 1.3.0
        Updated LEDAPS to the latest version from November 2011.  Added
        ability to generate NDVI for output products

        Multiple additions to collection processing to create browse and solr
        index.

Version 1.2.0
        Replaced Python's tar and untar commands in espa.py with the native
        operating system commands.

        Prior to this there were intermittent corrupt archives making it into
        the distribution node.

        Native os commands are also far faster than the python implementation.

Version 1.1.0
        Added RSS Status capability to ordering interface

Version 1.0.0
        First major stable version of ESPA released that will process Landsat
        L1T's to Surface Reflectance

## More Information
This project is provided by the US Geological Survey (USGS) Earth Resources
Observation and Science (EROS) Land Satellite Data Systems (LSDS) Science
Research and Development (LSRD) Project. For questions regarding products
produced by this source code, please contact the Landsat Contact Us page and
specify USGS CDR/ECV in the "Regarding" section.
https://landsat.usgs.gov/contactus.php 
