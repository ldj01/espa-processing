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
    distribution.py \
    environment.py \
    espa_exception.py \
    initialization.py \
    landsat_metadata.py \
    logging_tools.py \
    parameters.py \
    processor.py \
    sensor.py \
    settings.py \
    staging.py \
    statistics.py \
    transfer.py \
    utilities.py \
    warp.py

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
            install -m 755 $$file $(install_path); \
            ln -sf $(link_install_source_path)/$$file $(link_install_path)/$$file; \
        done;
	@for file in $(SCRIPT_IMPORTS); do \
            echo "  installing $$file"; \
            install -m 644 $$file $(install_path); \
            ln -sf $(link_install_source_path)/$$file $(link_install_path)/$$file; \
        done;
	@for file in $(TEMPLATE); do \
            echo "  installing $$file"; \
            install -m 644 $$file $(share_path); \
            ln -sf $(link_share_source_path)/$$file $(link_share_path)/$$file; \
        done;

#-----------------------------------------------------------------------------
clean:
