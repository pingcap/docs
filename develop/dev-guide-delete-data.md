---
title: 删除数据
summary: 了解用于删除数据的 SQL 语法、最佳实践和示例。
---

# 删除数据

本文档介绍如何使用 [DELETE](/sql-statements/sql-statement-delete.md) SQL 语句在 TiDB 中删除数据。如果你需要定期删除过期数据，可以使用 [time to live](/time-to-live.md) 功能。

## 开始之前

在阅读本文档之前，你需要准备以下内容：

- [构建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md)
- 阅读 [Schema Design Overview](/develop/dev-guide-schema-design-overview.md)、[创建数据库](/develop/dev-guide-create-database.md)、[创建表](/develop/dev-guide-create-table.md) 和 [创建二级索引](/develop/dev-guide-create-secondary-indexes.md)
- [插入数据](/develop/dev-guide-insert-data.md)

## SQL 语法

`DELETE` 语句通常的格式如下：

```sql
DELETE FROM {table} WHERE {filter}
```

| 参数名称 | 描述 |
| :--------: | :------------: |
| `{table}`  |      表名      |
| `{filter}` | 匹配条件的过滤器|

此示例仅展示了 `DELETE` 的简单用法。有关详细信息，请参见 [DELETE 语法](/sql-statements/sql-statement-delete.md)。

## 最佳实践

删除数据时应遵循以下一些最佳实践：

- 始终在 `DELETE` 语句中指定 `WHERE` 子句。如果不指定 `WHERE` 子句，TiDB 将删除表中的 **_所有行_**。

<CustomContent platform="tidb">

