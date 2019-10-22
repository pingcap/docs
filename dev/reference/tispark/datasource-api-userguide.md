---
title: TiDB Data Source API User Guide
summary: Learn how to use TiDB data source API.
category: reference
---

# TiDB Data Source API User Guide

<!-- markdownlint-disable MD029 -->

The interaction between TiDB and Spark is enabled by TiDB Connector for Spark, which allows you to use TiDB as the data source of Apache Spark. TiDB Connector supports bi-directional data movement between TiDB and Spark clusters. By using the Connector, you can populate a Spark DataFrame from a table in TiDB and write the contents of a Spark DataFrame to a table in TiDB.

This document introduce how to use TiDB Connector and the data source APIs.

> **Note:**
>
> TiDB Connector supports Spark 2.3.0+ and Spark 2.4.0+.

## `Transaction` support for data write

TiDB is a database that supports `transaction`. TiDB Connector for Spark also supports `transaction`, which means that:

1. if no conflicts exist, all data in DataFrame is written to TiDB successfully;
2. if any conflict exists, no data in DataFrame is written to TiDB;
3. no partial changes are visible to other sessions until the transaction is committed.

## Writing behavior of TiSpark

TiSpark only supports the `Append` SaveMode. This behavior is controlled by the `REPLACE` option. The default value of this option is `false`.

If `REPLACE` is true, data to be inserted is duplicated before the insertion. In this case:

- if the primary key or unique index exists in the database, data is updated.
- if no same primary key or unique index exists, data is inserted.

If `REPLACE` is `false`:

- if the primary key or unique index exists in the database, data with conflicts expects an exception.
- if no same primary key or unique index exists, data is inserted.

## Use Spark connector with extensions enabled

The Spark connector adheres to the standard Spark API with the addition of TiDB-specific options.

