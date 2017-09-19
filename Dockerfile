FROM dev/espa:latest


COPY . /usr/local/src/espa-processing
WORKDIR /usr/local/src/espa-processing

RUN mkdir -p /root/.usgs/espa/  \
	&& cp scheduling/example_cron.conf ~/.usgs/espa/cron.conf \
	&& cp scheduling/example_processing.conf ~/.usgs/espa/processing.conf

ENTRYPOINT ["/usr/bin/bash", "run_goes.sh"]
