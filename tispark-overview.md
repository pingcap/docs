---
title: TiSpark User Guide
summary: Use TiSpark to provide an HTAP solution to serve as a one-stop solution for both online transactions and analysis.
---

# TiSpark User Guide

[TiSpark](https://github.com/pingcap/tispark) is a thin layer built for running Apache Spark on top of TiDB/TiKV to answer the complex OLAP queries. It takes advantages of both the Spark platform and the distributed TiKV cluster and seamlessly glues to TiDB, the distributed OLTP database, to provide a Hybrid Transactional/Analytical Processing (HTAP) solution to serve as a one-stop solution for both online transactions and analysis.

<<<<<<< HEAD
TiSpark depends on the TiKV cluster and the PD cluster. You also need to set up a Spark cluster. This document provides a brief introduction to how to setup and use TiSpark. It requires some basic knowledge of Apache Spark. For more information, see [Spark website](https://spark.apache.org/docs/latest/index.html).
=======
[TiFlash](/tiflash/tiflash-overview.md) is another tool that enables HTAP. Both TiFlash and TiSpark allow the use of multiple hosts to execute OLAP queries on OLTP data. TiFlash stores data in a columnar format, which allows more efficient analytical queries. TiFlash and TiSpark can be used together.

TiSpark depends on the TiKV cluster and the PD cluster. You also need to set up a Spark cluster. This document provides a brief introduction to how to setup and use TiSpark. It requires some basic knowledge of Apache Spark. For more information, see [Apache Spark website](https://spark.apache.org/docs/latest/index.html).
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))

## Overview

TiSpark is an OLAP solution that runs Spark SQL directly on TiKV, the distributed storage engine.

<<<<<<< HEAD
![TiSpark architecture](/media/tispark-architecture.png)

+ TiSpark integrates with Spark Catalyst Engine deeply. It provides precise control of the computing, which allows Spark read data from TiKV efficiently. It also supports index seek, which improves the performance of the point query execution significantly.
+ It utilizes several strategies to push down the computing to reduce the size of dataset handling by Spark SQL, which accelerates the query execution. It also uses the TiDB built-in statistical information for the query plan optimization.
+ From the data integration point of view, TiSpark and TiDB serve as a solution for running both transaction and analysis directly on the same platform without building and maintaining any ETLs. It simplifies the system architecture and reduces the cost of maintenance.
+ You can deploy and utilize tools from the Spark ecosystem for further data processing and manipulation on TiDB. For example, using TiSpark for data analysis and ETL; retrieving data from TiKV as a machine learning data source; generating reports from the scheduling system and so on.
+ Also, TiSpark supports distributed writes to TiKV. Compared to using Spark combined with JDBC to write to TiDB, distributed writes to TiKV can implement transactions (either all data are written successfully or all writes fail), and the writes are faster.
=======
- TiSpark: Data analysis and ETLs
- TiKV: Data retrieval
- Scheduling system: Report generation

Also, TiSpark supports distributed writes to TiKV. Compared with writes to TiDB by using Spark and JDBC, distributed writes to TiKV can implement transactions (either all data are written successfully or all writes fail), and the writes are faster.

> **Warning:**
>
> Because TiSpark accesses TiKV directly, the access control mechanisms used by TiDB Server are not applicable to TiSpark. Since TiSpark v2.5.0, TiSpark supports user authentication and authorization, for more information, see [Security](/tispark-overview.md#security).
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))

## Environment setup

+ The TiSpark 2.x supports Spark 2.3.x and Spark 2.4.x. If you want to use Spark 2.1.x, use TiSpark 1.x instead.
+ TiSpark requires JDK 1.8+ and Scala 2.11 (Spark2.0 + default Scala version).
+ TiSpark runs in any Spark mode such as YARN, Mesos, and Standalone.

## Recommended configuration

