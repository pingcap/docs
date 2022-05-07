---
title: Use TiFlash
aliases: ['/docs/dev/tiflash/use-tiflash/','/docs/dev/reference/tiflash/use-tiflash/']
---

To experience the whole process from importing data to querying in a TPC-H dataset, refer to [Quick Start Guide for TiDB HTAP](/quick-start-with-htap.md).

# Use TiFlash

After TiFlash is deployed, data replication does not automatically begin. You need to manually specify the tables to be replicated.

You can either use TiDB to read TiFlash replicas for medium-scale analytical processing, or use TiSpark to read TiFlash replicas for large-scale analytical processing, which is based on your own needs. See the following sections for details:

- [Use TiDB to read TiFlash replicas](#use-tidb-to-read-tiflash-replicas)
- [Use TiSpark to read TiFlash replicas](#use-tispark-to-read-tiflash-replicas)

## Create TiFlash replicas

This section describes how to create TiFlash replicas for tables and for databases, and set available zones for replica scheduling.

### Create TiFlash replicas for tables

After TiFlash is connected to the TiKV cluster, data replication by default does not begin. You can send a DDL statement to TiDB through a MySQL client to create a TiFlash replica for a specific table:

{{< copyable "sql" >}}

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

The parameter of the above command is described as follows:

- `count` indicates the number of replicas. When the value is `0`, the replica is deleted.

If you execute multiple DDL statements on the same table, only the last statement is ensured to take effect. In the following example, two DDL statements are executed on the table `tpch50`, but only the second statement (to delete the replica) takes effect.

Create two replicas for the table:

{{< copyable "sql" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2;
```

Delete the replica:

{{< copyable "sql" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0;
```

**Notes:**

* If the table `t` is replicated to TiFlash through the above DDL statements, the table created using the following statement will also be automatically replicated to TiFlash:

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE table_name like t;
    ```

* For versions earlier than v4.0.6, if you create the TiFlash replica before using TiDB Lightning to import the data, the data import will fail. You must import data to the table before creating the TiFlash replica for the table.

* If TiDB and TiDB Lightning are both v4.0.6 or later, no matter a table has TiFlash replica(s) or not, you can import data to that table using TiDB Lightning. Note that this might slow the TiDB Lightning procedure, which depends on the NIC bandwidth on the lightning host, the CPU and disk load of the TiFlash node, and the number of TiFlash replicas.

* It is recommended that you do not replicate more than 1,000 tables because this lowers the PD scheduling performance. This limit will be removed in later versions.

* In v5.1 and later versions, setting the replicas for the system tables is no longer supported. Before upgrading the cluster, you need to clear the replicas of the relevant system tables. Otherwise, you cannot modify the replica settings of the system tables after you upgrade the cluster to a later version.

#### Check replication progress

You can check the status of the TiFlash replicas of a specific table using the following statement. The table is specified using the `WHERE` clause. If you remove the `WHERE` clause, you will check the replica status of all tables.

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

In the result of above statement:

* `AVAILABLE` indicates whether the TiFlash replicas of this table are available or not. `1` means available and `0` means unavailable. Once the replicas become available, this status does not change. If you use DDL statements to modify the number of replicas, the replication status will be recalculated.
* `PROGRESS` means the progress of the replication. The value is between `0.0` and `1.0`. `1` means at least one replica is replicated.

### Create TiFlash replicas for databases

Similar to creating TiFlash replicas for tables, you can send a DDL statement to TiDB through a MySQL client to create a TiFlash replica for all tables in a specific database:

{{< copyable "sql" >}}

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

In this statement, `count` indicates the number of replicas. When you set it to `0`, replicas are deleted.

Examples:

- Create two replicas for all tables in the database `tpch50`:

    {{< copyable "sql" >}}

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 2;
    ```

- Delete TiFlash replicas created for the database `tpch50`:

    {{< copyable "sql" >}}

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 0;
    ```

> **Note:**
>
> - This statement actually performs a series of DDL operations, which are resource-intensive. If the statement is interrupted during the execution, executed operations are not rolled back and unexecuted operations do not continue.
>
> - After executing the statement, do not set the number of TiFlash replicas or perform DDL operations on this database until **all tables in this database are replicated**. Otherwise, unexpected results might occur, which include:
>     - If you set the number of TiFlash replicas to 2 and then change the number to 1 before all tables in the database are replicated, the final number of TiFlash replicas of all the tables is not necessarily 1 or 2.
>     - After executing the statement, if you create tables in this database before the completion of the statement execution, TiFlash replicas **may or may not** be created for these new tables.
>     - After executing the statement, if you add indexes for tables in the database before the completion of the statement execution, the statement might hang and resume only after the indexes are added.
>
> - This statement skips system tables, views, temporary tables, and tables with character sets not supported by TiFlash.

#### Check replication progress

Similar to creating TiFlash replicas for tables, successful execution of the DDL statement does not mean the completion of replication. You can execute the following SQL statement to check the progress of replication on target tables:

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>';
```

To check tables without TiFlash replicas in the database, you can execute the following SQL statement:

{{< copyable "sql" >}}

```sql
SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = "<db_name>" and TABLE_NAME not in (SELECT TABLE_NAME FROM information_schema.tiflash_replica where TABLE_SCHEMA = "<db_name>");
```

### Set available zones

When configuring replicas, if you need to distribute TiFlash replicas to multiple data centers for disaster recovery, you can configure available zones by following the steps below:

1. Specify labels for TiFlash nodes in the cluster configuration file.

    ```
    tiflash_servers:
      - host: 172.16.5.81
        config:
          flash.proxy.labels: zone=z1
      - host: 172.16.5.82
        config:
          flash.proxy.labels: zone=z1
      - host: 172.16.5.85
        config:
          flash.proxy.labels: zone=z2
    ```

2. After starting a cluster, specify the labels when creating replicas.

    {{< copyable "sql" >}}

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;
    ```

    For example:

    {{< copyable "sql" >}}

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2 LOCATION LABELS "zone";
    ```

3. PD schedules the replicas based on the labels. In this example, PD respectively schedules two replicas of the table `t` to two available zones. You can use pd-ctl to view the scheduling.

    ```shell
    > tiup ctl:<version> pd -u<pd-host>:<pd-port> store

        ...
        "address": "172.16.5.82:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z1" }
        ],
        "region_count": 4,

        ...
        "address": "172.16.5.81:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z1" }
        ],
        "region_count": 5,
        ...

        "address": "172.16.5.85:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z2" }
        ],
        "region_count": 9,
        ...
    ```

For more information about scheduling replicas by using labels, see [Schedule Replicas by Topology Labels](/schedule-replicas-by-topology-labels.md), [Multiple Data Centers in One City Deployment](/multi-data-centers-in-one-city-deployment.md), and [Three Data Centers in Two Cities Deployment](/three-data-centers-in-two-cities-deployment.md).

## Use TiDB to read TiFlash replicas

TiDB provides three ways to read TiFlash replicas. If you have added a TiFlash replica without any engine configuration, the CBO (cost-based optimization) mode is used by default.

### Smart selection

For tables with TiFlash replicas, the TiDB optimizer automatically determines whether to use TiFlash replicas based on the cost estimation. You can use the `desc` or `explain analyze` statement to check whether or not a TiFlash replica is selected. For example:

{{< copyable "sql" >}}

```sql
desc select count(*) from test.t;
```

```
+--------------------------+---------+--------------+---------------+--------------------------------+
| id                       | estRows | task         | access object | operator info                  |
+--------------------------+---------+--------------+---------------+--------------------------------+
| StreamAgg_9              | 1.00    | root         |               | funcs:count(1)->Column#4       |
| └─TableReader_17         | 1.00    | root         |               | data:TableFullScan_16          |
|   └─TableFullScan_16     | 1.00    | cop[tiflash] | table:t       | keep order:false, stats:pseudo |
+--------------------------+---------+--------------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
explain analyze select count(*) from test.t;
```

```
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| id                       | estRows | actRows | task         | access object | execution info                                                       | operator info                  | memory    | disk |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| StreamAgg_9              | 1.00    | 1       | root         |               | time:83.8372ms, loops:2                                              | funcs:count(1)->Column#4       | 372 Bytes | N/A  |
| └─TableReader_17         | 1.00    | 1       | root         |               | time:83.7776ms, loops:2, rpc num: 1, rpc time:83.5701ms, proc keys:0 | data:TableFullScan_16          | 152 Bytes | N/A  |
|   └─TableFullScan_16     | 1.00    | 1       | cop[tiflash] | table:t       | time:43ms, loops:1                                                   | keep order:false, stats:pseudo | N/A       | N/A  |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
```

`cop[tiflash]` means that the task will be sent to TiFlash for processing. If you have not selected a TiFlash replica, you can try to update the statistics using the `analyze table` statement, and then check the result using the `explain analyze` statement.

Note that if a table has only a single TiFlash replica and the related node cannot provide service, queries in the CBO mode will repeatedly retry. In this situation, you need to specify the engine or use the manual hint to read data from the TiKV replica.

### Engine isolation

Engine isolation is to specify that all queries use a replica of the specified engine by configuring the corresponding variable. The optional engines are "tikv", "tidb" (indicates the internal memory table area of TiDB, which stores some TiDB system tables and cannot be actively used by users), and "tiflash", with the following two configuration levels:

* TiDB instance-level, namely, INSTANCE level. Add the following configuration item in the TiDB configuration file:

    ```
    [isolation-read]
    engines = ["tikv", "tidb", "tiflash"]
    ```

    **The INSTANCE-level default configuration is `["tikv", "tidb", "tiflash"]`.**

* SESSION level. Use the following statement to configure:

    {{< copyable "sql" >}}

    ```sql
    set @@session.tidb_isolation_read_engines = "engine list separated by commas";
    ```

    or

    {{< copyable "sql" >}}

    ```sql
    set SESSION tidb_isolation_read_engines = "engine list separated by commas";
    ```

    The default configuration of the SESSION level inherits from the configuration of the TiDB INSTANCE level.

The final engine configuration is the session-level configuration, that is, the session-level configuration overrides the instance-level configuration. For example, if you have configured "tikv" in the INSTANCE level and "tiflash" in the SESSION level, then the TiFlash replicas are read. If the final engine configuration is "tikv" and "tiflash", then the TiKV and TiFlash replicas are both read, and the optimizer automatically selects a better engine to execute.

> **Note:**
>
> Because [TiDB Dashboard](/dashboard/dashboard-intro.md) and other components need to read some system tables stored in the TiDB memory table area, it is recommended to always add the "tidb" engine to the instance-level engine configuration.

If the queried table does not have a replica of the specified engine (for example, the engine is configured as "tiflash" but the table does not have a TiFlash replica), the query returns an error.

### Manual hint

Manual hint can force TiDB to use specified replicas for specific table(s) on the premise of satisfying engine isolation. Here is an example of using the manual hint:

{{< copyable "sql" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

If you set an alias to a table in a query statement, you must use the alias in the statement that includes a hint for the hint to take effect. For example:

{{< copyable "sql" >}}

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

In the above statements, `tiflash[]` prompts the optimizer to read the TiFlash replicas. You can also use `tikv[]` to prompt the optimizer to read the TiKV replicas as needed. For hint syntax details, refer to [READ_FROM_STORAGE](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-).

If the table specified by a hint does not have a replica of the specified engine, the hint is ignored and a warning is reported. In addition, a hint only takes effect on the premise of engine isolation. If the engine specified in a hint is not in the engine isolation list, the hint is also ignored and a warning is reported.

> **Note:**
>
> The MySQL client of 5.7.7 or earlier versions clears optimizer hints by default. To use the hint syntax in these early versions, start the client with the `--comments` option, for example, `mysql -h 127.0.0.1 -P 4000 -uroot --comments`.

### The relationship of smart selection, engine isolation, and manual hint

In the above three ways of reading TiFlash replicas, engine isolation specifies the overall range of available replicas of engines; within this range, manual hint provides statement-level and table-level engine selection that is more fine-grained; finally, CBO makes the decision and selects a replica of an engine based on cost estimation within the specified engine list.

> **Note:**
>
> Before v4.0.3, the behavior of reading from TiFlash replica in a non-read-only SQL statement (for example, `INSERT INTO ... SELECT`, `SELECT ... FOR UPDATE`, `UPDATE ...`, `DELETE ...`) is undefined. In v4.0.3 and later versions, internally TiDB ignores the TiFlash replica for a non-read-only SQL statement to guarantee the data correctness. That is, for [smart selection](#smart-selection), TiDB automatically selects the non-TiFlash replica; for [engine isolation](#engine-isolation) that specifies TiFlash replica **only**, TiDB reports an error; and for [manual hint](#manual-hint), TiDB ignores the hint.

## Use TiSpark to read TiFlash replicas

Currently, you can use TiSpark to read TiFlash replicas in a method similar to the engine isolation in TiDB. This method is to configure the `spark.tispark.isolation_read_engines` parameter. The parameter value defaults to `tikv,tiflash`, which means that TiDB reads data from TiFlash or from TiKV according to CBO's selection. If you set the parameter value to `tiflash`, it means that TiDB forcibly reads data from TiFlash.

> **Notes**
>
> When this parameter is set to `true`, only the TiFlash replicas of all tables involved in the query are read and these tables must have TiFlash replicas; for tables that do not have TiFlash replicas, an error is reported. When this parameter is set to `false`, only the TiKV replica is read.

You can configure this parameter in one of the following ways:

* Add the following item in the `spark-defaults.conf` file:

    ```
    spark.tispark.isolation_read_engines tiflash
    ```

* Add `--conf spark.tispark.isolation_read_engines=tiflash` in the initialization command when initializing Spark shell or Thrift server.

* Set `spark.conf.set("spark.tispark.isolation_read_engines", "tiflash")` in Spark shell in a real-time manner.

* Set `set spark.tispark.isolation_read_engines=tiflash` in Thrift server after the server is connected via beeline.

## Supported push-down calculations

TiFlash supports the push-down of the following operators:

* TableScan: Reads data from tables.
* Selection: Filters data.
* HashAgg: Performs data aggregation based on the [Hash Aggregation](/explain-aggregation.md#hash-aggregation) algorithm.
* StreamAgg: Performs data aggregation based on the [Stream Aggregation](/explain-aggregation.md#stream-aggregation) algorithm. SteamAgg only supports the aggregation without the `GROUP BY` condition.
* TopN: Performs the TopN calculation.
* Limit: Performs the limit calculation.
* Project: Performs the projection calculation.
* HashJoin: Performs the join calculation using the [Hash Join](/explain-joins.md#hash-join) algorithm, but with the following conditions:
    * The operator can be pushed down only in the [MPP mode](#use-the-mpp-mode).
    * Supported joins are Inner Join, Left Join, Semi Join, Anti Semi Join, Left Semi Join, and Anti Left Semi Join.
    * The preceding joins support both Equi Join and Non-Equi Join (Cartesian Join). When calculating Cartesian Join, the Broadcast algorithm, instead of the Shuffle Hash Join algorithm, is used.

In TiDB, operators are organized in a tree structure. For an operator to be pushed down to TiFlash, all of the following prerequisites must be met:

+ All of its child operators can be pushed down to TiFlash.
+ If an operator contains expressions (most of the operators contain expressions), all expressions of the operator can be pushed down to TiFlash.

Currently, TiFlash supports the following push-down expressions:

* Mathematical functions: `+, -, /, *, %, >=, <=, =, !=, <, >, round, abs, floor(int), ceil(int), ceiling(int), sqrt, log, log2, log10, ln, exp, pow, sign, radians, degrees, conv, crc32, greatest(int/real), least(int/real)`
* Logical functions: `and, or, not, case when, if, ifnull, isnull, in, like, coalesce, is`
* Bitwise operations: `bitand, bitor, bigneg, bitxor`
* String functions: `substr, char_length, replace, concat, concat_ws, left, right, ascii, length, trim, ltrim, rtrim, position, format, lower, ucase, upper, substring_index, lpad, rpad, strcmp, regexp`
* Date functions: `date_format, timestampdiff, from_unixtime, unix_timestamp(int), unix_timestamp(decimal), str_to_date(date), str_to_date(datetime), datediff, year, month, day, extract(datetime), date, hour, microsecond, minute, second, sysdate, date_add, date_sub, adddate, subdate, quarter, dayname, dayofmonth, dayofweek, dayofyear, last_day, monthname`
* JSON function: `json_length`
* Conversion functions: `cast(int as double), cast(int as decimal), cast(int as string), cast(int as time), cast(double as int), cast(double as decimal), cast(double as string), cast(double as time), cast(string as int), cast(string as double), cast(string as decimal), cast(string as time), cast(decimal as int), cast(decimal as string), cast(decimal as time), cast(time as int), cast(time as decimal), cast(time as string), cast(time as real)`
* Aggregate functions: `min, max, sum, count, avg, approx_count_distinct, group_concat`
* Miscellaneous functions: `inetntoa, inetaton, inet6ntoa, inet6aton`

### Other restrictions

* Expressions that contain the Bit, Set, and Geometry types cannot be pushed down to TiFlash.

* The `date_add`, `date_sub`, `adddate`, and `subdate` functions support the following interval types only. If other interval types are used, TiFlash reports errors.

    * DAY
    * WEEK
    * MONTH
    * YEAR
    * HOUR
    * MINUTE
    * SECOND

If a query encounters unsupported push-down calculations, TiDB needs to complete the remaining calculations, which might greatly affect the TiFlash acceleration effect. The currently unsupported operators and expressions might be supported in future versions.

## Use the MPP mode

TiFlash supports using the MPP mode to execute queries, which introduces cross-node data exchange (data shuffle process) into the computation. TiDB automatically determines whether to select the MPP mode using the optimizer's cost estimation. You can change the selection strategy by modifying the values of [`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-new-in-v50) and [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51).

### Control whether to select the MPP mode

The `tidb_allow_mpp` variable controls whether TiDB can select the MPP mode to execute queries. The `tidb_enforce_mpp` variable controls whether the optimizer's cost estimation is ignored and the MPP mode of TiFlash is forcibly used to execute queries.

The results corresponding to all values of these two variables are as follows:

|                        | tidb_allow_mpp=off | tidb_allow_mpp=on (by default)              |
| ---------------------- | -------------------- | -------------------------------- |
| tidb_enforce_mpp=off (by default) | The MPP mode is not used. | The optimizer selects the MPP mode based on cost estimation. (by default)|
| tidb_enforce_mpp=on  | The MPP mode is not used.   | TiDB ignores the cost estimation and selects the MPP mode.      |

For example, if you do not want to use the MPP mode, you can execute the following statements:

{{< copyable "sql" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

If you want TiDB's cost-based optimizer to automatically decide whether to use the MPP mode (by default), you can execute the following statements:

{{< copyable "sql" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

If you want TiDB to ignore the optimizer's cost estimation and to forcibly select the MPP mode, you can execute the following statements:

{{< copyable "sql" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=1;
```

The initial value of the `tidb_enforce_mpp` session variable is equal to the [`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) configuration value of this tidb-server instance (which is `false` by default). If multiple tidb-server instances in a TiDB cluster only perform analytical queries and you want to make sure that the MPP mode is used on these instances, you can change their [`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) configuration values to `true`.

> **Note:**
>
> When `tidb_enforce_mpp=1` takes effect, the TiDB optimizer will ignore the cost estimation to choose the MPP mode. However, if other factors block the MPP mode, TiDB will not select the MPP mode. These factors include the absence of TiFlash replica, unfinished replication of TiFlash replicas, and statements containing operators or functions that are not supported by the MPP mode.
>
> If TiDB optimizer cannot select the MPP mode due to reasons other than cost estimation, when you use the `EXPLAIN` statement to check out the execution plan, a warning is returned to explain the reason. For example:
>
> {{< copyable "sql" >}}
>
> ```sql
> set @@session.tidb_enforce_mpp=1;
> create table t(a int);
> explain select count(*) from t;
> show warnings;
> ```
>
> ```
> +---------+------+-----------------------------------------------------------------------------+
> | Level   | Code | Message                                                                     |
> +---------+------+-----------------------------------------------------------------------------+
> | Warning | 1105 | MPP mode may be blocked because there aren't tiflash replicas of table `t`. |
> +---------+------+-----------------------------------------------------------------------------+
> ```

### Algorithm support for the MPP mode

The MPP mode supports these physical algorithms: Broadcast Hash Join, Shuffled Hash Join, Shuffled Hash Aggregation, Union All, TopN, and Limit. The optimizer automatically determines which algorithm to be used in a query. To check the specific query execution plan, you can execute the `EXPLAIN` statement. If the result of the `EXPLAIN` statement shows ExchangeSender and ExchangeReceiver operators, it indicates that the MPP mode has taken effect.

The following statement takes the table structure in the TPC-H test set as an example:

```sql
explain select count(*) from customer c join nation n on c.c_nationkey=n.n_nationkey;
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
| id                                       | estRows    | task              | access object | operator info                                                              |
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
| HashAgg_23                               | 1.00       | root              |               | funcs:count(Column#16)->Column#15                                          |
| └─TableReader_25                         | 1.00       | root              |               | data:ExchangeSender_24                                                     |
|   └─ExchangeSender_24                    | 1.00       | batchCop[tiflash] |               | ExchangeType: PassThrough                                                  |
|     └─HashAgg_12                         | 1.00       | batchCop[tiflash] |               | funcs:count(1)->Column#16                                                  |
|       └─HashJoin_17                      | 3000000.00 | batchCop[tiflash] |               | inner join, equal:[eq(tpch.nation.n_nationkey, tpch.customer.c_nationkey)] |
|         ├─ExchangeReceiver_21(Build)     | 25.00      | batchCop[tiflash] |               |                                                                            |
|         │ └─ExchangeSender_20            | 25.00      | batchCop[tiflash] |               | ExchangeType: Broadcast                                                    |
|         │   └─TableFullScan_18           | 25.00      | batchCop[tiflash] | table:n       | keep order:false                                                           |
|         └─TableFullScan_22(Probe)        | 3000000.00 | batchCop[tiflash] | table:c       | keep order:false                                                           |
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
9 rows in set (0.00 sec)
```

In the example execution plan, the `ExchangeReceiver` and `ExchangeSender` operators are included. The execution plan indicates that after the `nation` table is read, the `ExchangeSender` operator broadcasts the table to each node, the `HashJoin` and `HashAgg` operations are performed on the `nation` table and the `customer` table, and then the results are returned to TiDB.

TiFlash provides the following two global/session variables to control whether to use Broadcast Hash Join:

- [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50): The unit of the value is bytes. If the table size (in the unit of bytes) is less than the value of the variable, the Broadcast Hash Join algorithm is used. Otherwise, the Shuffled Hash Join algorithm is used.
- [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50): The unit of the value is rows. If the objects of the join operation belong to a subquery, the optimizer cannot estimate the size of the subquery result set, so the size is determined by the number of rows in the result set. If the estimated number of rows in the subquery is less than the value of this variable, the Broadcast Hash Join algorithm is used. Otherwise, the Shuffled Hash Join algorithm is used.

## Access partitioned tables in the MPP mode

To access partitioned tables in the MPP mode, you need to enable [dynamic pruning mode](https://docs.pingcap.com/tidb/stable/partitioned-table#dynamic-pruning-mode) first.

> **Warning:**
>
> - Currently, dynamic pruning mode for partitioned tables is an experimental feature and is not recommended for production environments.
>
> - Do not enable dynamic pruning mode when a partitioned table contains columns of the `time` type. Otherwise, TiFlash crashes when a query selects a column of the `time` type.

Example:

```sql
mysql> DROP TABLE if exists test.employees;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> CREATE TABLE test.employees (  id int(11) NOT NULL,  fname varchar(30) DEFAULT NULL,  lname varchar(30) DEFAULT NULL,  hired date NOT NULL DEFAULT '1970-01-01',  separated date DEFAULT '99
99-12-31',  job_code int(11) DEFAULT NULL,  store_id int(11) NOT NULL  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin  PARTITION BY RANGE (store_id)  (PARTITION p0 VALUES LESS THAN (
6),  PARTITION p1 VALUES LESS THAN (11),  PARTITION p2 VALUES LESS THAN (16), PARTITION p3 VALUES LESS THAN (MAXVALUE));
Query OK, 0 rows affected (0.10 sec)

mysql> ALTER table test.employees SET tiflash replica 1;
Query OK, 0 rows affected (0.09 sec)

mysql> SET tidb_partition_prune_mode=static;
Query OK, 0 rows affected (0.00 sec)

mysql> explain SELECT count(*) FROM test.employees;
+----------------------------------+----------+-------------------+-------------------------------+-----------------------------------+
| id                               | estRows  | task              | access object                 | operator info                     |
+----------------------------------+----------+-------------------+-------------------------------+-----------------------------------+
| HashAgg_19                       | 1.00     | root              |                               | funcs:count(Column#10)->Column#9  |
| └─PartitionUnion_21              | 4.00     | root              |                               |                                   |
|   ├─StreamAgg_40                 | 1.00     | root              |                               | funcs:count(Column#12)->Column#10 |
|   │ └─TableReader_41             | 1.00     | root              |                               | data:StreamAgg_27                 |
|   │   └─StreamAgg_27             | 1.00     | batchCop[tiflash] |                               | funcs:count(1)->Column#12         |
|   │     └─TableFullScan_39       | 10000.00 | batchCop[tiflash] | table:employees, partition:p0 | keep order:false, stats:pseudo    |
|   ├─StreamAgg_63                 | 1.00     | root              |                               | funcs:count(Column#14)->Column#10 |
|   │ └─TableReader_64             | 1.00     | root              |                               | data:StreamAgg_50                 |
|   │   └─StreamAgg_50             | 1.00     | batchCop[tiflash] |                               | funcs:count(1)->Column#14         |
|   │     └─TableFullScan_62       | 10000.00 | batchCop[tiflash] | table:employees, partition:p1 | keep order:false, stats:pseudo    |
|   ├─StreamAgg_86                 | 1.00     | root              |                               | funcs:count(Column#16)->Column#10 |
|   │ └─TableReader_87             | 1.00     | root              |                               | data:StreamAgg_73                 |
|   │   └─StreamAgg_73             | 1.00     | batchCop[tiflash] |                               | funcs:count(1)->Column#16         |
|   │     └─TableFullScan_85       | 10000.00 | batchCop[tiflash] | table:employees, partition:p2 | keep order:false, stats:pseudo    |
|   └─StreamAgg_109                | 1.00     | root              |                               | funcs:count(Column#18)->Column#10 |
|     └─TableReader_110            | 1.00     | root              |                               | data:StreamAgg_96                 |
|       └─StreamAgg_96             | 1.00     | batchCop[tiflash] |                               | funcs:count(1)->Column#18         |
|         └─TableFullScan_108      | 10000.00 | batchCop[tiflash] | table:employees, partition:p3 | keep order:false, stats:pseudo    |
+----------------------------------+----------+-------------------+-------------------------------+-----------------------------------+
18 rows in set, 4 warnings (0.00 sec)

mysql> SET tidb_partition_prune_mode=dynamic;
Query OK, 0 rows affected (0.00 sec)

mysql> explain SELECT count(*) FROM test.employees;
+------------------------------+----------+-------------------+-----------------+----------------------------------+
| id                           | estRows  | task              | access object   | operator info                    |
+------------------------------+----------+-------------------+-----------------+----------------------------------+
| HashAgg_21                   | 1.00     | root              |                 | funcs:count(Column#11)->Column#9 |
| └─TableReader_23             | 1.00     | root              | partition:all   | data:ExchangeSender_22           |
|   └─ExchangeSender_22        | 1.00     | batchCop[tiflash] |                 | ExchangeType: PassThrough        |
|     └─HashAgg_9              | 1.00     | batchCop[tiflash] |                 | funcs:count(1)->Column#11        |
|       └─TableFullScan_20     | 10000.00 | batchCop[tiflash] | table:employees | keep order:false, stats:pseudo   |
+------------------------------+----------+-------------------+-----------------+----------------------------------+
```

## Data validation

### User scenarios

Data corruptions are usually caused by serious hardware failures. In such cases, even if you attempt to manually recover data, your data become less reliable.

To ensure data integrity, by default, TiFlash performs basic data validation on data files, using the `City128` algorithm. In the event of any data validation failure, TiFlash immediately reports an error and exits, avoiding secondary disasters caused by inconsistent data. At this time, you need to manually intervene and replicate the data again before you can restore the TiFlash node.

Starting from v5.4.0, TiFlash introduces more advanced data validation features. TiFlash uses the `XXH3` algorithm by default and allows you to customize the validation frame and algorithm.

### Validation mechanism

The validation mechanism builds upon the DeltaTree File (DTFile). DTFile is the storage file that persists TiFlash data. DTFile has three formats:

| Version | State | Validation mechanism | Notes |
| :-- | :-- | :-- |:-- |
| V1 | Deprecated | Hashes are embedded in data files. | |
| V2 | Default for versions < v6.0.0 | Hashes are embedded in data files. | Compared to V1, V2 adds statistics of column data. |
| V3 | Default for versions >= v6.0.0 | V3 contains metadata and token data checksum, and supports multiple hash algorithms. | New in v5.4.0. |

DTFile is stored in the `stable` folder in the data file directory. All formats currently enabled are in folder format, which means the data is stored in multiple files under a folder with a name like `dmf_<file id>`.

#### Use data validation

TiFlash supports both automatic and manual data validation:

* Automatic data validation:
    * v6.0.0 and later versions use the V3 validation mechanism by default.
    * Versions earlier than v6.0.0 use the V2 validation mechanism by default.
    * To manually switch the validation mechanism, refer to [TiFlash configuration file](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file). However, the default configuration is verified by tests and therefore recommended.
* Manual data validation. Refer to [`DTTool inspect`](/tiflash/tiflash-command-line-flags.md#dttool-inspect).

> **Warning:**
>
> After you enable the V3 validation mechanism, the newly generated DTFile cannot be directly read by TiFlash earlier than v5.4.0. Since v5.4.0, TiFlash supports both V2 and V3 and does not actively upgrade or downgrade versions. If you need to upgrade or downgrade versions for existing files, you need to manually [switch versions](/tiflash/tiflash-command-line-flags.md#dttool-migrate).

#### Validation tool

In addition to automatic data validation performed when TiFlash reads data, a tool for manually checking data integrity is introduced in v5.4.0. For details, refer to [DTTool](/tiflash/tiflash-command-line-flags.md#dttool-inspect).

## Notes

TiFlash is incompatible with TiDB in the following situations:

* In the TiFlash computation layer:
    * Checking overflowed numerical values is not supported. For example, adding two maximum values of the `BIGINT` type `9223372036854775807 + 9223372036854775807`. The expected behavior of this calculation in TiDB is to return the `ERROR 1690 (22003): BIGINT value is out of range` error. However, if this calculation is performed in TiFlash, an overflow value of `-2` is returned without any error.
    * The window function is not supported.
    * Reading data from TiKV is not supported.
    * Currently, the `sum` function in TiFlash does not support the string-type argument. But TiDB cannot identify whether any string-type argument has been passed into the `sum` function during the compiling. Therefore, when you execute statements similar to `select sum(string_col) from t`, TiFlash returns the `[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.` error. To avoid such an error in this case, you need to modify this SQL statement to `select sum(cast(string_col as double)) from t`.
    * Currently, TiFlash's decimal division calculation is incompatible with that of TiDB. For example, when dividing decimal, TiFlash performs the calculation always using the type inferred from the compiling. However, TiDB performs this calculation using a type that is more precise than that inferred from the compiling. Therefore, some SQL statements involving the decimal division return different execution results when executed in TiDB + TiKV and in TiDB + TiFlash. For example:

        ```sql
        mysql> create table t (a decimal(3,0), b decimal(10, 0));
        Query OK, 0 rows affected (0.07 sec)
        mysql> insert into t values (43, 1044774912);
        Query OK, 1 row affected (0.03 sec)
        mysql> alter table t set tiflash replica 1;
        Query OK, 0 rows affected (0.07 sec)
        mysql> set session tidb_isolation_read_engines='tikv';
        Query OK, 0 rows affected (0.00 sec)
        mysql> select a/b, a/b + 0.0000000000001 from t where a/b;
        +--------+-----------------------+
        | a/b    | a/b + 0.0000000000001 |
        +--------+-----------------------+
        | 0.0000 |       0.0000000410001 |
        +--------+-----------------------+
        1 row in set (0.00 sec)
        mysql> set session tidb_isolation_read_engines='tiflash';
        Query OK, 0 rows affected (0.00 sec)
        mysql> select a/b, a/b + 0.0000000000001 from t where a/b;
        Empty set (0.01 sec)
        ```

        In the example above, `a/b`'s inferred type from the compiling is `Decimal(7,4)` both in TiDB and in TiFlash. Constrained by `Decimal(7,4)`, `a/b`'s returned type should be `0.0000`. In TiDB, `a/b`'s runtime precision is higher than `Decimal(7,4)`, so the original table data is not filtered by the `where a/b` condition. However, in TiFlash, the calculation of `a/b` uses `Decimal(7,4)` as the result type, so the original table data is filtered by the `where a/b` condition.
