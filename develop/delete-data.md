---
title: Delete Data
summary: The ways, best practices, and examples for deleting data, bulk data deletion.
---

# Delete Data

This page will use the [DELETE](/common/sql-statements/sql-statement-delete.md) SQL statement to delete the data in TiDB.

## Before you start

Before reading this page, you need to prepare the following:

- [Build a TiDB Cluster in TiDB Cloud(DevTier)](/develop/build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/schema-design-overview.md), [Create a Database](/develop/create-database.md), [Create a Table](/develop/create-table.md), and [Create Secondary Indexes](/develop/create-secondary-indexes.md).
- If you need to delete data, you need to [insert data](/develop/insert-data.md) first.

## SQL Syntax

In SQL, the `DELETE` statement is generally of the following form:

{{< copyable "sql" >}}

```sql
DELETE FROM {table} WHERE {filter}
```

| Parameter Name | Description |
| :--------: | :------------: |
| `{table}`  |      Table Name      |
| `{filter}` | Filter matching conditions |

This only shows a simple usage of `DELETE`. For detailed documentation, refer to TiDB's [DELETE syntax](/common/sql-statements/sql-statement-delete.md) page.

## Best Practices

There are some best practices to follow when delete rows as follows:

- Always specify the `WHERE` clause in the delete statement. If the `DELETE` does not have a `WHERE` clause, TiDB will delete **_ALL ROWS_** within this table.
- Use [bulk-delete](#bulk-delete) when you need to delete a large number of rows (tens of thousands or more), because TiDB has a single transaction size limit of [txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit) (default is 100MB).
- If you need to delete all the data in a table, do not use the `DELETE` statement; instead, use the [TRUNCATE](/common/sql-statements/sql-statement-truncate.md) statement.
- See [Performance Considerations](#performance-considerations).

## Example

Suppose we find that a application error has occurred within a specific time period and we need to delete all the data for the [rating](/develop/bookshop-schema-design.md#ratings-table) within this period, for example, `2022-04-15 00:00:00` to `2022-04-15 00:15:00`. In this case, you can use the `SELECT` statement to see the number of data items to be deleted.

{{< copyable "sql" >}}

```sql
SELECT COUNT(*) FROM `rating` WHERE `rating_at` >= "2022-04-15 00:00:00" AND  `rating_at` <= "2022-04-15 00:15:00";
```

- If the number of returned items is greater than 10,000, please check and use the [Bulk-Delete](#bulk-delete).
- If the number of returned items is less than 10,000, you can use the example here to delete.

<SimpleTab>
<div label="SQL" href="delete-sql">

{{< copyable "sql" >}}

```sql
DELETE FROM `rating` WHERE `rating_at` >= "2022-04-15 00:00:00" AND  `rating_at` <= "2022-04-15 00:15:00";
```

</div>

<div label="Java" href="delete-java">

{{< copyable "" >}}

```java
// ds is an entity of com.mysql.cj.jdbc.MysqlDataSource

try (Connection connection = ds.getConnection()) {
    PreparedStatement pstmt = connection.prepareStatement("DELETE FROM `rating` WHERE `rating_at` >= ? AND  `rating_at` <= ?");
    Calendar calendar = Calendar.getInstance();
    calendar.set(Calendar.MILLISECOND, 0);

    calendar.set(2022, Calendar.APRIL, 15, 0, 0, 0);
    pstmt.setTimestamp(1, new Timestamp(calendar.getTimeInMillis()));

    calendar.set(2022, Calendar.APRIL, 15, 0, 15, 0);
    pstmt.setTimestamp(2, new Timestamp(calendar.getTimeInMillis()));
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>
</SimpleTab>

> **Note:**
>
> Note here that the `rating_at` field is the `DATETIME` type of the [Date and Time Types](/data-type-date-and-time.md), which you can assume is stored as a literal quantity in TiDB, independent of the time zone. On the other hand, the `TIMESTAMP` type, will store a timestamp and thus display a different time string when [configured time zone](/configure-time-zone.md) differently.
>
> Also, like MySQL, the `TIMESTAMP` data type is affected by the [year 2038 problem](https://en.wikipedia.org/wiki/Year_2038_problem). It is recommended to use the DATETIME type if storing values larger than 2038.

## Performance Considerations

### TiDB GC Mechanism

TiDB does not delete the data immediately after the `DELETE` statement runs, but instead marks the data as ready for deletion. Then it waits for TiDB GC (Garbage Collection) to clean up the old data that is no longer needed. Therefore, your DELETE statement **_DOES NOT_** immediately reduce disk usage.

GC is triggered once every 10 minutes in the default configuration, and each GC calculates a time point called **safe_point**, and any data before this time point will not be used again, so TiDB can safely clean up the data.

You can read the introduction of [GC mechanism](/garbage-collection-overview.md) to get more detailed description of GC.

### Update statistical information

TiDB uses [statistical information](/statistics.md) to determine index selection, so there is a high risk that incorrect index selection will occur after a large volume of data is deleted. You can use a [manual collection](/statistics.md#manual-collection) to update the statistics. Use this to give the TiDB optimizer more accurate statistical information to provide SQL performance optimization.

## Bulk-delete

When you need to delete multiple rows of data from a table, you can choose the [`DELETE` example](#example) and use the `WHERE` clause to filter the data that needs to be deleted.

However, if you need to delete a large number of rows (tens of thousands or more), we recommend using an iteration that deletes a portion of the data at a time until the deletion is complete. This is because TiDB has a single transaction size limit of [txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit) (default is 100MB). You can use loops in your programs or scripts to complete operations.

This page provides an example of writing a script to handle a circular delete that demonstrates how you should do a combination of `SELECT` and `DELETE` to complete a bulk-delete.

### Write bulk-delete loop

First, you should write a `SELECT` query in a loop of your application or script. The return value of this query can be used as the primary key for the rows that need to be delete. Note that when defining this `SELECT` query, you need to be careful to use the `WHERE` clause to filter the rows that need to be delete.

### Bulk-delete Example

Suppose we find that a application error has occurred within a specific time period and we need to delete all the data for the [rating](/develop/bookshop-schema-design.md#ratings-table) within this period, for example, `2022-04-15 00:00:00` to `2022-04-15 00:15:00`, and more than 10,000 data are written in 15 minutes, we should use a round robin deletion to delete.

{{< copyable "" >}}

```java
package com.pingcap.bulkDelete;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.*;
import java.util.*;
import java.util.concurrent.TimeUnit;

public class BatchDeleteExample
{
    public static void main(String[] args) throws InterruptedException {
        // Configure the example database connection.

        // Create a mysql data source instance.
        MysqlDataSource mysqlDataSource = new MysqlDataSource();

        // Set server name, port, database name, username and password.
        mysqlDataSource.setServerName("localhost");
        mysqlDataSource.setPortNumber(4000);
        mysqlDataSource.setDatabaseName("bookshop");
        mysqlDataSource.setUser("root");
        mysqlDataSource.setPassword("");

        while (true) {
            batchDelete(mysqlDataSource);
            TimeUnit.SECONDS.sleep(1);
        }
    }

    public static void batchDelete (MysqlDataSource ds) {
        try (Connection connection = ds.getConnection()) {
            String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND  `rated_at` <= ? LIMIT 1000";
            PreparedStatement preparedStatement = connection.prepareStatement(sql);
            Calendar calendar = Calendar.getInstance();
            calendar.set(Calendar.MILLISECOND, 0);

            calendar.set(2022, Calendar.APRIL, 15, 0, 0, 0);
            preparedStatement.setTimestamp(1, new Timestamp(calendar.getTimeInMillis()));

            calendar.set(2022, Calendar.APRIL, 15, 0, 15, 0);
            preparedStatement.setTimestamp(2, new Timestamp(calendar.getTimeInMillis()));

            int count = preparedStatement.executeUpdate();
            System.out.println("delete " + count + " data");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

In each iteration, `SELECT` selects up to 1000 rows of primary key values for data in the time period `2022-04-15 00:00:00` to `2022-04-15 00:15:00`. Then do a bulk-delete. `TimeUnit.SECONDS.sleep(1);` at the end of each loop will cause the bulk-delete application to pause for `1` second, preventing the bulk-delete application from taking up too many hardware resources.