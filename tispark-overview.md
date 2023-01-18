---
title: TiSpark User Guide
summary: Use TiSpark to provide an HTAP solution to serve as a one-stop solution for both online transactions and analysis.
---

# TiSpark User Guide

![TiSpark architecture](/media/tispark-architecture.png)

[TiSpark](https://github.com/pingcap/tispark) is a thin layer built for running Apache Spark on top of TiDB/TiKV to answer the complex OLAP queries. It takes advantages of both the Spark platform and the distributed TiKV cluster and seamlessly glues to TiDB, the distributed OLTP database, to provide a Hybrid Transactional/Analytical Processing (HTAP) solution to serve as a one-stop solution for both online transactions and analysis.

[TiFlash](/tiflash/tiflash-overview.md) is another tool that enables HTAP. Both TiFlash and TiSpark allow the use of multiple hosts to execute OLAP queries on OLTP data. TiFlash stores data in a columnar format, which allows more efficient analytical queries. TiFlash and TiSpark can be used together.

TiSpark depends on the TiKV cluster and the PD cluster. You also need to set up a Spark cluster. This document provides a brief introduction to how to setup and use TiSpark. It requires some basic knowledge of Apache Spark. For more information, see [Apache Spark website](https://spark.apache.org/docs/latest/index.html).

Deeply integrating with Spark Catalyst Engine, TiSpark provides precise control on computing. This allows Spark to read data from TiKV efficiently. TiSpark also supports index seek, which enables high-speed point query.

TiSpark accelerates data queries by pushing computing to TiKV so as to reduce the volume of data to be processed by Spark SQL. Meanwhile, TiSpark can use TiDB built-in statistics to select the best query plan.

With TiSpark and TiDB, you can run both transaction and analysis tasks on the same platform without building and maintaining ETLs. This simplifies the system architecture and reduces the cost of maintenance.

You can use tools of the Spark ecosystem for data processing on TiDB:

- TiSpark: Data analysis and ETLs
- TiKV: Data retrieval
- Scheduling system: Report generation

Also, TiSpark supports distributed writes to TiKV. Compared with writes to TiDB by using Spark and JDBC, distributed writes to TiKV can implement transactions (either all data are written successfully or all writes fail), and the writes are faster.

> **Warning:**
>
> Because TiSpark accesses TiKV directly, the access control mechanisms used by TiDB Server are not applicable to TiSpark. Since TiSpark v2.5.0, TiSpark supports user authentication and authorization, for more information, see [Security](/tispark-overview.md#security).

## Environment setup

The following table lists the compatibility information of the supported TiSpark versions. You can choose a TiSpark version according to your need.

| TiSpark version | TiDB, TiKV, and PD versions | Spark version | Scala version |
| ---------------  | -------------------- | -------------  | ------------- |
| 2.4.x-scala_2.11 | 5.x, 4.x             | 2.3.x, 2.4.x    | 2.11          |
| 2.4.x-scala_2.12 | 5.x, 4.x             | 2.4.x           | 2.12          |
| 2.5.x            | 5.x, 4.x             | 3.0.x, 3.1.x    | 2.12           |
| 3.0.x            | 5.x, 4.x             | 3.0.x, 3.1.x, 3.2.x | 2.12            |

TiSpark runs in any Spark mode such as YARN, Mesos, and Standalone.

## Recommended configuration

This section describes the recommended configuration of independent deployment of TiKV and TiSpark, independent deployment of Spark and TiSpark, and co-deployed TiKV and TiSpark.

See also [TiSpark Deployment Topology](/tispark-deployment-topology.md) for more details about how to deploy TiSpark using TiUP.

### Configuration of independent deployment of TiKV and TiSpark

For independent deployment of TiKV and TiSpark, it is recommended to refer to the following recommendations:

+ Hardware configuration
    - For general purposes, refer to the TiDB and TiKV hardware configuration [recommendations](/hardware-and-software-requirements.md#development-and-test-environments).
    - If the usage is more focused on the analysis scenarios, you can increase the memory of the TiKV nodes to at least 64G.

### Configuration of independent deployment of Spark and TiSpark

See the [Spark official website](https://spark.apache.org/docs/latest/hardware-provisioning.html) for the detail hardware recommendations. The following is a short overview of TiSpark configuration:

- It is recommended to allocate 32G memory for Spark, and reserve at least 25% of the memory for the operating system and buffer cache.

- It is recommended to provision at least 8 to 16 cores on per machine for Spark. Initially, you can assign all the CPU cores to Spark.

### Configuration of co-deployed TiKV and TiSpark

To co-deploy TiKV and TiSpark, add TiSpark required resources to the TiKV reserved resources, and allocate 25% of the memory for the system.

## Deploy the TiSpark cluster

Download TiSpark's jar package [here](https://github.com/pingcap/tispark/releases) and place it in the `$SPARKPATH/jars` folder.

> **Note:**
>
> TiSpark v2.1.x and older versions have file names that look like `tispark-core-2.1.9-spark_2.4-jar-with-dependencies.jar`. Please check the [releases page on GitHub](https://github.com/pingcap/tispark/releases) for the exact file name for the version you want.

The following is a short example of how to install TiSpark v2.4.1:

{{< copyable "shell-regular" >}}

```shell
wget https://github.com/pingcap/tispark/releases/download/v2.4.1/tispark-assembly-2.4.1.jar
mv tispark-assembly-2.4.1.jar $SPARKPATH/jars/
```

Copy the `spark-defaults.conf` from the `spark-defaults.conf.template` file:

{{< copyable "shell-regular" >}}

```shell
cp conf/spark-defaults.conf.template conf/spark-defaults.conf
```

In the `spark-defaults.conf` file, add the following lines:

```
spark.tispark.pd.addresses $pd_host:$pd_port
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

The `spark.tispark.pd.addresses` configuration allows you to put in multiple PD servers. Specify the port number for each of them. For example, when you have multiple PD servers on `10.16.20.1,10.16.20.2,10.16.20.3` with the port 2379, put it as `10.16.20.1:2379,10.16.20.2:2379,10.16.20.3:2379`.

> **Note:**
>
> If TiSpark could not communicate properly, please check your firewall configuration. You can adjust the firewall rules or disable it on your need.

### Deploy TiSpark on an existing Spark cluster

Running TiSpark on an existing Spark cluster does not require a reboot of the cluster. You can use Spark's `--jars` parameter to introduce TiSpark as a dependency:

{{< copyable "shell-regular" >}}

```shell
spark-shell --jars $TISPARK_FOLDER/tispark-${name_with_version}.jar
```

### Deploy TiSpark without a Spark cluster

If you do not have a Spark cluster, we recommend using the standalone mode. For more information, see [Spark Standalone](https://spark.apache.org/docs/latest/spark-standalone.html). If you encounter any problem, see [Spark official website](https://spark.apache.org/docs/latest/spark-standalone.html). And you are welcome to [file an issue](https://github.com/pingcap/tispark/issues/new) on our GitHub.

## Use Spark Shell and Spark SQL

Assume that you have successfully started the TiSpark cluster as described above. The following describes how to use Spark SQL for OLAP analysis on a table named `lineitem` in the `tpch` database.

To generate the test data via a TiDB server available on `192.168.1.101`:

{{< copyable "shell-regular" >}}

```shell
tiup bench tpch prepare --host 192.168.1.101 --user root
```

Assuming that your PD node is located at `192.168.1.100`, port `2379`, add the following command to `$SPARK_HOME/conf/spark-defaults.conf`:

{{< copyable "" >}}

```
spark.tispark.pd.addresses 192.168.1.100:2379
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

Start the Spark Shell:

{{< copyable "shell-regular" >}}

```shell
./bin/spark-shell
```

And then enter the following command in the Spark Shell as in native Apache Spark:

{{< copyable "" >}}

```scala
spark.sql("use tpch")
spark.sql("select count(*) from lineitem").show
```

The result is:

```
+-------------+
| Count (1) |
+-------------+
| 2000      |
+-------------+
```

Besides Spark Shell, there is also Spark SQL available. To use Spark SQL, run:

{{< copyable "shell-regular" >}}

```shell
./bin/spark-sql
```

You can run the same query:

{{< copyable "" >}}

```scala
use tpch;
select count(*) from lineitem;
```

The result is:

```
2000
Time taken: 0.673 seconds, Fetched 1 row(s)
```

## Use JDBC support with ThriftServer

You can use Spark Shell or Spark SQL without JDBC support. However, JDBC support is required for tools like beeline. JDBC support is provided by Thrift server. To use Spark's Thrift server, run:

{{< copyable "shell-regular" >}}

```shell
./sbin/start-thriftserver.sh
```

To connect JDBC with Thrift server, you can use JDBC supported tools including beeline.

For example, to use it with beeline:

{{< copyable "shell-regular" >}}

```shell
./bin/beeline jdbc:hive2://localhost:10000
```

If the following message is displayed, you have enabled beeline successfully.

```
Beeline version 1.2.2 by Apache Hive
```

Then, you can run the query command:

```
1: jdbc:hive2://localhost:10000> use testdb;
+---------+--+
| Result  |
+---------+--+
+---------+--+
No rows selected (0.013 seconds)

select count(*) from account;
+-----------+--+
| count(1)  |
+-----------+--+
| 1000000   |
+-----------+--+
1 row selected (1.97 seconds)
```

## Use TiSpark together with Hive

You can use TiSpark together with Hive. Before starting Spark, you need to set the `HADOOP_CONF_DIR` environment variable to your Hadoop configuration folder and copy `hive-site.xml` to the `spark/conf` folder.

```scala
val tisparkDF = spark.sql("select * from tispark_table").toDF
tisparkDF.write.saveAsTable("hive_table") // save table to hive
spark.sql("select * from hive_table a, tispark_table b where a.col1 = b.col1").show // join table across Hive and Tispark
```

## Batch write DataFrames into TiDB using TiSpark

Starting from v2.3, TiSpark natively supports batch writing DataFrames into TiDB clusters. This writing mode is implemented through the two-phase commit protocol of TiKV.

Compared with the writing through Spark + JDBC, the TiSpark batch writing has the following advantages:

|  Aspects to compare    | TiSpark batch writes | Spark + JDBC writes|
| ------- | --------------- | --------------- |
| Atomicity   | The DataFrames either are all written successfully or all fail to write. | If the Spark task fails and exits during the writing process, a part of the data might be written successfully. |
| Isolation   | During the writing process, the data being written is invisible to other transactions. | During the writing process, some successfully written data is visible to other transactions.  |
| Error recovery | If the batch write fails, you only need to re-run Spark. | An application is required to achieve idempotence. For example, if the batch write fails, you need to clean up the part of the successfully written data and re-run Spark. You need to set `spark.task.maxFailures=1` to prevent data duplication caused by task retry. |
| Speed    | Data is directly written into TiKV, which is faster. | Data is written to TiKV through TiDB, which affects the speed. |

The following example shows how to batch write data using TiSpark via the scala API:

```scala
// select data to write
val df = spark.sql("select * from tpch.ORDERS")

// write data to tidb
df.write.
  format("tidb").
  option("tidb.addr", "127.0.0.1").
  option("tidb.port", "4000").
  option("tidb.user", "root").
  option("tidb.password", "").
  option("database", "tpch").
  option("table", "target_orders").
  mode("append").
  save()
```

If the amount of data to write is large and the writing time exceeds ten minutes, you need to ensure that the GC time is longer than the writing time.

```sql
UPDATE mysql.tidb SET VARIABLE_VALUE="6h" WHERE VARIABLE_NAME="tikv_gc_life_time";
```

Refer to [this document](https://github.com/pingcap/tispark/blob/master/docs/datasource_api_userguide.md) for details.

## Load Spark Dataframe into TiDB using JDBC

In addition to using TiSpark to batch write DataFrames into the TiDB cluster, you can also use Spark's native JDBC support for the data writing:

```scala
import org.apache.spark.sql.execution.datasources.jdbc.JDBCOptions

val customer = spark.sql("select * from customer limit 100000")
// You might repartition the source to make it balance across nodes
// and increase the concurrency.
val df = customer.repartition(32)
df.write
.mode(saveMode = "append")
.format("jdbc")
.option("driver", "com.mysql.jdbc.Driver")
 // Replace the host and port with that of your own and be sure to use the rewrite batch
.option("url", "jdbc:mysql://127.0.0.1:4000/test?rewriteBatchedStatements=true")
.option("useSSL", "false")
// As tested, 150 is good practice
.option(JDBCOptions.JDBC_BATCH_INSERT_SIZE, 150)
.option("dbtable", s"cust_test_select") // database name and table name here
.option("isolationLevel", "NONE") // recommended to set isolationLevel to NONE if you have a large DF to load.
.option("user", "root") // TiDB user here
.save()
```

<<<<<<< HEAD
It is recommended to set `isolationLevel` to `NONE` to avoid large single transactions which might potentially lead to TiDB OOM.
=======
Set `isolationLevel` to `NONE` to avoid large single transactions which might lead to TiDB OOM and also avoid the `ISOLATION LEVEL does not support` error (TiDB currently only supports `REPEATABLE-READ`).

### Delete data using TiSpark

You can use Spark SQL to delete data from TiKV.

```
spark.sql("use tidb_catalog")
spark.sql("delete from ${database}.${table} where xxx")
```

See [delete feature](https://github.com/pingcap/tispark/blob/master/docs/features/delete_userguide.md) for more details.

### Work with other data sources

You can use multiple catalogs to read data from different data sources as follows:

```
// Read from Hive
spark.sql("select * from spark_catalog.default.t").show

// Join Hive tables and TiDB tables
spark.sql("select t1.id,t2.id from spark_catalog.default.t t1 left join tidb_catalog.test.t t2").show
```

## TiSpark configurations

The configurations in the following table can be put together with `spark-defaults.conf` or passed in the same way as other Spark configuration properties.

| Key                                             | Default value    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|-------------------------------------------------|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `spark.tispark.pd.addresses`                    | `127.0.0.1:2379` | The addresses of PD clusters, which are split by commas.                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `spark.tispark.grpc.framesize`                  | `2147483647`     | The maximum frame size of gRPC response in bytes (default to 2G).                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `spark.tispark.grpc.timeout_in_sec`             | `10`             | The gRPC timeout time in seconds.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `spark.tispark.plan.allow_agg_pushdown`         | `true`           | Whether aggregations are allowed to push down to TiKV (in case of busy TiKV nodes).                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `spark.tispark.plan.allow_index_read`           | `true`           | Whether index is enabled in planning (which might cause heavy pressure on TiKV).                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `spark.tispark.index.scan_batch_size`           | `20000`          | The number of row keys in a batch for the concurrent index scan.                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `spark.tispark.index.scan_concurrency`          | `5`              | The maximum number of threads for index scan that retrieves row keys (shared among tasks inside each JVM).                                                                                                                                                                                                                                                                                                                                                                                                              |
| `spark.tispark.table.scan_concurrency`          | `512`            | The maximum number of threads for table scan (shared among tasks inside each JVM).                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `spark.tispark.request.command.priority`        | `Low`            | The value options are `Low`, `Normal`, `High`. This setting impacts the resources allocated in TiKV. `Low` is recommended because the OLTP workload is not disturbed.                                                                                                                                                                                                                                                                                                                                                   |
| `spark.tispark.coprocess.codec_format`          | `chblock`        | Retain the default codec format for coprocessor. Available options are `default`, `chblock` and `chunk`.                                                                                                                                                                                                                                                                                                                                                                                                                |
| `spark.tispark.coprocess.streaming`             | `false`          | Whether to use streaming for response fetching (experimental).                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `spark.tispark.plan.unsupported_pushdown_exprs` |                  | A comma-separated list of expressions. In case you have a very old version of TiKV, you might disable the push down of some expressions if they are not supported.                                                                                                                                                                                                                                                                                                                                                      |
| `spark.tispark.plan.downgrade.index_threshold`  | `1000000000`     | If the range of index scan on one Region exceeds this limit in the original request, downgrade this Region's request to table scan rather than the planned index scan. By default, the downgrade is disabled.                                                                                                                                                                                                                                                                                                           |
| `spark.tispark.show_rowid`                      | `false`          | Whether to show row ID if the ID exists.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `spark.tispark.db_prefix`                       |                  | The string that indicates the extra prefix for all databases in TiDB. This string distinguishes the databases in TiDB from the Hive databases with the same name.                                                                                                                                                                                                                                                                                                                                                       |
| `spark.tispark.request.isolation.level`         | `SI`             | Whether to resolve locks for the underlying TiDB clusters. When you use the "RC", you get the latest version of the record smaller than your `tso` and ignore the locks. When you use "SI", you resolve the locks and get the records depending on whether the resolved lock is committed or aborted.                                                                                                                                                                                                                   |
| `spark.tispark.coprocessor.chunk_batch_size`    | `1024`           | Rows fetched from coprocessor.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `spark.tispark.isolation_read_engines`          | `tikv,tiflash`   | List of readable engines of TiSpark, comma separated. Storage engines not listed will not be read.                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `spark.tispark.stale_read`                      | optional         | The stale read timestamp(ms). See [here](https://github.com/pingcap/tispark/blob/master/docs/features/stale_read.md) for more details.                                                                                                                                                                                                                                                                                                                                                                                  |
| `spark.tispark.tikv.tls_enable`                 | `false`          | Whether to enable TiSpark TLS. 　                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `spark.tispark.tikv.trust_cert_collection`      |                  | The trusted certificate for TiKV Client, used for verifying the remote PD's certificate, for example, `/home/tispark/config/root.pem` The file should contain an X.509 certificate collection.                                                                                                                                                                                                                                                                                                                          |
| `spark.tispark.tikv.key_cert_chain`             |                  | An X.509 certificate chain file for TiKV Client, for example, `/home/tispark/config/client.pem`.                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `spark.tispark.tikv.key_file`                   |                  | A PKCS#8 private key file for TiKV Client, for example, `/home/tispark/client_pkcs8.key`.                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `spark.tispark.tikv.jks_enable`                 | `false`          | Whether to use the JAVA key store instead of the X.509 certificate.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `spark.tispark.tikv.jks_trust_path`             |                  | A JKS format certificate for TiKV Client, generated by `keytool`, for example, `/home/tispark/config/tikv-truststore`.                                                                                                                                                                                                                                                                                                                                                                                                  |
| `spark.tispark.tikv.jks_trust_password`         |                  | The password of `spark.tispark.tikv.jks_trust_path`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `spark.tispark.tikv.jks_key_path`               |                  | A JKS format key for TiKV Client, generated by `keytool`, for example, `/home/tispark/config/tikv-clientstore`.                                                                                                                                                                                                                                                                                                                                                                                                         |
| `spark.tispark.tikv.jks_key_password`           |                  | The password of `spark.tispark.tikv.jks_key_path`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `spark.tispark.jdbc.tls_enable`                 | `false`          | Whether to enable TLS when using the JDBC connector.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `spark.tispark.jdbc.server_cert_store`          |                  | The trusted certificate for JDBC. It is a Java keystore (JKS) format certificate generated by `keytool`, for example, `/home/tispark/config/jdbc-truststore`. The default value is "", which means TiSpark does not verify the TiDB server.                                                                                                                                                                                                                                                                             |
| `spark.tispark.jdbc.server_cert_password`       |                  | The password of `spark.tispark.jdbc.server_cert_store`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `spark.tispark.jdbc.client_cert_store`          |                  | A PKCS#12 certificate for JDBC. It is a JKS format certificate generated by `keytool`, for example, `/home/tispark/config/jdbc-clientstore`. Default is "", which means TiDB server doesn't verify TiSpark.                                                                                                                                                                                                                                                                                                             |
| `spark.tispark.jdbc.client_cert_password`       |                  | The password of `spark.tispark.jdbc.client_cert_store`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `spark.tispark.tikv.tls_reload_interval`        | `10s`            | The interval for checking if there is any reloading certificates. The default value is `10s` (10 seconds).                                                                                                                                                                                                                                                                                                                                                                                                              |
| `spark.tispark.tikv.conn_recycle_time`          | `60s`            | The interval for cleaning expired connections with TiKV. It takes effect only when certificate reloading is enabled. The default value is `60s` (60 seconds).                                                                                                                                                                                                                                                                                                                                                           |
| `spark.tispark.host_mapping`                    |                  | The route map used to configure the mapping between public IP addresses and intranet IP addresses. When the TiDB cluster is running on the intranet, you can map a set of intranet IP addresses to public IP addresses for an outside Spark cluster to access. The format is `{Intranet IP1}:{Public IP1};{Intranet IP2}:{Public IP2}`, for example, `192.168.0.2:8.8.8.8;192.168.0.3:9.9.9.9`.                                                                                                                         |
| `spark.tispark.new_collation_enable`            |                  | When [new collation](https://docs.pingcap.com/tidb/stable/character-set-and-collation#new-framework-for-collations) is enabled on TiDB, this configuration can be set to `true`. If `new collation` is not enabled on TiDB, this configuration can be set to `false`. If this item is not configured, TiSpark configures `new collation` automatically based on the TiDB version. The configuration rule is as follows: If the TiDB version is greater than or equal to v6.0.0, it is `true`; otherwise, it is `false`. |

### TLS configurations

TiSpark TLS has two parts: TiKV Client TLS and JDBC connector TLS. To enable TLS in TiSpark, you need to configure both. `spark.tispark.tikv.xxx` is used for TiKV Client to create a TLS connection with PD and TiKV server. `spark.tispark.jdbc.xxx` is used for JDBC to connect with TiDB server in TLS connection.

When TiSpark TLS is enabled, you must configure either the X.509 certificate with `tikv.trust_cert_collection`, `tikv.key_cert_chain` and `tikv.key_file` configurations, or the JKS certificate with `tikv.jks_enable`, `tikv.jks_trust_path` and `tikv.jks_key_path`. `jdbc.server_cert_store` and `jdbc.client_cert_store` are optional.

TiSpark only supports TLSv1.2 and TLSv1.3.

* The following is an example of opening TLS configuration with the X.509 certificate in TiKV Client.

```
spark.tispark.tikv.tls_enable                                  true
spark.tispark.tikv.trust_cert_collection                       /home/tispark/root.pem
spark.tispark.tikv.key_cert_chain                              /home/tispark/client.pem
spark.tispark.tikv.key_file                                    /home/tispark/client.key
```

* The following is an example of enabling TLS with JKS configurations in TiKV Client.

```
spark.tispark.tikv.tls_enable                                  true
spark.tispark.tikv.jks_enable                                  true
spark.tispark.tikv.jks_key_path                                /home/tispark/config/tikv-truststore
spark.tispark.tikv.jks_key_password                            tikv_trustore_password
spark.tispark.tikv.jks_trust_path                              /home/tispark/config/tikv-clientstore
spark.tispark.tikv.jks_trust_password                          tikv_clientstore_password
```

When both JKS and X.509 certificates are configured, JKS would have a higher priority. That means TLS builder will use JKS certificate first. Therefore, do not set `spark.tispark.tikv.jks_enable=true` when you just want to use a common PEM certificate.

* The following is an example of enabling TLS in JDBC connector.

```
spark.tispark.jdbc.tls_enable                                  true
spark.tispark.jdbc.server_cert_store                           /home/tispark/jdbc-truststore
spark.tispark.jdbc.server_cert_password                        jdbc_truststore_password
spark.tispark.jdbc.client_cert_store                           /home/tispark/jdbc-clientstore
spark.tispark.jdbc.client_cert_password                        jdbc_clientstore_password
```

- For details about how to open TiDB TLS, see [Enable TLS between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md).
- For details about how to generate a JAVA key store, see [Connecting Securely Using SSL](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-using-ssl.html).

### Log4j configuration

When you start `spark-shell` or `spark-sql` and run query, you might see the following warnings:

```
Failed to get database ****, returning NoSuchObjectException
Failed to get database ****, returning NoSuchObjectException
```

where `****` is the database name.

The warnings are benign and occurs because Spark cannot find `****` in its own catalog. You can just ignore these warnings.

To mute them, append the following text to `${SPARK_HOME}/conf/log4j.properties`.

```
# tispark disable "WARN ObjectStore:568 - Failed to get database"
log4j.logger.org.apache.hadoop.hive.metastore.ObjectStore=ERROR
```

### Time zone configuration

Set time zone by using the `-Duser.timezone` system property (for example, `-Duser.timezone=GMT-7`), which affects the `Timestamp` type.

Do not use `spark.sql.session.timeZone`.

## Features

The major features of TiSpark are as follows:

| Feature support                 | TiSpark 2.4.x | TiSpark 2.5.x | TiSpark 3.0.x | TiSpark 3.1.x |
|---------------------------------| ------------- | ------------- | ----------- |---------------|
| SQL select without tidb_catalog | ✔           | ✔           |             |               |
| SQL select with tidb_catalog    |               | ✔           | ✔         | ✔             |
| DataFrame append                | ✔           | ✔           | ✔         | ✔             |
| DataFrame reads                 | ✔           | ✔           | ✔         | ✔             |
| SQL show databases              | ✔           | ✔           | ✔         | ✔             |
| SQL show tables                 | ✔           | ✔           | ✔         | ✔             |
| SQL auth                        |               | ✔           | ✔         | ✔             |
| SQL delete                      |               |               | ✔         | ✔             |
| SQL insert                      |               |               |           | ✔              |
| TLS                             |               |               | ✔         | ✔             |
| DataFrame auth                  |               |               |             | ✔             |

### Support for expression index

TiDB v5.0 supports [expression index](/sql-statements/sql-statement-create-index.md#expression-index).

TiSpark currently supports retrieving data from tables with `expression index`, but the `expression index` will not be used by the planner of TiSpark.

### Work with TiFlash

TiSpark can read data from TiFlash via the configuration `spark.tispark.isolation_read_engines`.

### Support for partitioned tables

**Read partitioned tables from TiDB**

TiSpark can read the range and hash partitioned tables from TiDB.

Currently, TiSpark does not support a MySQL/TiDB partition table syntax `select col_name from table_name partition(partition_name)`. However, you can still use the `where` condition to filter the partitions.

TiSpark decides whether to apply partition pruning according to the partition type and the partition expression associated with the table.

TiSpark applies partition pruning on range partitioning only when the partition expression is one of the following:

+ column expression
+ `YEAR($argument)` where the argument is a column and its type is datetime or string literal that can be parsed as datetime.

If partition pruning is not applicable, TiSpark's reading is equivalent to doing a table scan over all partitions.

**Write into partitioned tables**

Currently, TiSpark only supports writing data into the range and hash partitioned tables under the following conditions:

+ The partition expression is a column expression.
+ The partition expression is `YEAR($argument)` where the argument is a column and its type is datetime or string literal that can be parsed as datetime.

There are two ways to write into partitioned tables:

- Use datasource API to write into partition table which supports replace and append semantics.
- Use delete statement with Spark SQL.
>>>>>>> d304b1f7b (Update JDBC information (#11916))

> **Note:**
>
> When you use JDBC, the default value of `isolationLevel` is `READ_UNCOMMITTED`, which causes the error of unsupported isolation level transactions. It is recommended to set the value of `isolationLevel` to `NONE`.

## Statistics information

TiSpark uses TiDB statistic information for the following items:

1. Determining which index to ues in your query plan with the estimated lowest cost.
2. Small table broadcasting, which enables efficient broadcast join.

If you would like TiSpark to use statistic information, first you need to make sure that concerning tables have already been analyzed. Read more about [how to analyze tables](/statistics.md).

Starting from TiSpark 2.0, statistics information is default to auto load.

## Security

If you are using TiSpark v2.5.0 or a later version, you can authenticate and authorize TiSpark users by using TiDB.

The authentication and authorization feature is disabled by default. To enable it, add the following configurations to the Spark configuration file `spark-defaults.conf`.

```
// Enable authentication and authorization
spark.sql.auth.enable true

// Configure TiDB information
spark.sql.tidb.addr $your_tidb_server_address
spark.sql.tidb.port $your_tidb_server_port
spark.sql.tidb.user $your_tidb_server_user
spark.sql.tidb.password $your_tidb_server_password
```

For more information, see [Authorization and authentication through TiDB server](https://github.com/pingcap/tispark/blob/master/docs/authorization_userguide.md).

> **Note:**
>
> After enabling the authentication and authorization feature, TiSpark Spark SQL can only use TiDB as the data source, so switching to other data sources (such as Hive) makes tables invisible.

## TiSpark FAQ

Q: What are the pros/cons of independent deployment as opposed to a shared resource with an existing Spark / Hadoop cluster?

A: You can use the existing Spark cluster without a separate deployment, but if the existing cluster is busy, TiSpark will not be able to achieve the desired speed.

Q: Can I mix Spark with TiKV?

A: If TiDB and TiKV are overloaded and run critical online tasks, consider deploying TiSpark separately. You also need to consider using different NICs to ensure that OLTP's network resources are not compromised and affect online business. If the online business requirements are not high or the loading is not large enough, you can consider mixing TiSpark with TiKV deployment.

Q: What can I do if `warning: WARN ObjectStore:568 - Failed to get database` is returned when executing SQL statements using TiSpark?

A: You can ignore this warning. It occurs because Spark tries to load two nonexistent databases (`default` and `global_temp`) in its catalog. If you want to mute this warning, modify [log4j](https://github.com/pingcap/tidb-docker-compose/blob/master/tispark/conf/log4j.properties#L43) by adding `log4j.logger.org.apache.hadoop.hive.metastore.ObjectStore=ERROR` to the `log4j` file in `tispark/conf`. You can add the parameter to the `log4j` file of the `config` under Spark. If the suffix is `template`, you can use the `mv` command to change it to `properties`.

Q: What can I do if `java.sql.BatchUpdateException: Data Truncated` is returned when executing SQL statements using TiSpark?

A: This error occurs because the length of the data written exceeds the length of the data type defined by the database. You can check the field length and adjust it accordingly.

Q: Does TiSpark read Hive metadata by default?

A: By default, TiSpark searches for the Hive database by reading the Hive metadata in hive-site. If the search task fails, it searches for the TiDB database instead, by reading the TiDB metadata.

If you do not need this default behavior, do not configure the Hive metadata in hive-site.

Q: What can I do if `Error: java.io.InvalidClassException: com.pingcap.tikv.region.TiRegion; local class incompatible: stream classdesc serialVersionUID ...` is returned when TiSpark is executing a Spark task?

A: The error message shows a `serialVersionUID` conflict, which occurs because you have used `class` and `TiRegion` of different versions. Because `TiRegion` only exists in TiSpark, multiple versions of TiSpark packages might be used. To fix this error, you need to make sure the version of TiSpark dependency is consistent among all nodes in the cluster.