Fow how to use it with extensions enabled, refer to [code examples with extensions](https://github.com/pingcap/tispark-test/blob/master/tispark-examples/src/main/scala/com/pingcap/tispark/examples/TiDataSourceExampleWithExtensions.scala).

+ Start `SparkConf`:

    ```scala
    val sparkConf = new SparkConf().
      setIfMissing("spark.master", "local[*]").
      setIfMissing("spark.app.name", getClass.getName).
      setIfMissing("spark.sql.extensions", "org.apache.spark.sql.TiExtensions").
      setIfMissing("spark.tispark.pd.addresses", "pd0:2379").
      setIfMissing("spark.tispark.tidb.addr", "tidb").
      setIfMissing("spark.tispark.tidb.port", "4000")
      // if tidb <= 3.x, set the spark.tispark.write.without_lock_table=true
      // .setIfMissing("spark.tispark.write.without_lock_table", "true")

    val spark = SparkSession.builder.config(sparkConf).getOrCreate()
    ```

+ Read data using scala:

    ```scala
    val sqlContext = spark.sqlContext

    // use TiDB config in the spark config if no data source config is provided.
    val tidbOptions: Map[String, String] = Map(
      "tidb.user" -> "root",
      "tidb.password" -> ""
    )

    val df = sqlContext.read.
      format("tidb").
      options(tidbOptions).
      option("database", "tpch_test").
      option("table", "CUSTOMER").
      load().
      filter("C_CUSTKEY = 1").
      select("C_NAME")
    df.show()
    ```

+ Write data using scala:

    ```scala
    /* create table before running the code
    CREATE TABLE tpch_test.target_table_orders (
      `O_ORDERKEY` int(11) NOT NULL,
      `O_CUSTKEY` int(11) NOT NULL,
      `O_ORDERSTATUS` char(1) NOT NULL,
      `O_TOTALPRICE` decimal(15,2) NOT NULL,
      `O_ORDERDATE` date NOT NULL,
      `O_ORDERPRIORITY` char(15) NOT NULL,
      `O_CLERK` char(15) NOT NULL,
      `O_SHIPPRIORITY` int(11) NOT NULL,
      `O_COMMENT` varchar(79) NOT NULL
    )
    */

    // use TiDB config in the spark config if no data source config is provided
    val tidbOptions: Map[String, String] = Map(
      "tidb.user" -> "root",
      "tidb.password" -> ""
    )

    // data to write
    val df = sqlContext.read.
      format("tidb").
      options(tidbOptions).
      option("database", "tpch_test").
      option("table", "ORDERS").
      load()

    // append
    df.write.
      format("tidb").
      options(tidbOptions).
      option("database", "tpch_test").
      option("table", "target_table_orders").
      mode("append").
      save()
    ```

+ Use another TiDB server:

   TiDB configuration can be overwritten in data source options, so you can connect to a different TiDB server.

    ```scala
    // TiDB config priority: data source config > spark config
    val tidbOptions: Map[String, String] = Map(
      "tidb.addr" -> "anotherTidbIP",
      "tidb.password" -> "",
      "tidb.port" -> "4000",
      "tidb.user" -> "root",
      "spark.tispark.pd.addresses" -> "pd0:2379"
    )

    val df = sqlContext.read.
      format("tidb").
      options(tidbOptions).
      option("database", "tpch_test").
      option("table", "CUSTOMER").
      load().
      filter("C_CUSTKEY = 1").
      select("C_NAME").
    df.show()
    ```

## Use Spark connector with extensions disabled

For how to use the connector with extensions disabled,
refer to [code examples without extensions](https://github.com/pingcap/tispark-test/blob/master/tispark-examples/src/main/scala/com/pingcap/tispark/examples/TiDataSourceExampleWithoutExtensions.scala).

+ Start `SparkConf`:

    ```scala
    import org.apache.spark.SparkConf
    import org.apache.spark.sql.{DataFrame, SQLContext, SparkSession}

    val sparkConf = new SparkConf()
      .setIfMissing("spark.master", "local[*]")
      .setIfMissing("spark.app.name", getClass.getName)

    val spark = SparkSession.builder.config(sparkConf).getOrCreate()
    val sqlContext = spark.sqlContext
    ```

    If TiDB version is 3.x or earlier, set `spark.tispark.write.without_lock_table=true.setIfMissing("spark.tispark.write.without_lock_table", "true")`.

+ Read data using scala:

    ```scala
    val sqlContext = spark.sqlContext

    // TiSpark's common options can also be passed in,
    // for example, spark.tispark.plan.allow_agg_pushdown`, spark.tispark.plan.allow_index_read, etc.
    // spark.tispark.plan.allow_index_read is optional.
    val tidbOptions: Map[String, String] = Map(
      "tidb.addr" -> "tidb",
      "tidb.password" -> "",
      "tidb.port" -> "4000",
      "tidb.user" -> "root",
      "spark.tispark.pd.addresses" -> "pd0:2379"
    )

    val df = sqlContext.read.
      format("tidb").
      options(tidbOptions).
      option("database", "tpch_test").
      option("table", "CUSTOMER").
      load().
      filter("C_CUSTKEY = 1").
      select("C_NAME").
    df.show()
    ```

+ Write data using scala:

    ```scala
    /* create table before running the code
    CREATE TABLE tpch_test.target_table_customer (
      `C_CUSTKEY` int(11) NOT NULL,
      `C_NAME` varchar(25) NOT NULL,
      `C_ADDRESS` varchar(40) NOT NULL,
      `C_NATIONKEY` int(11) NOT NULL,
      `C_PHONE` char(15) NOT NULL,
      `C_ACCTBAL` decimal(15,2) NOT NULL,
      `C_MKTSEGMENT` char(10) NOT NULL,
      `C_COMMENT` varchar(117) NOT NULL
    )
    */

    // Common options can also be passed in,
    // for example, spark.tispark.plan.allow_agg_pushdown, spark.tispark.plan.allow_index_read, etc.
    // spark.tispark.plan.allow_index_read is optional.
    val tidbOptions: Map[String, String] = Map(
      "tidb.addr" -> "127.0.0.1",
      "tidb.password" -> "",
      "tidb.port" -> "4000",
      "tidb.user" -> "root",
      "spark.tispark.pd.addresses" -> "127.0.0.1:2379"
    )

    val df = readUsingScala(sqlContext)

    df.write.
      format("tidb").
      options(tidbOptions).
      option("database", "tpch_test").
      option("table", "target_table_customer").
      mode("append").
      save()
    ```

## Use data source API in SparkSQL

Follow these steps to use data source API in SparkSQL:

1. Configure TiDB or PD addresses and enable write through SparkSQL in `conf/spark-defaults.conf` as the following commands shows:

    ```
    spark.tispark.pd.addresses 127.0.0.1:2379
    spark.tispark.tidb.addr 127.0.0.1
    spark.tispark.tidb.port 4000
    spark.tispark.write.allow_spark_sql true
    ```

    If the TiDB version is 3.x or earlier, set `spark.tispark.write.without_lock_table=true spark.tispark.write.without_lock_table true`.

2. Create a new table using mysql-client:

    ```sql
    CREATE TABLE tpch_test.TARGET_TABLE_CUSTOMER (
      `C_CUSTKEY` int(11) NOT NULL,
      `C_NAME` varchar(25) NOT NULL,
      `C_ADDRESS` varchar(40) NOT NULL,
      `C_NATIONKEY` int(11) NOT NULL,
      `C_PHONE` char(15) NOT NULL,
      `C_ACCTBAL` decimal(15,2) NOT NULL,
      `C_MKTSEGMENT` char(10) NOT NULL,
      `C_COMMENT` varchar(117) NOT NULL
    )
    ```

3. Register a TiDB table `tpch_test.CUSTOMER` to the Spark catalog:

    ```sql
    CREATE TABLE CUSTOMER_SRC USING tidb OPTIONS (
      tidb.user 'root',
      tidb.password '',
      database 'tpch_test',
      table 'CUSTOMER'
    )
    ```

4. Select data from `tpch_test.CUSTOMER`:

    ```sql
    SELECT * FROM CUSTOMER_SRC limit 10
    ```

5. Register another TiDB table `tpch_test.TARGET_TABLE_CUSTOMER` to the Spark catalog:

    ```sql
    CREATE TABLE CUSTOMER_DST USING tidb OPTIONS (database 'tpch_test', table 'TARGET_TABLE_CUSTOMER')
    ```

6. Write data to `tpch_test.TARGET_TABLE_CUSTOMER`:

    ```sql
    INSERT INTO CUSTOMER_DST VALUES(1000, 'Customer#000001000', 'AnJ5lxtLjioClr2khl9pb8NLxG2', 9, '19-407-425-2584', 2209.81, 'AUTOMOBILE', '. even, express theodolites upo')

    INSERT INTO CUSTOMER_DST SELECT * FROM CUSTOMER_SRC
    ```

## TiDB options

The following table shows the TiDB-specific options, which can be passed in through `TiDBOptions` or `SparkConf`.

| Key                        | Short Name    | Required value | Description                                                                                                                                                 | Default |
| :-------------------------- | :------------- | :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- |
| spark.tispark.pd.addresses | -             | true           | The addresses of PD clusters, split by comma                                                                                                                | -       |
| spark.tispark.tidb.addr    | tidb.addr     | true           | TiDB address, which currently only supports one instance                                                                                                    | -       |
| spark.tispark.tidb.port    | tidb.port     | true           | TiDB Port                                                                                                                                                   | -       |
| spark.tispark.tidb.user    | tidb.user     | true           | TiDB User                                                                                                                                                   | -       |
| tidb.password              | tidb.password | true           | TiDB Password                                                                                                                                               | -       |
| database                   | -             | true           | TiDB Database                                                                                                                                               | -       |
| table                      | -             | true           | TiDB Table                                                                                                                                                  | -       |
| skipCommitSecondaryKey     | -             | false          | Whether to skip the commit phase of secondary keys                                                                                                          | false   |
| enableRegionSplit          | -             | false          | Splits the Region to avoid hot Region during insertion                                                                                                        | true    |
| regionSplitNum             | -             | false          | The Region split number defined by user during insertion                                                                                                    | 0       |
| replace                    | -             | false          | Defines the behavior of append                                                                                                                            | false   |
| lockTTLSeconds             | -             | false          | TiKV's lock TTL. The write duration must be no longer than `lockTTLSeconds`, otherwise the write might fail because of the Garbage Collection (GC).             | 3600    |
| writeConcurrency           | -             | false          | The maximum number of threads for writing data to TiKV. It is recommended that `writeConcurrency` is smaller than or equal to 8 * `number of TiKV instance`. | 0       |

## TiDB version and configuration for data write

TiDB's version must be 4.0 or later.

> **Note:**
>
> Currently, TiDB 4.0 is not released yet, but you can use code from [TiDB master branch](https://github.com/pingcap/tidb/tree/master).

Make sure that the following TiDB configuration items are correctly set.

```
# enable-table-lock is used to control the table lock feature.
# The default value is false, indicating that the table lock feature is disabled.
enable-table-lock: true

# delay-clean-table-lock is used to control the time (milliseconds) of delay
# before unlocking the table in abnormal situations.
delay-clean-table-lock: 60000

# When creating table, split a separated Region for it.
# It is recommended to disable this option if there is a large number of tables created.
split-table: true
```

If your TiDB version is earlier than 4.0, set `spark.tispark.write.without_lock_table` to `true` to enable write, but ACID is **not** guaranteed.

## Type conversion for data write

The following types of SparkSQL data currently cannot be written into TiDB:

- BinaryType
- ArrayType
- MapType
- StructType

The complete conversion metrics are as follows.

| Write      | Boolean            | Byte               | Short              | Integer            | Long               | Float              | Double             | String             | Decimal            | Date               | Timestamp          |
| :---------- | :------------------ | :------------------ | :------------------ | :------------------ | :------------------ | :------------------ | :------------------ | :------------------ | :------------------ | :------------------ | :------------------ |
| BIT        | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                | :x:                |
| BOOLEAN    | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                |
| TINYINT    | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                |
| SMALLINT   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                |
| MEDIUMINT  | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                |
| INTEGER    | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                |
| BIGINT     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                |
| FLOAT      | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :x:                |
| DOUBLE     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :white_check_mark: | :x:                |
| DECIMAL    | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                |
| DATE       | :x:                | :x:                | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                | :white_check_mark: | :white_check_mark: |
| DATETIME   | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: |
| TIMESTAMP  | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :white_check_mark: | :x:                | :white_check_mark: | :white_check_mark: |
| TIME       | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                |
| YEAR       | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                |
| CHAR       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| VARCHAR    | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| TINYTEXT   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| TEXT       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| MEDIUMTEXT | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| LONGTEXT   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| BINARY     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :x:                | :x:                | :x:                |
| VARBINARY  | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :x:                | :x:                | :x:                |
| TINYBLOB   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :x:                | :x:                | :x:                |
| BLOB       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :x:                | :x:                | :x:                |
| MEDIUMBLOB | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :x:                | :x:                | :x:                |
| LONGBLOB   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :white_check_mark: | :x:                | :x:                | :x:                |
| ENUM       | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                | :x:                | :x:                |
| SET        | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                |

For the benchmark test results of TiSpark operations with TiDB, refer to [TiSpark Benchmark Results](/dev/benchmark/tispark.md).