<<<<<<< HEAD
This section describes the configuration of independent deployment of TiKV and TiSpark, independent deployment of Spark and TiSpark, and hybrid deployment of TiKV and TiSpark.
=======
This section describes the recommended configuration of independent deployment of TiKV and TiSpark, independent deployment of Spark and TiSpark, and co-deployed TiKV and TiSpark.

See also [TiSpark Deployment Topology](/tispark-deployment-topology.md) for more details about how to deploy TiSpark using TiUP.
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))

### Configuration of independent deployment of TiKV and TiSpark

For independent deployment of TiKV and TiSpark, it is recommended to refer to the following recommendations:

+ Hardware configuration
    - For general purposes, refer to the TiDB and TiKV hardware configuration [recommendations](/hardware-and-software-requirements.md#development-and-test-environments).
    - If the usage is more focused on the analysis scenarios, you can increase the memory of the TiKV nodes to at least 64G.

### Configuration of independent deployment of Spark and TiSpark

See the [Spark official website](https://spark.apache.org/docs/latest/hardware-provisioning.html) for the detail hardware recommendations. The following is a short overview of TiSpark configuration:

- It is recommended to allocate 32G memory for Spark, and reserve at least 25% of the memory for the operating system and buffer cache.

- It is recommended to provision at least 8 to 16 cores on per machine for Spark. Initially, you can assign all the CPU cores to Spark.

See the [official configuration](https://spark.apache.org/docs/latest/spark-standalone.html) on the Spark website. The following is an example based on the `spark-env.sh` configuration:

```sh
SPARK_EXECUTOR_CORES: 5
SPARK_EXECUTOR_MEMORY: 10g
SPARK_WORKER_CORES: 5
SPARK_WORKER_MEMORY: 10g
```

<<<<<<< HEAD
In the `spark-defaults.conf` file, add the following lines:

```sh
spark.tispark.pd.addresses $your_pd_servers
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

Add the following configuration in the `CDH` spark version:

```
spark.tispark.pd.addresses=$your_pd_servers
spark.sql.extensions=org.apache.spark.sql.TiExtensions
```

`your_pd_servers` are comma-separated PD addresses, with each in the format of `$your_pd_address:$port`.

For example, when you have multiple PD servers on `10.16.20.1,10.16.20.2,10.16.20.3` with the port 2379, put it as `10.16.20.1:2379,10.16.20.2:2379,10.16.20.3:2379`.

### Configuration of hybrid deployment of TiKV and TiSpark

For the hybrid deployment of TiKV and TiSpark, add TiSpark required resources to the TiKV reserved resources, and allocate 25% of the memory for the system.

=======
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))
## Deploy the TiSpark cluster

Download TiSpark's jar package [here](https://github.com/pingcap/tispark/releases). Download your desired version of jar package and copy the content to the appropriate folder.

### Deploy TiSpark on the existing Spark cluster

<<<<<<< HEAD
Running TiSpark on an existing Spark cluster does not require a reboot of the cluster. You can use Spark's `--jars` parameter to introduce TiSpark as a dependency:

```sh
spark-shell --jars $TISPARK_FOLDER/tispark-${name_with_version}.jar
```

### Deploy TiSpark without the Spark cluster

If you do not have a Spark cluster, we recommend using the standalone mode. To use the Spark Standalone model, you can simply place a compiled version of Spark on each node of the cluster. If you encounter problems, see its [official website](https://spark.apache.org/docs/latest/spark-standalone.html). And you are welcome to [file an issue](https://github.com/pingcap/tispark/issues/new) on our GitHub.
=======
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
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))

#### Download and install

<<<<<<< HEAD
You can download [Apache Spark](https://spark.apache.org/downloads.html)

For the Standalone mode without Hadoop support, use Spark **2.3.x** and any version of Pre-build with Apache Hadoop 2.x with Hadoop dependencies. If you need to use the Hadoop cluster, choose the corresponding Hadoop version. You can also choose to build from the [source code](https://spark.apache.org/docs/latest/building-spark.html) to match the previous version of the official Hadoop 2.x.

Suppose you already have a Spark binaries, and the current PATH is `SPARKPATH`, you can copy the TiSpark jar package to the `${SPARKPATH}/jars` directory.
=======
```
spark.tispark.pd.addresses $pd_host:$pd_port
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

The `spark.tispark.pd.addresses` configuration allows you to put in multiple PD servers. Specify the port number for each of them. For example, when you have multiple PD servers on `10.16.20.1,10.16.20.2,10.16.20.3` with the port 2379, put it as `10.16.20.1:2379,10.16.20.2:2379,10.16.20.3:2379`.
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))

> **Note:**
>
> If TiSpark could not communicate properly, please check your firewall configuration. You can adjust the firewall rules or disable it on your need.

<<<<<<< HEAD
#### Start a Master node

Execute the following command on the selected Spark Master node:

```sh
cd $SPARKPATH

./sbin/start-master.sh
```

After the above step is completed, a log file will be printed on the screen. Check the log file to confirm whether the Spark-Master is started successfully. You can open the <http://${spark-master-hostname}:8080> to view the cluster information (if you does not change the Spark-Master default port number). When you start Spark-Worker, you can also use this panel to confirm whether the Worker is joined to the cluster.

#### Start a Worker node

Similarly, you can start a Spark-Worker node with the following command:

```sh
./sbin/start-slave.sh spark://${spark-master-hostname}:7077
```

After the command returns, you can see if the Worker node is joined to the Spark cluster correctly from the panel as well. Repeat the above command at all Worker nodes. After all Workers are connected to the master, you have a Standalone mode Spark cluster.

#### Spark SQL shell and JDBC server

TiSpark supports Spark 2.3, so you can use Spark's ThriftServer and SparkSQL directly.
=======
### Deploy TiSpark on an existing Spark cluster

Running TiSpark on an existing Spark cluster does not require a reboot of the cluster. You can use Spark's `--jars` parameter to introduce TiSpark as a dependency:

{{< copyable "shell-regular" >}}

```shell
spark-shell --jars $TISPARK_FOLDER/tispark-${name_with_version}.jar
```

### Deploy TiSpark without a Spark cluster

If you do not have a Spark cluster, we recommend using the standalone mode. For more information, see [Spark Standalone](https://spark.apache.org/docs/latest/spark-standalone.html). If you encounter any problem, see [Spark official website](https://spark.apache.org/docs/latest/spark-standalone.html). And you are welcome to [file an issue](https://github.com/pingcap/tispark/issues/new) on our GitHub.

## Use Spark Shell and Spark SQL
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))

