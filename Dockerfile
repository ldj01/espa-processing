FROM dev/espa:latest


COPY . /usr/local/src/espa-processing
WORKDIR /usr/local/src/espa-processing

RUN cd espa-reprojection \
    && make install

RUN REPO_NAME=espa-product-formatter \
    && REPO_TAG=dev_v1.14.0 \
    && cd $SRC_DIR \
    && git clone git://github.com/USGS-EROS/${REPO_NAME}.git ${REPO_NAME} \
    && cd ${REPO_NAME} \
    && git checkout ${REPO_TAG} \
    && make BUILD_STATIC=yes ENABLE_THREADING=yes \
    && make install \
    && cd $SRC_DIR \
    && rm -rf ${REPO_NAME}


RUN mkdir -p /root/.usgs/espa/  \
	&& cp scheduling/example_cron.conf ~/.usgs/espa/cron.conf \
	&& cp scheduling/example_processing.conf ~/.usgs/espa/processing.conf

ENTRYPOINT ["/usr/bin/bash", "run_goes.sh"]
#ENTRYPOINT ["/usr/bin/bash"]
