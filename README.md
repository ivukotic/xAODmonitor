xAODmonitor
===========

based on flume collector, hdfs storage, pig cleanup, pig Hadoop2ES interface, ES+Kibana analytics

running on hadoop-dev.mwt2.org

Flume 
-----------------------
listens on 18080.
Starts like this: 
flume-ng agent -c flume -f flumeCollector/collector.properties -n summaryAgent -C '/home/ivukotic/xAODmonitor/flume-hadoop-pig/flumeCollector'

in production like this:
/etc/init.d/flume-collector-pig restart

logs are in:
/var/log/flume-ng-pig.log