## Demo

<<<<<<< HEAD
Assuming that you have successfully started the TiSpark cluster as described above, here's a quick introduction to how to use Spark SQL for OLAP analysis. Here we use a table named `lineitem` in the `tpch` database as an example.
=======
To generate the test data via a TiDB server available on `192.168.1.101`:

{{< copyable "shell-regular" >}}

```shell
tiup bench tpch prepare --host 192.168.1.101 --user root
```
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))

Assuming that your PD node is located at `192.168.1.100`, port `2379`, add the following command to `$SPARK_HOME/conf/spark-defaults.conf`:

{{< copyable "" >}}

```
spark.tispark.pd.addresses 192.168.1.100:2379
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

<<<<<<< HEAD
And then enter the following command in the Spark-Shell as in native Apache Spark:
=======
Start the Spark Shell:

{{< copyable "shell-regular" >}}

```shell
./bin/spark-shell
```

And then enter the following command in the Spark Shell as in native Apache Spark:
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))

{{< copyable "" >}}

<<<<<<< HEAD
spark.sql("select count(*)from lineitem").show
=======
```scala
spark.sql("use tpch")
spark.sql("select count(*) from lineitem").show
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))
```

The result is:

```
+-------------+
| Count (1) |
+-------------+
| 600000000 |
+-------------+
```

<<<<<<< HEAD
Spark SQL Interactive shell remains the same:
=======
Besides Spark Shell, there is also Spark SQL available. To use Spark SQL, run:

{{< copyable "shell-regular" >}}

```shell
./bin/spark-sql
```

You can run the same query:
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))

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

<<<<<<< HEAD
For JDBC connection with Thrift Server, you can try it with various JDBC supported tools including SQuirreLSQL and hive-beeline. For example, to use it with beeline:

```sh
./beeline
Beeline version 1.2.2 by Apache Hive
beeline> !connect jdbc:hive2://localhost:10000