- 当你删除大量行（例如超过一万行）时，建议使用 [bulk-delete](#bulk-delete)，因为 TiDB 限制了单个事务的大小（[txn-total-size-limit](/tidb-configuration-file.md#txn-total-size-limit)，默认 100 MB）。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 当你删除大量行（例如超过一万行）时，建议使用 [bulk-delete](#bulk-delete)，因为 TiDB 默认限制单个事务的大小为 100 MB。

</CustomContent>

- 如果要删除表中的所有数据，不要使用 `DELETE` 语句。应改用 [`TRUNCATE`](/sql-statements/sql-statement-truncate.md) 语句。
- 出于性能考虑，详见 [性能注意事项](#performance-considerations)。
- 在需要删除大量数据的场景中，[非事务性批量删除](#non-transactional-bulk-delete) 可以显著提升性能，但会丧失删除的事务性，因此 **不能** 回滚。请确保操作正确。

## 示例

假设你在某个时间段内发现应用程序出现错误，需要删除该时间段内所有的 [ratings](/develop/dev-guide-bookshop-schema-design.md#ratings-table) 数据，例如，从 `2022-04-15 00:00:00` 到 `2022-04-15 00:15:00`。此时，可以先用 `SELECT` 语句检查待删除的记录数。

```sql
SELECT COUNT(*) FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

如果返回的记录数超过 10,000 条，建议使用 [Bulk-Delete](#bulk-delete) 进行删除。

如果返回的记录数少于 10,000 条，可以使用以下示例进行删除。

<SimpleTab groupId="language">
<div label="SQL" value="sql">

在 SQL 中，示例如下：

```sql
DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND `rated_at` <= "2022-04-15 00:15:00";
```

</div>

<div label="Java" value="java">

在 Java 中，示例如下：

```java
// ds 是 com.mysql.cj.jdbc.MysqlDataSource 的实体

try (Connection connection = ds.getConnection()) {
    String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ?";
    PreparedStatement preparedStatement = connection.prepareStatement(sql);
    Calendar calendar = Calendar.getInstance();
    calendar.set(Calendar.MILLISECOND, 0);

    calendar.set(2022, Calendar.APRIL, 15, 0, 0, 0);
    preparedStatement.setTimestamp(1, new Timestamp(calendar.getTimeInMillis()));

    calendar.set(2022, Calendar.APRIL, 15, 0, 15, 0);
    preparedStatement.setTimestamp(2, new Timestamp(calendar.getTimeInMillis()));

    preparedStatement.executeUpdate();
} catch (SQLException e) {
    e.printStackTrace();
}
```

</div>

<div label="Golang" value="golang">

在 Golang 中，示例如下：

```go
package main

import (
    "database/sql"
    "fmt"
    "time"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    startTime := time.Date(2022, 04, 15, 0, 0, 0, 0, time.UTC)
    endTime := time.Date(2022, 04, 15, 0, 15, 0, 0, time.UTC)

    bulkUpdateSql := fmt.Sprintf("DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ?")
    result, err := db.Exec(bulkUpdateSql, startTime, endTime)
    if err != nil {
        panic(err)
    }
    _, err = result.RowsAffected()
    if err != nil {
        panic(err)
    }
}
```

</div>

<div label="Python" value="python">

在 Python 中，示例如下：

```python
import MySQLdb
import datetime
import time
connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)
with connection:
    with connection.cursor() as cursor:
        start_time = datetime.datetime(2022, 4, 15)
        end_time = datetime.datetime(2022, 4, 15, 0, 15)
        delete_sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= %s AND `rated_at` <= %s"
        affect_rows = cursor.execute(delete_sql, (start_time, end_time))
        print(f'delete {affect_rows} data')
```

</div>

</SimpleTab>

<CustomContent platform="tidb">

`rated_at` 字段为 [日期和时间类型](/data-type-date-and-time.md) 中的 `DATETIME` 类型。你可以假设它在 TiDB 中以字面值存储，与时区无关。另一方面，`TIMESTAMP` 类型存储时间戳，因此在不同的 [时区](/configure-time-zone.md) 中显示的时间字符串会不同。

</CustomContent>

<CustomContent platform="tidb-cloud">

`rated_at` 字段为 [日期和时间类型](/data-type-date-and-time.md) 中的 `DATETIME` 类型。你可以假设它在 TiDB 中以字面值存储，与时区无关。另一方面，`TIMESTAMP` 类型存储时间戳，因此在不同的时区显示的时间字符串会不同。

</CustomContent>

> **Note:**
>
> 和 MySQL 一样，`TIMESTAMP` 数据类型受到 [2038 年问题](https://en.wikipedia.org/wiki/Year_2038_problem) 的影响。如果你存储的值大于 2038，建议使用 `DATETIME` 类型。

## 性能注意事项

### TiDB GC 机制

TiDB 在你运行 `DELETE` 语句后，并不会立即删除数据，而是将数据标记为准备删除状态。然后等待 TiDB 的 GC（垃圾回收）清理过期数据。因此，`DELETE` 语句 **_不会_** 立即减少磁盘空间的使用。

GC 默认每 10 分钟触发一次。每次 GC 会计算一个时间点，称为 **safe_point**。在此时间点之前的任何数据将不再被使用，TiDB 可以安全地将其清理。

更多信息，请参见 [GC 机制](/garbage-collection-overview.md)。

### 更新统计信息

TiDB 使用 [统计信息](/statistics.md) 来决定索引的选择。在删除大量数据后，索引可能会被错误选择。你可以使用 [手动收集](/statistics.md#manual-collection) 来更新统计信息，为 SQL 性能优化提供更准确的统计数据。

## 批量删除

当你需要从表中删除多行数据时，可以选择 [示例](#example) 中的 `DELETE`，并使用 `WHERE` 子句过滤需要删除的数据。

<CustomContent platform="tidb">

然而，如果你需要删除大量行（超过一万行），建议采用迭代方式删除，即每次删除一部分数据，直到删除完成。这是因为 TiDB 限制了单个事务的大小（[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)，默认 100 MB）。你可以在程序或脚本中使用循环执行此类操作。

</CustomContent>

<CustomContent platform="tidb-cloud">

然而，如果你需要删除大量行（超过一万行），建议采用迭代方式删除，即每次删除一部分数据，直到删除完成。这是因为 TiDB 默认限制单个事务的大小为 100 MB。你可以在程序或脚本中使用循环执行此类操作。

</CustomContent>

本节提供一个示例，演示如何编写脚本实现迭代删除操作，结合 `SELECT` 和 `DELETE` 完成批量删除。

### 编写批量删除循环

你可以在应用或脚本的循环中写入 `DELETE` 语句，使用 `WHERE` 子句过滤数据，并用 `LIMIT` 限制单次删除的行数。

### 批量删除示例

假设你在某个时间段内发现应用程序出现错误，需要删除该时间段内所有的 [rating](/develop/dev-guide-bookshop-schema-design.md#ratings-table) 数据，例如，从 `2022-04-15 00:00:00` 到 `2022-04-15 00:15:00`，在 15 分钟内写入了超过 1 万条记录。可以按如下方式操作。

<SimpleTab groupId="language">
<div label="Java" value="java">

在 Java 中，批量删除示例如下：

```java
package com.pingcap.bulkDelete;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.*;
import java.util.*;
import java.util.concurrent.TimeUnit;

public class BatchDeleteExample
{
    public static void main(String[] args) throws InterruptedException {
        // 配置示例数据库连接。

        // 创建一个 mysql 数据源实例。
        MysqlDataSource mysqlDataSource = new MysqlDataSource();

        // 设置服务器名、端口、数据库名、用户名和密码。
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
            String sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ? LIMIT 1000";
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

每次迭代中，`DELETE` 最多删除 1000 行，从 `2022-04-15 00:00:00` 到 `2022-04-15 00:15:00`。

</div>

<div label="Golang" value="golang">

在 Golang 中，批量删除示例如下：

```go
package main

import (
    "database/sql"
    "fmt"
    "time"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:4000)/bookshop")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    affectedRows := int64(-1)
    startTime := time.Date(2022, 04, 15, 0, 0, 0, 0, time.UTC)
    endTime := time.Date(2022, 04, 15, 0, 15, 0, 0, time.UTC)

    for affectedRows != 0 {
        affectedRows, err = deleteBatch(db, startTime, endTime)
        if err != nil {
            panic(err)
        }
    }
}

// deleteBatch 每次最多删除 1000 行
func deleteBatch(db *sql.DB, startTime, endTime time.Time) (int64, error) {
    bulkUpdateSql := fmt.Sprintf("DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= ? AND `rated_at` <= ? LIMIT 1000")
    result, err := db.Exec(bulkUpdateSql, startTime, endTime)
    if err != nil {
        return -1, err
    }
    affectedRows, err := result.RowsAffected()
    if err != nil {
        return -1, err
    }

    fmt.Printf("delete %d data\n", affectedRows)
    return affectedRows, nil
}
```

每次迭代中，`DELETE` 最多删除 1000 行，从 `2022-04-15 00:00:00` 到 `2022-04-15 00:15:00`。

</div>

<div label="Python" value="python">

在 Python 中，批量删除示例如下：

```python
import MySQLdb
import datetime
import time
connection = MySQLdb.connect(
    host="127.0.0.1",
    port=4000,
    user="root",
    password="",
    database="bookshop",
    autocommit=True
)
with connection:
    with connection.cursor() as cursor:
        start_time = datetime.datetime(2022, 4, 15)
        end_time = datetime.datetime(2022, 4, 15, 0, 15)
        affect_rows = -1
        while affect_rows != 0:
            delete_sql = "DELETE FROM `bookshop`.`ratings` WHERE `rated_at` >= %s AND  `rated_at` <= %s LIMIT 1000"
            affect_rows = cursor.execute(delete_sql, (start_time, end_time))
            print(f'delete {affect_rows} data')
            time.sleep(1)
```

每次迭代中，`DELETE` 最多删除 1000 行，从 `2022-04-15 00:00:00` 到 `2022-04-15 00:15:00`。

</div>

</SimpleTab>

## 非事务性批量删除

> **Note:**
>
> 自 v6.1.0 版本起，TiDB 支持 [非事务性 DML 语句](/non-transactional-dml.md)。此功能不适用于 TiDB v6.1.0 之前的版本。

### 非事务性批量删除的前提条件

在使用非事务性批量删除前，请确保已阅读 [非事务性 DML 语句文档](/non-transactional-dml.md)。非事务性批量删除在批量数据处理场景中提升了性能和易用性，但会牺牲事务的原子性和隔离性。

因此，应谨慎使用，避免因操作不当导致严重后果（如数据丢失）。

### 非事务性批量删除的 SQL 语法

非事务性批量删除语句的 SQL 语法如下：

```sql
BATCH ON {shard_column} LIMIT {batch_size} {delete_statement};
```

| 参数名称 | 描述 |
| :--------: | :------------: |
| `{shard_column}` | 用于分批的列名。      |
| `{batch_size}`   | 控制每批的大小。 |
| `{delete_statement}` | `DELETE` 语句。 |

上述示例仅展示了非事务性批量删除语句的简单用法。详细信息请参见 [非事务性 DML 语句](/non-transactional-dml.md)。

### 非事务性批量删除示例

在与 [批量删除示例](#bulk-delete-example) 相同的场景中，以下 SQL 语句演示了如何执行非事务性批量删除：

```sql
BATCH ON `rated_at` LIMIT 1000 DELETE FROM `ratings` WHERE `rated_at` >= "2022-04-15 00:00:00" AND  `rated_at` <= "2022-04-15 00:15:00";
```

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>