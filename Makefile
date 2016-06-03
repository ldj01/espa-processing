#-----------------------------------------------------------------------------
# Makefile
#
# Simple makefile for installing espa-processing.
#-----------------------------------------------------------------------------
.PHONY: check-environment all install clean

include make.config

all:

install: check-environment
	echo "make install in processing"; \
        (cd processing; $(MAKE) install);

clean:

#-----------------------------------------------------------------------------
check-environment:
ifndef PREFIX
    $(error Environment variable PREFIX is not defined)
endif