=======
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
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))
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
update mysql.tidb set VARIABLE_VALUE="6h" where VARIABLE_NAME="tikv_gc_life_time";
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

It is recommended to set `isolationLevel` to `NONE` to avoid large single transactions which might potentially lead to TiDB OOM.

> **Note:**
>
> When you use JDBC, the default value of `isolationLevel` is `READ_UNCOMMITTED`, which causes the error of unsupported isolation level transactions. It is recommended to set the value of `isolationLevel` to `NONE`.

## Statistics information

TiSpark uses TiDB statistic information for the following items:

1. Determining which index to ues in your query plan with the estimated lowest cost.
2. Small table broadcasting, which enables efficient broadcast join.

If you would like TiSpark to use statistic information, first you need to make sure that concerning tables have already been analyzed. Read more about [how to analyze tables](/statistics.md).

Starting from TiSpark 2.0, statistics information is default to auto load.

<<<<<<< HEAD
## FAQ
=======
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
>>>>>>> 2f099ab90 (Delete the description of installing and deploying Spark (#8328))

Q: What are the pros/cons of independent deployment as opposed to a shared resource with an existing Spark / Hadoop cluster?

A: You can use the existing Spark cluster without a separate deployment, but if the existing cluster is busy, TiSpark will not be able to achieve the desired speed.

Q: Can I mix Spark with TiKV?

A: If TiDB and TiKV are overloaded and run critical online tasks, consider deploying TiSpark separately. You also need to consider using different NICs to ensure that OLTP's network resources are not compromised and affect online business. If the online business requirements are not high or the loading is not large enough, you can consider mixing TiSpark with TiKV deployment.

Q: What can I do if `warning：WARN ObjectStore:568 - Failed to get database` is returned when executing SQL statements using TiSpark?

A: You can ignore this warning. It occurs because Spark tries to load two nonexistent databases (`default` and `global_temp`) in its catalog. If you want to mute this warning, modify [log4j](https://github.com/pingcap/tidb-docker-compose/blob/master/tispark/conf/log4j.properties#L43) by adding `log4j.logger.org.apache.hadoop.hive.metastore.ObjectStore=ERROR` to the `log4j` file in `tispark/conf`. You can add the parameter to the `log4j` file of the `config` under Spark. If the suffix is `template`, you can use the `mv` command to change it to `properties`.

Q: What can I do if `java.sql.BatchUpdateException: Data Truncated` is returned when executing SQL statements using TiSpark?

A: This error occurs because the length of the data written exceeds the length of the data type defined by the database. You can check the field length and adjust it accordingly.

Q: Does TiSpark read Hive metadata by default?

A: By default, TiSpark searches for the Hive database by reading the Hive metadata in hive-site. If the search task fails, it searches for the TiDB database instead, by reading the TiDB metadata.

If you do not need this default behavior, do not configure the Hive metadata in hive-site.

Q: What can I do if `Error：java.io.InvalidClassException: com.pingcap.tikv.region.TiRegion; local class incompatible: stream classdesc serialVersionUID ...` is returned when TiSpark is executing a Spark task?

A: The error message shows a `serialVersionUID` conflict, which occurs because you have used `class` and `TiRegion` of different versions. Because `TiRegion` only exists in TiSpark, multiple versions of TiSpark packages might be used. To fix this error, you need to make sure the version of TiSpark dependency is consistent among all nodes in the cluster.
