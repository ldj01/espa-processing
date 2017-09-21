rm -f ./*.log

python scheduling/ondemand_cron.py --priority all --limit 1 --product-types abi 2> /dev/null | python processing/ondemand_mapper.py --developer
cat espa-*.log \
	&& curl some-api:4004/production-api/v0/reset-status \
	&& curl some-api:4004/production-api/v0/handle-orders

# If you want a shell:
#/bin/bash

ls ./espa-jbrinkmann*/*.tar.gz && (echo "YES!"; /bin/bash; ) || echo 'nope!'
