---
title: Insert Data
summary: The ways, best practices and examples for inserting data, bulk data import.
---

<!-- markdownlint-disable MD029 -->

# Insert Data

This page will demonstrate the use of SQL language with different programming languages to insert data into TiDB.

## Before you start

Before reading this page, you need to prepare the following:

- [Build a TiDB Cluster in TiDB Cloud(DevTier)](/develop/build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/schema-design-overview.md), [Create a Database](/develop/create-database.md), [Create a Table](/develop/create-table.md), and [Create Secondary Indexes](/develop/create-secondary-indexes.md)

## Insert Rows

Assuming that you need to insert multiple rows of data, there would be two ways to insert, for example, if we need to insert **3** players' data.

- A **multi-line insertion statement**：

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2), (3, 300, 5);
    ```

- Multiple **single-line insertion statements**：

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (2, 230, 2);
    INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (3, 300, 5);
    ```

Generally using a `multi-line insertion statement` will be faster than multiple `single-line insertion statements`.

<SimpleTab>
<div label="SQL">

{{< copyable "sql" >}}

```sql
CREATE TABLE `player` (`id` INT, `coins` INT, `goods` INT);
INSERT INTO `player` (`id`, `coins`, `goods`) VALUES (1, 1000, 1), (2, 230, 2);
```

