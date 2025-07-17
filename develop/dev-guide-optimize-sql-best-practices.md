---
title: 性能调优最佳实践
summary: 介绍 TiDB 性能调优的最佳实践。
---

# 性能调优最佳实践

本文档介绍了一些使用 TiDB 数据库的最佳实践。

## DML 最佳实践

本节描述在使用 TiDB 进行 DML 操作时的最佳实践。

### 使用多行语句

当需要修改多行数据时，建议使用多行语句：

```sql
INSERT INTO t VALUES (1, 'a'), (2, 'b'), (3, 'c');

DELETE FROM t WHERE id IN (1, 2, 3);
```

不建议使用多条单行语句：

```sql
INSERT INTO t VALUES (1, 'a');
INSERT INTO t VALUES (2, 'b');
INSERT INTO t VALUES (3, 'c');

DELETE FROM t WHERE id = 1;
DELETE FROM t WHERE id = 2;
DELETE FROM t WHERE id = 3;
```

### 使用 `PREPARE`

当需要多次执行某条 SQL 语句时，建议使用 `PREPARE` 语句，以避免重复解析 SQL 语法带来的开销。

<SimpleTab>
<div label="Golang">

```go
func BatchInsert(db *sql.DB) error {
    stmt, err := db.Prepare("INSERT INTO t (id) VALUES (?), (?), (?), (?), (?)")
    if err != nil {
        return err
    }
    for i := 0; i < 1000; i += 5 {
        values := []interface{}{i, i + 1, i + 2, i + 3, i + 4}
        _, err = stmt.Exec(values...)
        if err != nil {
            return err
        }
    }
    return nil
}
```

</div>

<div label="Java">

```java
public void batchInsert(Connection connection) throws SQLException {
    PreparedStatement statement = connection.prepareStatement(
            "INSERT INTO `t` (`id`) VALUES (?), (?), (?), (?), (?)");
    for (int i = 0; i < 1000; i ++) {
        statement.setInt(i % 5 + 1, i);

        if (i % 5 == 4) {
            statement.executeUpdate();
        }
    }
}
```

</div>
</SimpleTab>

不要反复执行 `PREPARE` 语句，否则无法提升执行效率。

### 只查询需要的列

如果不需要所有列的数据，不要使用 `SELECT *` 返回全部列。以下查询效率较低：

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

应只查询需要的列，例如：

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

### 使用批量删除

当需要删除大量数据时，建议使用 [bulk delete](/develop/dev-guide-delete-data.md#bulk-delete)。

### 使用批量更新

当需要更新大量数据时，建议使用 [bulk update](/develop/dev-guide-update-data.md#bulk-update)。

### 使用 `TRUNCATE` 替代 `DELETE` 进行全表数据删除

当需要删除表中的所有数据时，建议使用 `TRUNCATE` 语句：

```sql
TRUNCATE TABLE t;
```

不建议使用 `DELETE` 进行全表删除：

```sql
DELETE FROM t;
```

## DDL 最佳实践

本节描述在使用 TiDB 的 DDL 时的最佳实践。

### 主键最佳实践

请参阅 [选择主键的规则](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)。

## 索引最佳实践

请参阅 [索引最佳实践](/develop/dev-guide-index-best-practice.md)。

### 添加索引的最佳实践

TiDB 支持在线添加索引操作。你可以使用 [ADD INDEX](/sql-statements/sql-statement-add-index.md) 或 [CREATE INDEX](/sql-statements/sql-statement-create-index.md) 语句添加索引。此操作不会阻塞表中的数据读写。在索引添加的 `re-organize` 阶段，你可以通过修改以下系统变量调整并发度和批次大小：

* [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
* [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

为了减少对线上应用的影响，默认索引添加速度较慢。当索引目标列只涉及读负载或与线上工作负载关系不大时，可以适当提高上述变量的值以加快索引添加速度：

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;
```

当索引目标列频繁更新（包括 `UPDATE`、`INSERT` 和 `DELETE`）时，增大上述变量会导致更多写冲突，影响线上工作负载。因此，索引添加可能会因为不断重试而耗时较长。此时，建议降低上述变量的值以避免与线上应用的写冲突：

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 4;
SET @@global.tidb_ddl_reorg_batch_size = 128;
```

## 事务冲突

<CustomContent platform="tidb">

关于如何定位和解决事务冲突，参见 [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

关于如何定位和解决事务冲突，参见 [Troubleshoot Lock Conflicts](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)。

</CustomContent>

## 使用 TiDB 开发 Java 应用的最佳实践

<CustomContent platform="tidb">

请参阅 [使用 TiDB 开发 Java 应用的最佳实践](/best-practices/java-app-best-practices.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

请参阅 [使用 TiDB 开发 Java 应用的最佳实践](https://docs.pingcap.com/tidb/stable/java-app-best-practices)。

</CustomContent>

### 另请参阅

<CustomContent platform="tidb">

- [高并发写入的最佳实践](/best-practices/high-concurrency-best-practices.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [高并发写入的最佳实践](https://docs.pingcap.com/tidb/stable/high-concurrency-best-practices)

</CustomContent>

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>