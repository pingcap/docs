---
title: TiSpark User Guide (after v2.0)
summary: Learn how to use TiSpark.
category: reference
---

# TiSpark User Guide (after v2.0)

> **Note:**
>
> This is a user guide for TiSpark version later than 2.0. If you are using version earlier than 2.0, refer to [Document for Spark 2.1](/v2.1/reference/tispark/userguide-spark2.1.md)

This document introduces how to deploy and use TiSpark, which requires some basic knowledge of Apache Spark. Refer to [Spark website](https://spark.apache.org/docs/latest/index.html) for details.

## Prerequisites for deploying TiSpark

+ For TiSpark to be compatible with Spark, refer to [Spark versions supported by TiSpark](/v2.1/reference/tispark/overview.md#spark-versions-supported-by-tiSpark).
+ TiSpark requires JDK 1.8+ and Scala 2.11 (Spark 2.0 + default Scala version).
+ TiSpark runs in any Spark mode such as `YARN`, `Mesos`, and `Standalone`.

### Configurations

This section describes the independent deployment of Spark and TiSpark, and hybrid deployment of TiKV and TiSpark.

#### Independent deployment of Spark cluster and TiSpark cluster

Refer to the [Spark official website](https://spark.apache.org/docs/latest/hardware-provisioning.html) for detailed hardware recommendations.

+ It is recommended to allocate 32G memory for Spark. Reserve at least 25% of the memory for the operating system and the buffer cache.

+ It is recommended to provision at least 8 to 16 cores per machine for Spark. First, you must assign all the CPU cores to Spark.

This is an example based on the `spark-env.sh` configuration:

```
SPARK_EXECUTOR_CORES: 5
SPARK_EXECUTOR_MEMORY: 10g
SPARK_WORKER_CORES: 5
SPARK_WORKER_MEMORY: 10g
```

Add the following lines in `spark-defaults.conf`.

```
spark.tispark.pd.addresses $your_pd_servers
spark.sql.extensions org.apache.spark.sql.TiExtensions
```

In the first line, `your_pd_servers` is the PD addresses separated by commas, each in the format of `$your_pd_address:$port`.

For example, `10.16.20.1:2379,10.16.20.2:2379,10.16.20.3:2379`, which means that you have multiple PD servers on `10.16.20.1,10.16.20.2,10.16.20.3` with the port `2379`.

#### Hybrid deployment of TiSpark and TiKV cluster

For the hybrid deployment of TiSpark and TiKV, add the resources required by TiSpark to the resources reserved in TiKV, and allocate 25% of the memory for the system.

## Deploy TiSpark

Download the TiSpark's jar package from [here](https://github.com/pingcap/tispark/releases).

Download your desired version of jar package and copy the content to the appropriate folder.

### Deploy TiSpark on existing Spark cluster

Do not reboot the existing Spark cluster for TiSpark to run on it. Instead, use Spark's `--jars` parameter to introduce TiSpark as a dependency:

```
spark-shell --jars $your_path_to/tispark-${name_with_version}.jar
```

To deploy TiSpark as a default component, place the TiSpark jar package into each node's jar path on the Spark cluster and restart the Spark cluster:

```
cp $your_path_to/tispark-${name_with_version}.jar $SPARK_HOME/jars
```

In this way, you can use either `Spark-Submit` or `Spark-Shell` to use TiSpark directly.

### Deploy TiSpark without Spark cluster

To deploy TiSpark without a Spark cluster, it is recommended that you use the Spark `standalone` mode by placing a compiled version of Spark on each node on the cluster. For any problem, refer to the [official Spark website](https://spark.apache.org/docs/latest/spark-standalone.html). You are also welcome to [file an issue](https://github.com/pingcap/tispark/issues/new) on GitHub.

1. Download and install [Apache Spark](https://spark.apache.org/downloads.html).

    + For the `standalone` mode without Hadoop support, use Spark **2.3.x/2.4.x** and any version of pre-build with Apache Hadoop 2.x with Hadoop dependencies.

    + If you need to use the Hadoop cluster, choose the corresponding Hadoop version. You can also build Spark from the [Spark 2.3 source code](https://spark.apache.org/docs/2.3.4/building-spark.html) or [Spark 2.4 source code](https://spark.apache.org/docs/2.4.4/building-spark.html) to match the previous version of the official Hadoop 2.6.

    > **Note:**
    >
    > Check the Spark version that your TiSpark version supports.

    Suppose you already have a Spark binary, and the current PATH is `SPARKPATH`, copy the TiSpark jar package to the `$SPARKPATH/jars` directory.

2. Start a Master node.

    Execute the following command on the selected Spark-Master node:

    ```
    cd $SPARKPATH

    ./sbin/start-master.sh
    ```

    After the command is executed, a log file is printed on the screen. Check the log file to confirm whether the Spark-Master is started successfully.

    Open the [http://spark-master-hostname:8080](http://spark-master-hostname:8080) to view the cluster information (if you do not change the default port number of Spark-Master).

    When you start Spark-Slave, you can also use this panel to confirm whether the Slave is joined to the cluster.

3. Start a Slave node.

    Similarly, start a Spark-Slave node by executing the following command:

    ```
    ./sbin/start-slave.sh spark://spark-master-hostname:7077
    ```

    After the command returns, also check whether the Slave node is joined to the Spark cluster correctly from the panel.

    Repeat the above command on all Slave nodes. After all the Slaves are connected to the Master, you have a Standalone mode Spark cluster.

4. Spark SQL shell and JDBC Server.

    Use Spark's ThriftServer and SparkSQL directly because TiSpark now supports Spark 2.3/2.4.

## Demonstration

This section briefly introduces how to use Spark SQL for OLAP analysis (assuming that you have successfully started the TiSpark cluster as described above).

The following example uses a table named `lineitem` in the `tpch` database.

1. Add the entry below in your `./conf/spark-defaults.conf`, assuming that your PD node is located at `192.168.1.100`, port `2379`.

    ```
    spark.tispark.pd.addresses 192.168.1.100:2379
    spark.sql.extensions org.apache.spark.sql.TiExtensions
    ```

2. In the Spark-Shell, enter the following command:

    ```
    spark.sql("use tpch")
    ```

3. Call Spark SQL directly:

    ```
    spark.sql("select count (*) from lineitem").show
    ```

    The result:

    ```
    +-------------+
    | Count (1) |
    +-------------+
    | 600000000 |
    +-------------+
    ```

TiSpark's SQL Interactive shell is almost the same as spark-sql shell.

```
spark-sql> use tpch;
Time taken: 0.015 seconds

spark-sql> select count(*) from lineitem;
2000
Time taken: 0.673 seconds, Fetched 1 row(s)
```

For the JDBC connection with Thrift Server, try various JDBC-supported tools including SQuirreL SQL and hive-beeline.

For example, to use it with beeline:

```
./beeline
Beeline version 1.2.2 by Apache Hive
beeline> !connect jdbc:hive2://localhost:10000

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

## TiSparkR

TiSparkR is a thin layer built for supporting R language with TiSpark. Refer to [this document](https://github.com/pingcap/tispark/blob/master/R/README.md) for TiSparkR guide.

## TiSpark on PySpark

TiSpark on PySpark is a Python package build to support Python language with TiSpark. Refer to [this document](https://github.com/pingcap/tispark/blob/master/python/README.md) for TiSpark on PySpark guide .

## Use TiSpark with Hive

To use TiSpark with Hive:

1. Set the environment variable `HADOOP_CONF_DIR` to your Hadoop's configuration folder.

2. Copy `hive-site.xml` to the `spark/conf` folder before you start Spark.

    ```
    val tisparkDF = spark.sql("select * from tispark_table").toDF
    tisparkDF.write.saveAsTable("hive_table") // save table to hive
    spark.sql("select * from hive_table a, tispark_table b where a.col1 = b.col1").show // join table across Hive and Tispark
    ```

## Load Spark DataFrame into TiDB using JDBC

While TiSpark provides a direct way to load data into your TiDB cluster, you can also do it by using JDBC.

For example:

```scala
import org.apache.spark.sql.execution.datasources.jdbc.JDBCOptions

val customer = spark.sql("select * from customer limit 100000")
// you might repartition source to make it balanced across nodes
// and increase concurrency
val df = customer.repartition(32)
df.write
.mode(saveMode = "append")
.format("jdbc")
.option("driver", "com.mysql.jdbc.Driver")
 // replace the host and port with yours and be sure to use rewrite batch
.option("url", "jdbc:mysql://127.0.0.1:4000/test?rewriteBatchedStatements=true")
.option("useSSL", "false")
// as tested, setting to `150` is a good practice
.option(JDBCOptions.JDBC_BATCH_INSERT_SIZE, 150)
.option("dbtable", s"cust_test_select") // database name and table name here
.option("isolationLevel", "NONE") // recommended to set isolationLevel to NONE if you have a large DF to load.
.option("user", "root") // TiDB user here
.save()
```

It is recommended that you set `isolationLevel` to `NONE` to avoid large single transactions which might lead to TiDB OOM.

## Statistics information

TiSpark uses the statistic information in TiDB for:

+ Determining which index to use in your query plan with the lowest estimated cost;
+ Small table broadcasting, which enables efficient broadcast join.

For TiSpark to use the statistic information in TiDB, first make sure that relevant tables have been analyzed.

See [here](/v2.1/reference/sql/statements/analyze-table.md) for more details on how to analyze tables.

Since TiSpark 2.0, statistics information is default to auto-load.

> **Note:**
>
> Table statistics is cached in your Spark driver node's memory, so you need to make sure that the memory is large enough for the statistics information.

Currently, you can adjust the following configuration in your `spark.conf` file.

| Property Name | Default | Description
| :--------   | :-----   | :---- |
| `spark.tispark.statistics.auto_load` | `true` | Decides whether to load the statistics information automatically during database mapping. |

## Read partition table from TiDB

TiSpark reads the range and hash partition table from TiDB. TiSpark decides whether to apply partition pruning according to the partition type and the partition expression associated with the table.

Currently, TiSpark partially apply partition pruning on range partition. The partition pruning is applied when the partition expression of the range partition is one of the following types:

+ column expression
+ `YEAR` (expression) where the expression is a column and its type is `DATETIME` or string literal
that can be parsed as `DATETIME`

If partition pruning is not applied, TiSpark's reading behavior is equivalent to scanning tables over all partitions.

## Common port numbers used by Spark cluster

|Port Name| Default Port Number   | Configuration Property   | Notes|
| :---------------| :------------- | :-----| :-----|
| Master web UI  | `8080`  | `spark.master.ui.port`  or `SPARK_MASTER_WEBUI_PORT` | The value set by `spark.master.ui.port` takes precedence.  |
| Worker web UI  |  `8081`  | `spark.worker.ui.port` or `SPARK_WORKER_WEBUI_PORT`  | The value set by `spark.worker.ui.port` takes precedence.|
|History server web UI   |  `18080`  | `spark.history.ui.port`  |An optional port; it is only applied if you use the history server.   |
|Master port   |  `7077`  |   `SPARK_MASTER_PORT`  |   |
|Master REST port   |  `6066`  | `spark.master.rest.port`  | Not needed if you disable the `REST` service.   |
|Worker port |  (random)   |  `SPARK_WORKER_PORT` |   |
|Block manager port  |(random)   | `spark.blockManager.port`  |   |
|Shuffle server  |  `7337`   | `spark.shuffle.service.port`  |  An optional port; it is only applied if you use the external shuffle service.  |
|  Application web UI  |  `4040`  |  `spark.ui.port` | If the `4040` port is occupied, `4041` is used instead. |