For more information on how to use this SQL, see the [Connecting to a TiDB Cluster](/develop/build-cluster-in-cloud.md#step-2-connect-to-a-cluster) documentation section and follow the documentation steps to enter the SQL statement after connecting to a TiDB cluster using a client.

</div>

<div label="Java">

{{< copyable "" >}}

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource
try (Connection connection = ds.getConnection()) {
    connection.setAutoCommit(false);

    PreparedStatement pstmt = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)"))

    // first player
    pstmt.setInt(1, 1);
    pstmt.setInt(2, 1000);
    pstmt.setInt(3, 1);
    pstmt.addBatch();

    // second player
    pstmt.setInt(1, 2);
    pstmt.setInt(2, 230);
    pstmt.setInt(3, 2);
    pstmt.addBatch();

    pstmt.executeBatch();
    connection.commit();
} catch (SQLException e) {
    e.printStackTrace();
}
```

Also, due to the default MySQL JDBC Driver settings, you will need to change some of the parameters to get better bulk insert performance.

|            Parameter            |                 Means                  |   Recommended Scenario   | Recommended Configuration|
| :------------------------: | :-----------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------: |
|    `useServerPrepStmts`    |    Whether to use the server side to enable prepared statement support    |  When you need to use a prepared statement more than once                                                             |          `true`          |
|      `cachePrepStmts`      |       Whether the client caches prepared statement        |                                                           `useServerPrepStmts=true` 时                                                            |          `true`          |
|  `prepStmtCacheSqlLimit`   |  Maximum size of a prepared statement (default 256 characters)  | When the prepared statement is greater than 256 characters | Configured according to the actual size of the prepared statement |
|    `prepStmtCacheSize`     | Maximum number of prepared statement caches (default 25) | When the number of prepared statement is greater than 25  | Configured according to the actual number of prepared statements |
| `rewriteBatchedStatements` |          Whether to rewrite **Batched** statements          | When batch operations are required |          `true`          |
|    `allowMultiQueries`     |             Start batch operations              | Because a [client bug](https://bugs.mysql.com/bug.php?id=96623) requires this to be set when `rewriteBatchedStatements = true` and `useServerPrepStmts = true` |          `true`          |

MySQL JDBC Driver also provides an integrated configuration item: `useConfigs`. When it is configured with `maxPerformance`, it is equivalent to configuring a set of configurations, for example, `mysql:mysql-connector-java:8.0.28`, `useConfigs=maxPerformance` contains:

{{< copyable "" >}}

```properties
cachePrepStmts=true
cacheCallableStmts=true
cacheServerConfiguration=true
useLocalSessionState=true
elideSetAutoCommits=true
alwaysSendSetIsolation=false
enableQueryTimeouts=false
connectionAttributes=none
useInformationSchema=true
```

You can check `mysql-connector-java-{version}.jar!/com/mysql/cj/configurations/maxPerformance.properties` yourself to get the `useConfigs=maxPerformance` contains configurations for the corresponding version of MySQL JDBC Driver.

A more generic scenario of JDBC connection string configuration is given here, with Host: `127.0.0.1`, Port: `4000`, User name: `root`, Password: null, Default database: `test` as an example:

{{< copyable "" >}}

```
jdbc:mysql://127.0.0.1:4000/test?user=root&useConfigs=maxPerformance&useServerPrepStmts=true&prepStmtCacheSqlLimit=2048&prepStmtCacheSize=256&rewriteBatchedStatements=true&allowMultiQueries=true
```

For a complete example in Java, see:

- [Build a Simple CRUD App with TiDB and Java - Using JDBC](/develop/sample-application-java.md#step-2-get-the-code)
- [Build a Simple CRUD App with TiDB and Java - Using Hibernate](/develop/sample-application-java.md#step-2-get-the-code)
- [Build the TiDB Application using Spring Boot](/develop/sample-application-spring-boot.md)

</div>

</SimpleTab>

## Bulk-Insert

If you need to quickly import a large amount of data into a TiDB cluster, the best way to do it is not to use the `INSERT` statement, which is not the most efficient way and requires you to handle exceptions and other issues on your own. We recommend using a range of tools provided by **PingCAP** for data migration.

- Data export tool: [Dumpling](/dumpling-overview.md). You can export MySQL or TiDB data to local or Amazon S3.
- Data import tool: [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md). You can import **Dumpling** exported data, a **CSV** file, or [Migrate Data from Amazon Aurora to TiDB](/migrate-aurora-to-tidb.md). It also supports reading data from a local disk or [Amazon S3 cloud disk](/br/backup-and-restore-storages.md).
- Data synchronization tool: [TiDB Data Migration](/dm/dm-overview.md). You can synchronize MySQL, MariaDB, and Amazon Aurora databases to TiDB. It also supports merging and migrating the original sharded instances and tables from the source databases.
- Data backup restore tool: [Backup & Restore (BR)](/br/backup-and-restore-tool.md). Compared to **Dumpling**, **BR** is more suitable for **_big data_** scenario.

## Avoid hot spots

When designing a table you need to consider if there is a large number of inserts. And if so, you need to avoid hotspots during table design. See the [Select primary key](/develop/create-table.md#select-primary-key) section and follow the [Rules when selecting primary key](/develop/create-table.md#rules-to-follow-when-selecting-primary-key).

For more information on how to handle hotspot issues, please refer to the [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md) documentation.

## Insert data to a table with `AUTO_RANDOM` primary key

In case the primary key of the table we insert has the `AUTO_RANDOM` attribute, then by default, the primary key cannot be specified. For example, in the [bookshop](/develop/bookshop-schema-design.md) database, we can see that the `id` field of the [users table](/develop/bookshop-schema-design.md#users-table) contains the `AUTO_RANDOM` attribute.

In this case, we cannot use SQL like the following to insert:

{{< copyable "sql" >}}

```sql
INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
```

An error will occur：

```
ERROR 8216 (HY000): Invalid auto random: Explicit insertion on auto_random column is disabled. Try to set @@allow_auto_random_explicit_insert = true.
```

This is intended to indicate to you that it is not recommended to manually specify the `AUTO_RANDOM` column at insert time. At this point, you have two solutions to handle this error:

- (Recommended) Remove this column from the insert statement and use the `AUTO_RANDOM` value that TiDB initialized for you. This fits the semantics of `AUTO_RANDOM`.

    {{< copyable "sql" >}}

    ```sql
    INSERT INTO `bookshop`.`users` (`balance`, `nickname`) VALUES (0.00, 'nicky');
    ```

- If you confirm that you **_must_** specify this column, then you can use the [SET statement](https://docs.pingcap.com/zh/tidb/stable/sql-statement-set-variable) to allow the column of `AUTO_RANDOM` to be specified at insert time by changing the user variable.

    {{< copyable "sql" >}}

    ```sql
    SET @@allow_auto_random_explicit_insert = true;
    INSERT INTO `bookshop`.`users` (`id`, `balance`, `nickname`) VALUES (1, 0.00, 'nicky');
    ```

## Using HTAP

In TiDB, using HTAP capabilities does not require you to perform additional operations when inserting data. There is no additional insertion logic, and TiDB does the data consistency assurance automatically. All you need to do is [turn on column-oriented copy synchronization](/develop/create-table.md#using-htap-capabilities) after creating the table and you can use the column copy to speed up your queries directly.
