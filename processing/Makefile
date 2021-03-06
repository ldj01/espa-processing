#-----------------------------------------------------------------------------
# Makefile
#
# Simple makefile for installing the scripts.
#-----------------------------------------------------------------------------
.PHONY: all install clean check

# Inherit from upper-level make.config
TOP = ..
include $(TOP)/make.config

SCRIPTS = \
    cli.py \
    ondemand_mapper.py

SCRIPT_IMPORTS = \
    api_interface.py \
    config_utils.py \
    distribution.py \
    environment.py \
    espa_exception.py \
    initialization.py \
    landsat_metadata.py \
    logging_tools.py \
    parameters.py \
    processor.py \
    product_formatting.py \
    sensor.py \
    settings.py \
    staging.py \
    transfer.py \
    utilities.py

TEMPLATE = \
    order_template.json


#-----------------------------------------------------------------------------
all:

#-----------------------------------------------------------------------------
install:
	install -d $(link_install_path)
	install -d $(link_share_path)
	install -d $(install_path)
	install -d $(share_path)
	@for file in $(SCRIPTS); do \
            echo "  installing $$file"; \
            install -m 755 $$file $(install_path) || exit 1; \
            ln -sf $(link_install_source_path)/$$file $(link_install_path)/$$file; \
        done;
	@for file in $(SCRIPT_IMPORTS); do \
            echo "  installing $$file"; \
            install -m 644 $$file $(install_path) || exit 1; \
            ln -sf $(link_install_source_path)/$$file $(link_install_path)/$$file; \
        done;
	@for file in $(TEMPLATE); do \
            echo "  installing $$file"; \
            install -m 644 $$file $(share_path) || exit 1; \
            ln -sf $(link_share_source_path)/$$file $(link_share_path)/$$file; \
        done;

#-----------------------------------------------------------------------------
clean:
