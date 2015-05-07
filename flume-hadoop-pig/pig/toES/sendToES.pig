REGISTER '/usr/lib/pig/piggybank.jar' ;
REGISTER '/usr/lib/pig/lib/avro-*.jar';
REGISTER '/usr/lib/pig/lib/jackson-*.jar';
REGISTER '/usr/lib/pig/lib/json-*.jar';
REGISTER '/usr/lib/pig/lib/jython-*.jar';
REGISTER '/usr/lib/pig/lib/snappy-*.jar';

REGISTER '/usr/lib/pig/lib/elasticsearch-hadoop-*.jar';

define EsStorage org.elasticsearch.hadoop.pig.EsStorage('es.nodes=http://uct2-es-head.mwt2.org:9200');

-- RECS = LOAD 'xAODcollector' as (CRTIME: long,  PRODSOURCELABEL:chararray, times:bag{tuple(state:chararray, time:long)}, SORTED:int);
-- L = LIMIT RECS 100; dump L;
-- STORE L INTO 'xAOD-test/xAOD-test_record' USING EsStorage();


RECS = LOAD 'tests' USING PigStorage AS (F:int,S:int,T:int,N:chararray);
--dump RECS;
STORE RECS INTO 'xAOD-test/xAOD-test_record' USING EsStorage();