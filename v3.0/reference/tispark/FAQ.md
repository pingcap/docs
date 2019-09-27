---
title: TiSpark FAQ
summary: Learn about the frequently asked questions (FAQs) and answers about TiSpark.
category: reference
---

## TiSpark FAQ

Q: What are the pros and cons of independent deployment as opposed to a shared resource with an existing Spark / Hadoop cluster?

A: You can use the existing Spark cluster without a separate deployment, but if the existing cluster is busy, TiSpark will not be able to achieve the desired speed.

Q: Can I mix Spark with TiKV?

A: If TiDB and TiKV are overloaded and run critical online tasks, consider deploying TiSpark separately.

You also need to consider using different NICs to ensure that OLTP's network resources are not compromised so that online business is not affected.

If the online business requirements are not high or the loading is not large enough, you can mix TiSpark with TiKV deployment.

Q: What can I do if `warning：WARN ObjectStore:568 - Failed to get database` is returned when executing SQL statements using TiSpark?

A: You can ignore this warning. It occurs because Spark tries to load two nonexistent databases (`default` and `global_temp`) in its catalog. If you want to mute this warning, modify [log4j](https://github.com/pingcap/tidb-docker-compose/blob/master/tispark/conf/log4j.properties#L43) by adding `log4j.logger.org.apache.hadoop.hive.metastore.ObjectStore=ERROR` to the `log4j` file in `tispark/conf`. You can add the parameter to the `log4j` file of the `config` under Spark. If the suffix is `template`, you can use the `mv` command to change it to `properties`.

Q: What can I do if `java.sql.BatchUpdateException: Data Truncated` is returned when executing SQL statements using TiSpark?

A: This error occurs because the length of the data written exceeds the length of the data type defined by the database. You can check the field length and adjust it accordingly.

Q: How to use PySpark with TiSpark?

A: Follow [TiSpark on PySpark](https://github.com/pingcap/tispark/blob/master/python/README.md) or [TiSpark on PySpark for Spark 2.1](https://github.com/pingcap/tispark/blob/master/python/README_spark2.1.md).

Q: How to use SparkR with TiSpark?

A: Follow [TiSpark on SparkR](https://github.com/pingcap/tispark/blob/master/R/README.md).
