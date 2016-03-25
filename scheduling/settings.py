# The maximum number of jobs Hadoop should be able to run at once.
# This is needed so that the job tracker doesn't exceed resource limits.
# This also affects our level of service to end users.
# We are submitting batches of 25 every minute, so 25 * 50 = 1250 scenes.
# This means it will take a little over an hour to addres an item ordered
# because the hadoop queue will be 25 * 50 scenes deep.
HADOOP_MAX_JOBS = 50


# Set the hadoop timeouts to a ridiculous number so jobs don't get killed
# before they are done
HADOOP_TIMEOUT = 172800000  # which is 2 days

# Specifies the hadoop queue to use based on priority
# 'all' must be present as it is used in the cron code to pass 'None' instead
HADOOP_QUEUE_MAPPING = {
    'all': 'ondemand',
    'low': 'ondemand-low',
    'normal': 'ondemand',
    'high': 'ondemand-high'
}
